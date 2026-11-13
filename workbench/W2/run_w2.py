"""W2 runner (questions.md, W2-frozen).

  python workbench/W2/run_w2.py controls             # scripted brains on every set -> output/controls.json
  python workbench/W2/run_w2.py checks               # -> checks.log
  python workbench/W2/run_w2.py learn M|M0|R SEED [EPISODES]
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
import world2 as W2  # noqa: E402
import brains2 as BR  # noqa: E402
import run_w1c as C  # noqa: E402  (the empty rooms)

W, N, MOVES = W2.W, W2.N, W2.MOVES
OUT = HERE / "output"
EPISODES = 150_000
TEACHER = {"M": "Bp", "M0": "B0", "R": "Bp"}


def make(kind, seed):
    return BR.RNet(seed) if kind == "R" else BR.MapVIN(seed)


def mem_tour(lay):
    return W2.tour_mem(lay, lay["tour"])


# --- a learned brain's inputs ------------------------------------------------------------------------------------------
class Senses:
    """What each learned brain gets per step. M: the remembered map; M0: the current view as a map; R: r_input."""

    def __init__(self, kind, lay, mem0):
        self.kind, self.lay = kind, lay
        self.mem = mem0.copy() if mem0 is not None else W2.Mem()

    def get(self, pos):
        walls, goal = self.lay["walls"], self.lay["goal"]
        if self.kind == "R":
            return BR.r_input(walls, pos, goal)
        if self.kind == "M0":
            return W2.view_mem(walls, pos).channels(goal)
        self.mem.see(walls, pos)
        return self.mem.channels(goal)


def r_tour(net, lay, cells):
    """R steps through the tour (no food: the food's part of its input is zero)."""
    for c in cells:
        x = BR.r_input(lay["walls"], c, c)
        x[31:] = 0.0
        net.step(x)


def act(kind, net, x, pos):
    z = net.step(x)[2] if kind == "R" else net.step(x, pos[1] * N + pos[0])[2]
    return int(np.argmax(z))


def run_learned(kind, net, lay, mem0=None, cells=None):
    """One test episode, arg-max. mem0: the map after the tour (M); cells: the tour (R steps through it)."""
    env = W.Env(lay)
    net.reset()
    if kind == "R" and cells:
        r_tour(net, lay, cells)
    s = Senses(kind, lay, mem0 if kind == "M" else None)
    path = [env.pos]
    while not env.done:
        env.step(act(kind, net, s.get(env.pos), env.pos))
        path.append(env.pos)
    ok = env.pos == env.goal
    return {"solved": ok, "steps": env.t, "efficient": ok and env.t <= W2.EFF * lay["shortest"], "path": path}


# --- learning ----------------------------------------------------------------------------------------------------------
def episode(kind, net, lay, rng):
    """One imitation episode: new or familiar (equal chance, a fresh tour); the teacher acts, the brain is taught at
    every state the teacher visits."""
    cells = W2.tour(lay, rng) if rng.random() < 0.5 else None
    mem0 = W2.tour_mem(lay, cells) if cells else None
    teacher = W2.MapBFS(TEACHER[kind])
    env = W.Env(lay)
    teacher.reset(env, mem0)
    s = Senses(kind, lay, mem0 if kind == "M" else None)
    xs, poss, acts = [], [], []
    while not env.done:
        a = teacher.act(env)
        xs.append(s.get(env.pos))
        poss.append(env.pos[1] * N + env.pos[0])
        acts.append(a)
        env.step(a)
    if kind == "R":
        net.reset()
        if cells:
            r_tour(net, lay, cells)
        hps, hs, dl = [], [], []
        for x, a in zip(xs, acts):
            hp, h, z, _ = net.step(x)
            d = BR.B1.softmax(z)
            d[a] -= 1.0
            hps.append(hp); hs.append(h); dl.append(d)
        net.apply(net.backward(xs, hps, hs, dl, [0.0] * len(xs)))
    else:
        net.imitate(np.stack(xs), poss, acts)


def shuffle_partner(dets):
    """For each detour layout, the other detour layout with the nearest wall count (ties: lower index)."""
    n = [len(l["walls"]) for l in dets]
    return [min((j for j in range(len(dets)) if j != i), key=lambda j: (abs(n[j] - n[i]), j)) for i in range(len(dets))]


def side_ok(lay, path):
    """1 if the first sideways move (across the start-food axis) goes toward the gap, else 0 (also if none)."""
    k = 0 if lay["axis"] == "x" else 1
    for a, b in zip(path, path[1:]):
        if a[k] != b[k]:
            return int(abs(b[k] - lay["gap"][k]) < abs(a[k] - lay["gap"][k]))
    return 0


def value_corr(net, lay):
    m = W2.Mem()
    m.known[:] = True
    for x, y in lay["walls"]:
        m.wall[y, x] = True
    q = net.plan(m.channels(lay["goal"])[None])[4]
    v = q.max(1)
    xs, ys = [], []
    for x in range(N):
        for y in range(N):
            if (x, y) in lay["walls"]:
                continue
            dd = W.shortest(lay["walls"], (x, y), lay["goal"])[0]
            if dd is not None:
                xs.append(v[y * N + x])
                ys.append(-dd)
    rx, ry = np.argsort(np.argsort(xs)), np.argsort(np.argsort(ys))
    return float(np.corrcoef(rx, ry)[0, 1])


def strip(r):
    return {k: v for k, v in r.items() if k != "path"}


def evaluate(kind, net, d, empty):
    res = {}
    for name in ("detour", "control"):
        lays = d[name]
        res[name + "_new"] = [strip(run_learned(kind, net, l)) for l in lays]
        res[name + "_fam"] = [strip(run_learned(kind, net, l, mem_tour(l), l["tour"])) for l in lays]
    res["empty"] = [strip(run_learned(kind, net, l)) for l in empty]
    res["pairs"] = [[side_ok(l, run_learned(kind, net, l, mem_tour(l), l["tour"])["path"]) for l in pr]
                    for pr in d["pairs"]]
    if kind == "M":
        part = shuffle_partner(d["detour"])
        res["detour_erase"] = [strip(run_learned(kind, net, l, W2.Mem())) for l in d["detour"]]
        res["detour_shuffle"] = [strip(run_learned(kind, net, l, mem_tour(d["detour"][j])))
                                 for l, j in zip(d["detour"], part)]
    if kind in ("M", "M0"):
        res["value_corr"] = float(np.mean([value_corr(net, l) for l in d["detour"]]))
    return res


def learn(kind, seed, episodes=None):
    episodes = episodes or EPISODES
    d = W2.load()
    empty = C.load_probes()["empty"]
    rng = np.random.default_rng([seed, 1])
    net = make(kind, [seed, 2])
    for _ in range(episodes):
        episode(kind, net, d["learn"][int(rng.integers(len(d["learn"])))], rng)
    res = {"brain": kind, "seed": seed, "episodes": episodes, **evaluate(kind, net, d, empty)}
    OUT.mkdir(exist_ok=True)
    tag = "" if episodes == EPISODES else f"_{episodes // 1000}k" if episodes >= 1000 else f"_{episodes}ep"
    (OUT / f"{kind}{tag}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    print(kind, seed, episodes, "eff detour new/fam",
          round(np.mean([r["efficient"] for r in res["detour_new"]]), 3),
          round(np.mean([r["efficient"] for r in res["detour_fam"]]), 3),
          "pairs", round(float(np.mean(res["pairs"])), 3), flush=True)


def controls():
    d = W2.load()
    empty = C.load_probes()["empty"]
    out = {}
    for name, b in W2.controls().items():
        r = {}
        for s in ("detour", "control"):
            r[s + "_new"] = [strip(W2.run(b, l)) for l in d[s]]
            r[s + "_fam"] = [strip(W2.run(b, l, mem_tour(l))) for l in d[s]]
        r["empty"] = [strip(W2.run(b, l)) for l in empty]
        r["pairs"] = [[side_ok(l, W2.run(b, l, mem_tour(l))["path"]) for l in pr] for pr in d["pairs"]]
        out[name] = r
        print(name, "eff detour new/fam", round(np.mean([x["efficient"] for x in r["detour_new"]]), 3),
              round(np.mean([x["efficient"] for x in r["detour_fam"]]), 3), "pairs",
              round(float(np.mean(r["pairs"])), 3))
    OUT.mkdir(exist_ok=True)
    (OUT / "controls.json").write_text(json.dumps(out), encoding="utf-8")


# --- checks ------------------------------------------------------------------------------------------------------------
def checks():
    lines, ok = [], True

    def say(text, good):
        nonlocal ok
        ok &= bool(good)
        lines.append(f"{text}: {'yes' if good else 'NO'}")

    d = W2.load()
    rng = np.random.default_rng(7)
    # the batched planner equals planning one map at a time
    net = BR.MapVIN([1, 2])
    maps = np.stack([W2.view_mem(d["learn"][i]["walls"], d["learn"][i]["start"]).channels(d["learn"][i]["goal"])
                     for i in range(5)])
    qb = net.plan(maps)[4].reshape(5, N * N, -1)
    say("the batched planner equals one map at a time",
        all(np.allclose(qb[t], net.plan(maps[t:t + 1])[4]) for t in range(5)))
    # the plus mask holds after learning
    lay = d["learn"][0]
    for _ in range(3):
        episode("M", net, lay, rng)
    say("V+'s diagonal propagation weights stay 0", np.all(net.p["Wv"][:, :, [0, 0, 2, 2], [0, 2, 0, 2]] == 0))
    # gradient checks
    for kind in ("M", "R"):
        net = make(kind, [3, 30])
        lay = d["learn"][6]
        cells = W2.tour(lay, np.random.default_rng(1))
        mem0 = W2.tour_mem(lay, cells)
        env = W.Env(lay)
        t = W2.MapBFS("Bp")
        t.reset(env, mem0)
        s = Senses(kind, lay, mem0 if kind == "M" else None)
        xs, poss = [], []
        for _ in range(6):
            xs.append(s.get(env.pos))
            poss.append(env.pos[1] * N + env.pos[0])
            env.step(t.act(env))
        dl = [rng.normal(0, 1, 5) for _ in xs]
        dv = [float(rng.normal()) for _ in xs]
        if kind == "M":
            mp = np.stack(xs)

            def loss():
                fw = net.plan(mp)
                qa = fw[4][np.arange(6) * N * N + np.asarray(poss)]
                return float(sum(dl[i] @ (net.p["Wo"] @ qa[i] + net.p["bo"]) + dv[i] * (net.p["wv"] @ qa[i] +
                                                                                       net.p["bv"][0]) for i in range(6)))

            def sig():
                return b"".join(np.asarray(am).tobytes() for _, am in net.plan(mp)[3])
            g = net.backprop(net.plan(mp), poss, dl, dv)
        else:
            def run_r():                         # no tour here: learning does not backprop into the tour
                net.reset()
                return [net.step(x) for x in xs]

            def loss():
                return float(sum(dl[i] @ o[2] + dv[i] * o[3] for i, o in enumerate(run_r())))

            def sig():
                return b""
            outs = run_r()
            # full backprop through the 6 steps (they are within one 16-step window)
            g = net.backward(xs, [o[0] for o in outs], [o[1] for o in outs], dl, dv)
        worst, flips = 0.0, 0
        for name, P in net.p.items():
            f, gf = P.reshape(-1), g[name].reshape(-1)
            idx = [i for i in range(f.size) if not (kind == "M" and name == "Wv" and net.mask.reshape(-1)[i] == 0)]
            for i in rng.choice(idx, min(12, len(idx)), replace=False):
                o, base = f[i], sig()
                f[i] = o + 1e-6
                lp, s1 = loss(), sig()
                f[i] = o - 1e-6
                lm, s2 = loss(), sig()
                f[i] = o
                if s1 != base or s2 != base:
                    flips += 1
                    continue
                num = (lp - lm) / 2e-6
                worst = max(worst, abs(num - gf[i]) / max(1e-3, abs(num) + abs(gf[i])))
        say(f"{kind}: gradients equal finite differences (worst rel. {worst:.1e}; {flips} max flips skipped)",
            worst < 1e-3)
    # the sets
    tours_ok = True
    for lay in d["detour"] + d["control"] + [l for pr in d["pairs"] for l in pr]:
        s = lay["start"]
        opens = [(x, y) for x in range(N) for y in range(N) if (x, y) not in lay["walls"]]
        m = mem_tour(lay)
        cov = sum(m.known[y, x] for x, y in opens) / len(opens)
        near = any(max(abs(c[0] - s[0]), abs(c[1] - s[1])) <= 1 for c in lay["tour"])
        steps_ok = all(W.manhattan(a, b) == 1 for a, b in zip(lay["tour"], lay["tour"][1:]))
        tours_ok &= (cov >= W2.COVER - 1e-9 or "must_see" in lay) and not near and steps_ok
    say("every tour covers 60% of the open cells, never enters the start's 3 x 3, and moves one cell at a time",
        tours_ok)
    ctl = W2.controls()
    say("every test detour: B0, H2, W2 fail it in a new room; Bp is efficient in the familiar room",
        all(not any(W2.run(ctl[b], l)["efficient"] for b in ("B0", "H2", "W2")) and
            W2.run(ctl["Bp"], l, mem_tour(l))["efficient"] for l in d["detour"]))
    look = all(W2.view_mem(a["walls"], a["start"]).channels(a["goal"]).tobytes() ==
               W2.view_mem(b["walls"], b["start"]).channels(b["goal"]).tobytes() and
               a["start"] == b["start"] and a["goal"] == b["goal"] and a["gap"] != b["gap"] and
               mem_tour(a).known[a["gap"][1], a["gap"][0]] and mem_tour(b).known[b["gap"][1], b["gap"][0]]
               for a, b in d["pairs"])
    say("look-alike pairs: the same start, food and view; different gaps; each tour sees its gap", look)
    say("M-shuffle partners are other layouts", all(j != i for i, j in enumerate(shuffle_partner(d["detour"]))))
    # the same seed twice
    global EPISODES
    keep, EPISODES = EPISODES, 30
    for kind in ("M", "M0", "R"):
        outs = []
        for _ in range(2):
            with contextlib.redirect_stdout(io.StringIO()):
                learn(kind, 99)
            outs.append((OUT / f"{kind}_seed_99.json").read_text())
        (OUT / f"{kind}_seed_99.json").unlink()
        say(f"{kind}: the same seed gives the same result twice (30 episodes)", outs[0] == outs[1])
    EPISODES = keep
    lines.append(f"All: {'PASS' if ok else 'FAIL'}")
    (HERE / "checks.log").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "checks":
        checks()
    elif cmd == "controls":
        controls()
    elif cmd == "learn":
        learn(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else None)
