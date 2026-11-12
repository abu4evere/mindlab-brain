"""W1d runner (questions.md, W1d-frozen).

  python workbench/W1d/run_w1d.py probes                    # moving-food probe -> moving.json (seed 20261119)
  python workbench/W1d/run_w1d.py checks                    # -> checks.log
  python workbench/W1d/run_w1d.py learn V|V1|Vm|Vac SEED [EPISODES]
"""
from __future__ import annotations

import contextlib
import io
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "W1c"))
import vin as V  # noqa: E402
import run_w1c as C  # noqa: E402  (W1c's probe sets and helpers)

B1, W = V.B1, V.W
OUT = HERE / "output"
EPISODES = 30_000
MOVE_SEED = 20261119
K_SWEEP = [1, 5, 10, 15, 20, 30]


def make(kind, seed):
    if kind == "V1":
        return V.VIN(seed, 1)
    if kind == "Vm":
        return V.VIN(seed, 30, "mean")
    return V.VIN(seed, 30)


# --- probes ----------------------------------------------------------------------------------------------------------
def build_moving():
    d = W.load()
    rng = np.random.default_rng(MOVE_SEED)
    out = []
    for k, lay in enumerate(d["test"]):
        if not lay["detour"]:
            continue
        cells = [(x, y) for x in range(W.N) for y in range(W.N) if (x, y) not in lay["walls"]]
        out.append({"k": k, "cells": [list(c) for c in cells], "pick": int(rng.integers(1 << 30))})
    (HERE / "moving.json").write_text(json.dumps({"seed": MOVE_SEED, "items": out}), encoding="utf-8")
    print("moving-food items", len(out))


def run(net, lay, move=None):
    """One test episode (arg-max actions). With `move`, the food moves after the 3rd step to an open cell at least 4
    from the agent (chosen by the item's own draw); success = reaching the new food within 1.15 x the shortest path
    from where the agent was when it moved."""
    env = W.Env(lay)
    net.reset()
    path = [env.pos]
    moved_at, new_short = None, None
    while not env.done:
        if move is not None and env.t == 3 and moved_at is None:
            r = np.random.default_rng(move["pick"])
            cands = [tuple(c) for c in move["cells"] if W.manhattan(tuple(c), env.pos) >= 4 and tuple(c) != env.goal]
            env.goal = cands[int(r.integers(len(cands)))]
            moved_at = env.t
            new_short = W.shortest(env.walls, env.pos, env.goal)[0]
        z = net.step(env.obs())[2]
        env.step(int(np.argmax(z)))
        path.append(env.pos)
    ok = env.pos == env.goal
    if move is not None:
        return {"solved": ok, "efficient": bool(ok and new_short and env.t - moved_at <= W.EFF * new_short)}
    return {"set": lay.get("set"), "family": lay["family"], "detour": lay["detour"], "solved": ok, "steps": env.t,
            "shortest": lay["shortest"], "efficient": ok and env.t <= W.EFF * lay["shortest"],
            "first3": C.first3(lay, path) if lay["detour"] else None}


def value_map_corr(net, lay):
    """Spearman correlation between the final v map and -(true BFS distance) over reachable cells."""
    env = W.Env(lay)
    net.reset()
    net.step(env.obs())
    q = net.fw[3]
    v = q.max(1) if net.mode == "max" else np.tanh(q.mean(1))
    xs, ys = [], []
    for x in range(W.N):
        for y in range(W.N):
            if (x, y) in lay["walls"]:
                continue
            dd = W.shortest(lay["walls"], (x, y), lay["goal"])[0]
            if dd is not None:
                xs.append(v[y * W.N + x])
                ys.append(-dd)
    rx, ry = np.argsort(np.argsort(xs)), np.argsort(np.argsort(ys))
    return float(np.corrcoef(rx, ry)[0, 1])


def learn(kind, seed, episodes=None):
    episodes = episodes or EPISODES
    d, pr = W.load(), C.load_probes()
    mv = json.loads((HERE / "moving.json").read_text())["items"]
    rng = np.random.default_rng([seed, 1])
    net = make(kind, [seed, 2])
    ok, curve = [], []
    for ep in range(episodes):
        lay = d["learn"][int(rng.integers(len(d["learn"])))]
        if kind == "Vac":
            ok.append(B1.episode_ac(net, W.Env(lay), rng))
        else:
            B1.episode_imit(net, W.Env(lay), lay)
        if (ep + 1) % 3000 == 0:
            curve.append({"episode": ep + 1, "train_success": float(np.mean(ok[-3000:])) if ok else None})
    res = {"brain": kind, "seed": seed, "episodes": episodes, "curve": curve,
           "test": [run(net, l) for l in d["test"]],
           "empty": [run(net, l) for l in pr["empty"]],
           "held": [run(net, l) for l in pr["held"]],
           "moving": [run(net, d["test"][m["k"]], m) for m in mv]}
    if kind in ("V", "V1", "Vm"):
        res["value_corr"] = float(np.mean([value_map_corr(net, l) for l in d["test"]]))
    if kind == "V":
        keep = net.K
        res["k_sweep"] = {}
        for k in K_SWEEP:
            net.K = k
            res["k_sweep"][str(k)] = [run(net, l) for l in d["test"]]
        net.K = keep
    OUT.mkdir(exist_ok=True)
    tag = "" if episodes == EPISODES else f"_{episodes // 1000}k"
    (OUT / f"{kind}{tag}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    det = [r for r in res["test"] if r["detour"]]
    con = [r for r in res["test"] if not r["detour"]]
    print(kind, seed, episodes, "control", round(np.mean([r["solved"] for r in con]), 3), "eff detour",
          round(np.mean([r["efficient"] for r in det]), 3), flush=True)


def checks():
    lines, ok = [], True
    d = W.load()
    rng = np.random.default_rng(6)
    # gradients (max: nudges that flip a max are skipped; mean: all)
    for mode, K in (("max", 1), ("max", 30), ("mean", 30)):
        lay = d["learn"][6]
        net = V.VIN([3, K], K, mode)
        env = W.Env(lay)
        _, path = W.shortest(lay["walls"], lay["start"], lay["goal"])
        xs = []
        for c in path[:6]:
            env.pos = c
            xs.append(env.obs())
        dl = [rng.normal(0, 1, 5) for _ in xs]
        dv = [float(rng.normal()) for _ in xs]

        def loss():
            net.reset()
            tot = 0.0
            for t, x in enumerate(xs):
                _, h, z, v = net.step(x)
                tot += float(dl[t] @ z) + dv[t] * v
            return tot

        def ams():
            net.reset()
            net.step(xs[0])
            return b"".join(np.asarray(a).tobytes() for _, a in net.fw[2]) if mode == "max" else b""
        net.reset()
        hs = [net.step(x)[1] for x in xs]
        g = net.backward(xs, None, hs, dl, dv)
        worst, flips = 0.0, 0
        for name, P in net.p.items():
            f, gf = P.reshape(-1), g[name].reshape(-1)
            for i in rng.choice(f.size, min(15, f.size), replace=False):
                o = f[i]
                base = ams()
                f[i] = o + 1e-7
                lp, a1 = loss(), ams()
                f[i] = o - 1e-7
                lm, a2 = loss(), ams()
                f[i] = o
                if a1 != base or a2 != base:
                    flips += 1
                    continue
                num = (lp - lm) / 2e-7
                worst = max(worst, abs(num - gf[i]) / max(1e-3, abs(num) + abs(gf[i])))
        good = worst < 1e-3
        ok &= good
        lines.append(f"gradients equal finite differences, VIN {mode} K={K}: {'yes' if good else 'NO'} "
                     f"(worst rel. {worst:.1e}; {flips} nudges skipped for flipping a max)")
    # the moving-food probe: the same for every brain, food moved to an open cell
    mv = json.loads((HERE / "moving.json").read_text())["items"]
    good = len(mv) == 120 and all(d["test"][m["k"]]["detour"] for m in mv)
    ok &= good
    lines.append(f"moving-food probe: 120 items, one per detour test layout: {'yes' if good else 'NO'}")
    # the same seed twice
    global EPISODES
    keep, EPISODES = EPISODES, 50
    outs = []
    for _ in range(2):
        with contextlib.redirect_stdout(io.StringIO()):
            learn("V", 99)
        outs.append((OUT / "V_seed_99.json").read_text())
    (OUT / "V_seed_99.json").unlink()
    EPISODES = keep
    same = outs[0] == outs[1]
    ok &= same
    lines.append(f"the same seed gives the same result twice (V, 50 episodes): {'yes' if same else 'NO'}")
    lines.append(f"All: {'PASS' if ok else 'FAIL'}")
    (HERE / "checks.log").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "probes":
        build_moving()
    elif cmd == "checks":
        checks()
    elif cmd == "learn":
        learn(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else None)
