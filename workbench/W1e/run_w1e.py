"""W1e runner (questions.md, W1e-frozen): V (W1d's VIN, retrained) and V+ (the plus-shaped propagation filter), with
three read-out diagnostics: the map read-out, step accuracy, and near-ties.

  python workbench/W1e/run_w1e.py checks
  python workbench/W1e/run_w1e.py learn V|Vp SEED [EPISODES]
"""
from __future__ import annotations

import contextlib
import io
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "W1d"))
import run_w1d as D  # noqa: E402

V, W, B1, C = D.V, D.W, D.B1, D.C
OUT = HERE / "output"
EPISODES = 30_000


def make(kind, seed):
    return V.VIN(seed, 30, "max", plus=(kind == "Vp"))


def map_run(net, lay):
    """The map read-out: each move goes to the open neighbour with the highest learned value v (no action head)."""
    env = W.Env(lay)
    net.reset()
    while not env.done:
        net.step(env.obs())
        v = net.fw[3].max(1)
        best, bv = 4, -np.inf
        for a, (dx, dy) in enumerate(W.MOVES[:4]):
            x, y = env.pos[0] + dx, env.pos[1] + dy
            if not W.blocked(env.walls, x, y) and v[y * W.N + x] > bv:
                best, bv = a, v[y * W.N + x]
        env.step(best)
    ok = env.pos == env.goal
    return {"detour": lay["detour"], "family": lay["family"], "solved": ok,
            "efficient": ok and env.t <= W.EFF * lay["shortest"]}


def head_diagnostics(net, lay):
    """With the trained head (arg-max): per step, does it shorten the true BFS distance, and the gap between the two best
    action scores."""
    env = W.Env(lay)
    net.reset()
    good, gaps = [], []
    while not env.done:
        z = net.step(env.obs())[2]
        a = int(np.argmax(z))
        top = np.sort(z)[::-1]
        gaps.append(float(top[0] - top[1]))
        before = W.shortest(env.walls, env.pos, env.goal)[0]
        env.step(a)
        after = W.shortest(env.walls, env.pos, env.goal)[0]
        good.append(after is not None and before is not None and after == before - 1)
    return good, gaps


def learn(kind, seed, episodes=None):
    episodes = episodes or EPISODES
    d, pr = W.load(), C.load_probes()
    mv = json.loads((HERE.parent / "W1d" / "moving.json").read_text())["items"]
    rng = np.random.default_rng([seed, 1])
    net = make(kind, [seed, 2])
    for ep in range(episodes):
        lay = d["learn"][int(rng.integers(len(d["learn"])))]
        B1.episode_imit(net, W.Env(lay), lay)
    res = {"brain": kind, "seed": seed, "episodes": episodes,
           "test": [D.run(net, l) for l in d["test"]],
           "empty": [D.run(net, l) for l in pr["empty"]],
           "held": [D.run(net, l) for l in pr["held"]],
           "moving": [D.run(net, d["test"][m["k"]], m) for m in mv],
           "value_corr": float(np.mean([D.value_map_corr(net, l) for l in d["test"]])),
           "map_readout": [map_run(net, l) for l in d["test"]]}
    good, gaps = [], []
    for l in d["test"]:
        if l["detour"]:
            g, gp = head_diagnostics(net, l)
            good += g
            gaps += gp
    res["step_accuracy"] = float(np.mean(good))
    res["gap_mean"] = float(np.mean(gaps))
    res["near_tie_share"] = float(np.mean(np.array(gaps) < 0.05))
    OUT.mkdir(exist_ok=True)
    tag = "" if episodes == EPISODES else f"_{episodes // 1000}k"
    (OUT / f"{kind}{tag}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    det = [r for r in res["test"] if r["detour"]]
    mdet = [r for r in res["map_readout"] if r["detour"]]
    print(kind, seed, episodes, "eff detour", round(np.mean([r["efficient"] for r in det]), 3), "map read-out",
          round(np.mean([r["efficient"] for r in mdet]), 3), flush=True)


def checks():
    lines, ok = [], True
    d = W.load()
    # the plus mask: diagonals start and stay at 0; V (no mask) is W1d's VIN unchanged
    net = make("Vp", [1, 2])
    lay = d["learn"][0]
    B1.episode_imit(net, W.Env(lay), lay)
    diag = net.p["Wv"][:, :, [0, 0, 2, 2], [0, 2, 0, 2]]
    good = bool(np.all(diag == 0.0)) and bool(np.all(net.p["Wv"][:, :, 1, 1] != 0.0))
    ok &= good
    lines.append(f"V+: the diagonal propagation weights start and stay 0 after learning: {'yes' if good else 'NO'}")
    a, b = make("V", [3, 2]), V.VIN([3, 2], 30)
    good = all(np.array_equal(a.p[k], b.p[k]) for k in a.p)
    ok &= good
    lines.append(f"V is W1d's VIN unchanged (same start weights): {'yes' if good else 'NO'}")
    # gradient check for V+ (nudges flipping a max skipped; diagonal entries excluded, they are fixed)
    rng = np.random.default_rng(6)
    net = make("Vp", [3, 30])
    env = W.Env(d["learn"][6])
    _, path = W.shortest(env.walls, d["learn"][6]["start"], d["learn"][6]["goal"])
    xs = []
    for c in path[:6]:
        env.pos = c
        xs.append(env.obs())
    dl = [rng.normal(0, 1, 5) for _ in xs]
    dv = [float(rng.normal()) for _ in xs]

    def loss():
        net.reset()
        return sum(float(dl[t] @ net.step(x)[2]) + dv[t] * net.step(x)[3] * 0 for t, x in enumerate(xs)) + \
            sum(dv[t] * net.step(x)[3] for t, x in enumerate(xs))
    def ams():
        net.reset()
        net.step(xs[0])
        return b"".join(np.asarray(a).tobytes() for _, a in net.fw[2])
    net.reset()
    hs = [net.step(x)[1] for x in xs]
    g = net.backward(xs, None, hs, dl, dv)
    worst, flips = 0.0, 0
    for name, P in net.p.items():
        f, gf = P.reshape(-1), g[name].reshape(-1)
        idx = [i for i in range(f.size) if not (name == "Wv" and net.mask.reshape(-1)[i] == 0)]
        for i in rng.choice(idx, min(15, len(idx)), replace=False):
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
    lines.append(f"V+ gradients equal finite differences: {'yes' if good else 'NO'} (worst rel. {worst:.1e}; "
                 f"{flips} nudges skipped for flipping a max)")
    # the same seed twice
    global EPISODES
    keep, EPISODES = EPISODES, 40
    outs = []
    for _ in range(2):
        with contextlib.redirect_stdout(io.StringIO()):
            learn("Vp", 99)
        outs.append((OUT / "Vp_seed_99.json").read_text())
    (OUT / "Vp_seed_99.json").unlink()
    EPISODES = keep
    same = outs[0] == outs[1]
    ok &= same
    lines.append(f"the same seed gives the same result twice (V+, 40 episodes): {'yes' if same else 'NO'}")
    lines.append(f"All: {'PASS' if ok else 'FAIL'}")
    (HERE / "checks.log").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "checks":
        checks()
    elif cmd == "learn":
        learn(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else None)
