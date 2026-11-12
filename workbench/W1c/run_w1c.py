"""W1c runner (questions.md, W1c-frozen).

  python workbench/W1c/run_w1c.py probes                       # empty rooms + held-out topologies -> probes.json
  python workbench/W1c/run_w1c.py checks                       # -> checks.log
  python workbench/W1c/run_w1c.py learn E|Eimit|C|Cimit|Cdag SEED [EPISODES]
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
import nets_c as N  # noqa: E402

B1, W = N.B1, N.W
OUT = HERE / "output"
EPISODES = 30_000
PROBE_SEED = 20261118


# --- probe sets ------------------------------------------------------------------------------------------------------
def zigzag(rng):
    return [(i, 0) for i in range(5)] + [(4, 1), (4, 2)] + [(i, 2) for i in range(5, 9)]


def hook(rng):
    b, a = int(rng.integers(5, 8)), 3
    return W.cup(rng, b, a) + [(1, -a)]


def comb(rng):
    n = 7
    return [(i, 0) for i in range(n)] + [(x, y) for x in (1, 3, 5) for y in (1, 2)]


HELD = {"zigzag": zigzag, "hook": hook, "comb": comb}


def draw_held(rng, want_detour):
    names = list(HELD)
    fam = names[int(rng.integers(len(names)))]
    for _ in range(50000):
        walls = W.place(rng, HELD[fam])
        if walls is None:
            continue
        cells = [(x, y) for x in range(W.N) for y in range(W.N) if (x, y) not in walls]
        s, g = cells[int(rng.integers(len(cells)))], cells[int(rng.integers(len(cells)))]
        if W.manhattan(s, g) < 4:
            continue
        d, _ = W.shortest(walls, s, g)
        if d is None or d > 30 or W.is_detour(walls, s, g) != want_detour:
            continue
        return {"family": fam, "walls": walls, "start": s, "goal": g, "detour": want_detour, "shortest": d}
    raise RuntimeError("could not draw")


def build_probes():
    rng = np.random.default_rng(PROBE_SEED)
    empty = []
    cells = [(x, y) for x in range(W.N) for y in range(W.N)]
    while len(empty) < 60:
        s, g = cells[int(rng.integers(len(cells)))], cells[int(rng.integers(len(cells)))]
        if W.manhattan(s, g) >= 4:
            empty.append({"family": "empty", "walls": set(), "start": s, "goal": g, "detour": False,
                          "shortest": W.manhattan(s, g), "set": "empty"})
    held = ([dict(draw_held(rng, True), set="held_detour") for _ in range(60)] +
            [dict(draw_held(rng, False), set="held_control") for _ in range(60)])
    out = {"seed": PROBE_SEED, "empty": [W.to_json(l) for l in empty], "held": [W.to_json(l) for l in held]}
    (HERE / "probes.json").write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    print("empty", len(empty), "held", len(held))


def load_probes():
    d = json.loads((HERE / "probes.json").read_text(encoding="utf-8"))
    for lay in d["empty"] + d["held"]:
        lay["walls"] = {tuple(c) for c in lay["walls"]}
        lay["start"], lay["goal"] = tuple(lay["start"]), tuple(lay["goal"])
    return d


# --- brains ----------------------------------------------------------------------------------------------------------
def make_net(kind, seed):
    return N.ConvNet(seed) if kind.startswith("C") else N.FlatNet(seed)


class Learned:
    def __init__(self, net):
        self.net = net

    def reset(self, env):
        self.net.reset()

    def act(self, env):
        out = int(np.argmax(self.net.step(env.obs())[2]))
        if hasattr(self.net, "cache"):
            self.net.cache.clear()                  # testing: no backward pass, keep no cache
        return out


def b_move(walls, pos, goal):
    _, path = W.shortest(walls, pos, goal)
    if path is None or len(path) < 2:
        return 4
    nxt = path[1]
    return W.MOVES.index((nxt[0] - pos[0], nxt[1] - pos[1]))


def episode_dagger(net, lay, rng):
    """DAgger: walk the layout with B's move (chance 1/2) or the net's own best move; label every visited state with
    B's move from there; one cross-entropy update per episode."""
    env = N.EgoEnv(lay)
    net.reset()
    xs, hs, dl = [], [], []
    while not env.done:
        x = env.obs()
        _, h, z, _ = net.step(x)
        a_b = b_move(env.walls, env.pos, env.goal)
        d = B1.softmax(z)
        d[a_b] -= 1.0
        xs.append(x); hs.append(h); dl.append(d)
        env.step(a_b if rng.random() < 0.5 else int(np.argmax(z)))
    net.apply(net.backward(xs, [None] * len(xs), hs, dl, [0.0] * len(xs)))


def run_one(net, lay):
    env = N.EgoEnv(lay)
    brain = Learned(net)
    brain.reset(env)
    path = [env.pos]
    while not env.done:
        env.step(brain.act(env))
        path.append(env.pos)
    ok = env.pos == env.goal
    return {"set": lay.get("set"), "family": lay["family"], "detour": lay["detour"], "solved": ok, "steps": env.t,
            "shortest": lay["shortest"], "efficient": ok and env.t <= W.EFF * lay["shortest"],
            "first3": first3(lay, path) if lay["detour"] else None}


def first3(lay, path):
    if len(path) < 4:
        return False
    for a, b in zip(path[:3], path[1:4]):
        da, db = W.shortest(lay["walls"], a, lay["goal"])[0], W.shortest(lay["walls"], b, lay["goal"])[0]
        if da is None or db is None or db != da - 1:
            return False
    return True


def imitation_accuracy(net, lays):
    ok = n = 0
    for lay in lays:
        _, path = W.shortest(lay["walls"], lay["start"], lay["goal"])
        env = N.EgoEnv(lay)
        net.reset()
        for c, nx in zip(path[:-1], path[1:]):
            env.pos = c
            z = net.step(env.obs())[2]
            ok += int(np.argmax(z) == W.MOVES.index((nx[0] - c[0], nx[1] - c[1])))
            n += 1
        net.reset()
    return ok / n


def learn(kind, seed, episodes=None):
    episodes = episodes or EPISODES
    d, pr = W.load(), load_probes()
    rng = np.random.default_rng([seed, 1])
    net = make_net(kind, [seed, 2])
    ok, curve = [], []
    for ep in range(episodes):
        lay = d["learn"][int(rng.integers(len(d["learn"])))]
        if kind in ("E", "C"):
            ok.append(B1.episode_ac(net, N.EgoEnv(lay), rng))
        elif kind in ("Eimit", "Cimit"):
            B1.episode_imit(net, N.EgoEnv(lay), lay)
        else:
            episode_dagger(net, lay, rng)
        if (ep + 1) % 3000 == 0:
            curve.append({"episode": ep + 1, "train_success": float(np.mean(ok[-3000:])) if ok else None})
    res = {"brain": kind, "seed": seed, "episodes": episodes, "curve": curve,
           "test": [run_one(net, l) for l in d["test"]],
           "empty": [run_one(net, l) for l in pr["empty"]],
           "held": [run_one(net, l) for l in pr["held"]],
           "imit_acc_learn": imitation_accuracy(net, d["learn"][:100]),
           "imit_acc_test": imitation_accuracy(net, d["test"][:100])}
    OUT.mkdir(exist_ok=True)
    tag = "" if episodes == EPISODES else f"_{episodes // 1000}k"
    (OUT / f"{kind}{tag}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    det = [r for r in res["test"] if r["detour"]]
    con = [r for r in res["test"] if not r["detour"]]
    print(kind, seed, episodes, "control", round(np.mean([r["solved"] for r in con]), 3), "eff detour",
          round(np.mean([r["efficient"] for r in det]), 3), "empty", round(np.mean([r["solved"] for r in
                                                                                     res["empty"]]), 3), flush=True)


# --- checks ----------------------------------------------------------------------------------------------------------
def checks():
    lines, ok = [], True
    d, pr = W.load(), load_probes()
    # egocentric view: the agent at the centre; food where it is; outside the area is wall
    lay = d["test"][0]
    env = N.EgoEnv(lay)
    o = env.obs().reshape(2, N.S, N.S)
    gx, gy = lay["goal"][0] - lay["start"][0] + N.R, lay["goal"][1] - lay["start"][1] + N.R
    corner = o[0, 0, 0] if lay["start"] == (0, 0) else o[0, N.R - lay["start"][1] - 1, N.R]
    good = o[1, gy, gx] == 1.0 and o[1].sum() == 1.0 and \
        all(o[0, j, i] == (1.0 if W.blocked(lay["walls"], lay["start"][0] + i - N.R, lay["start"][1] + j - N.R) else 0.0)
            for j in range(N.S) for i in range(N.S))
    ok &= good
    lines.append(f"egocentric view: food in place, walls and the outside as walls, agent centred: {'yes' if good else 'NO'}")
    # probes: labels, solvable, disjoint from learning
    key = lambda l: (tuple(sorted(l["walls"])), l["start"], l["goal"])  # noqa: E731
    good = all(W.is_detour(l["walls"], l["start"], l["goal"]) == l["detour"] and
               W.shortest(l["walls"], l["start"], l["goal"])[0] == l["shortest"] for l in pr["empty"] + pr["held"])
    good &= not ({key(l) for l in pr["held"]} & {key(l) for l in d["learn"]})
    good &= all(l["family"] in HELD for l in pr["held"])
    ok &= good
    lines.append(f"probe sets: labels and shortest paths recomputed, held-out families not in learning: "
                 f"{'yes' if good else 'NO'}")
    # gradients, conv (3 layers) and flat (882 -> 64)
    rng = np.random.default_rng(3)
    for kind in ("C", "E"):
        net = make_net(kind, [1, 2])
        for k in net.p:
            if k.startswith("b"):
                net.p[k] = rng.normal(0, 0.1, net.p[k].shape)
        T = 3
        xs = [(rng.random(N.S * N.S * 2) < 0.3).astype(float) for _ in range(T)]
        dlc = [rng.normal(0, 1, 5) for _ in range(T)]
        dvc = [float(rng.normal()) for _ in range(T)]

        def loss():
            net.reset()
            tot = 0.0
            for t in range(T):
                _, h, z, v = net.step(xs[t])
                tot += float(dlc[t] @ z) + dvc[t] * v
            return tot
        net.reset()
        hs = [net.step(x)[1] for x in xs]
        g = net.backward(xs, [np.zeros(N.HID)] * T, hs, dlc, dvc)
        worst = 0.0
        for name, P in net.p.items():
            flat, gf = P.reshape(-1), g[name].reshape(-1)
            for i in rng.choice(flat.size, min(15, flat.size), replace=False):
                o_ = flat[i]
                flat[i] = o_ + 1e-6
                lp = loss()
                flat[i] = o_ - 1e-6
                lm = loss()
                flat[i] = o_
                num = (lp - lm) / 2e-6
                worst = max(worst, abs(num - gf[i]) / max(1e-3, abs(num) + abs(gf[i])))
        good = worst < 1e-4
        ok &= good
        lines.append(f"gradients equal finite differences, {kind}: {'yes' if good else 'NO'} (worst rel. {worst:.1e})")
    # DAgger labels are B's moves from the visited states
    lay = d["learn"][3]
    good = True
    for x in range(W.N):
        for y in range(W.N):
            p = (x, y)
            if p in lay["walls"] or p == lay["goal"]:
                continue
            here = W.shortest(lay["walls"], p, lay["goal"])[0]
            if here is None:
                continue
            dx, dy = W.MOVES[b_move(lay["walls"], p, lay["goal"])]
            if W.shortest(lay["walls"], (x + dx, y + dy), lay["goal"])[0] != here - 1:
                good = False
    ok &= good
    lines.append(f"DAgger's label (B's move) shortens the path from every reachable cell: {'yes' if good else 'NO'}")
    # the same seed twice
    global EPISODES
    keep, EPISODES = EPISODES, 60
    outs = []
    for _ in range(2):
        with contextlib.redirect_stdout(io.StringIO()):
            learn("Cdag", 99)
        outs.append((OUT / "Cdag_seed_99.json").read_text())
    (OUT / "Cdag_seed_99.json").unlink()
    EPISODES = keep
    same = outs[0] == outs[1]
    ok &= same
    lines.append(f"the same seed gives the same result twice (C-dag, 60 episodes): {'yes' if same else 'NO'}")
    lines.append(f"All: {'PASS' if ok else 'FAIL'}")
    (HERE / "checks.log").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "probes":
        build_probes()
    elif cmd == "checks":
        checks()
    elif cmd == "learn":
        learn(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else None)
