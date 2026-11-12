"""W1b runner (questions.md, W1b-frozen). The learning code is W1's (brains.py: actor-critic, imitation), with W1b's
sizes: 363 inputs, 64 hidden units.

  python workbench/W1b/run_w1b.py checks
  python workbench/W1b/run_w1b.py scripted
  python workbench/W1b/run_w1b.py learn F|R|Fimit SEED
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
sys.path.insert(0, str(HERE.parent / "W1"))
import brains as B1  # noqa: E402  (W1's learning code)
import world_b as W  # noqa: E402

IN, HID = 363, 64
EPISODES = 30_000
OUT = HERE / "output"


class Net(B1.Net):
    """W1's network with W1b's sizes."""

    def __init__(self, seed, recurrent):
        r = np.random.default_rng(seed)
        self.rec = recurrent
        self.p = {"Wx": r.normal(0, 0.1, (HID, IN)), "b": np.zeros(HID), "Wa": r.normal(0, 0.1, (5, HID)),
                  "ba": np.zeros(5), "Wv": r.normal(0, 0.1, HID), "bv": np.zeros(1)}
        if recurrent:
            self.p["Wh"] = r.normal(0, 0.1, (HID, HID))

    def reset(self):
        self.h = np.zeros(HID)

    def backward(self, xs, hps, hs, dlogits, dvals):
        keep = B1.H
        B1.H = HID                     # W1's backward sizes its carried gradient by brains.H
        try:
            return super().backward(xs, hps, hs, dlogits, dvals)
        finally:
            B1.H = keep


def first_decision(lay, path):
    """Each of the first 3 moves shortens the true BFS distance to the food."""
    if len(path) < 4:
        return False
    for a, b in zip(path[:3], path[1:4]):
        da, _ = W.shortest(lay["walls"], a, lay["goal"])
        db, _ = W.shortest(lay["walls"], b, lay["goal"])
        if db is None or da is None or db != da - 1:
            return False
    return True


def test(brain, layouts):
    rows = []
    for k, lay in enumerate(layouts):
        ok, steps, path = W.run(brain, lay)
        rows.append({"k": k, "set": lay["set"], "family": lay["family"], "detour": lay["detour"], "solved": ok,
                     "steps": steps, "shortest": lay["shortest"],
                     "efficient": ok and steps <= W.EFF * lay["shortest"],
                     "first3": first_decision(lay, path) if lay["detour"] else None})
    return rows


def save(name, seed, rows, extra=None):
    OUT.mkdir(exist_ok=True)
    (OUT / f"{name}_seed_{seed}.json").write_text(json.dumps({"brain": name, "seed": seed, "rows": rows,
                                                              **(extra or {})}), encoding="utf-8")


class Learned:
    def __init__(self, name, net):
        self.name, self.net = name, net

    def reset(self, env):
        self.net.reset()

    def act(self, env):
        return int(np.argmax(self.net.step(env.obs())[2]))


def learn(kind, seed):
    d = W.load()
    rng = np.random.default_rng([seed, 1])
    net = Net([seed, 2], recurrent=(kind == "R"))
    ok, curve = [], []
    for ep in range(EPISODES):
        lay = d["learn"][int(rng.integers(len(d["learn"])))]
        env = W.Env(lay)
        if kind == "Fimit":
            B1.episode_imit(net, env, lay)
        else:
            ok.append(B1.episode_ac(net, env, rng))
        if (ep + 1) % 3000 == 0:
            curve.append({"episode": ep + 1, "train_success": float(np.mean(ok[-3000:])) if ok else None})
    rows = test(Learned(kind, net), d["test"])
    save(kind, seed, rows, {"curve": curve})
    det = [r for r in rows if r["detour"]]
    print(kind, seed, "efficient detour", round(np.mean([r["efficient"] for r in det]), 3), flush=True)


def scripted():
    d = W.load()
    for brain in W.controls() + [W.Planner()]:
        save(brain.name.replace("-", "m"), 0, test(brain, d["test"]))
        print(brain.name, "done", flush=True)


def checks():
    lines, ok = [], True
    d = W.load()
    good = all(W.is_detour(l["walls"], l["start"], l["goal"]) == l["detour"] and
               W.shortest(l["walls"], l["start"], l["goal"])[0] == l["shortest"] <= 30 for l in d["learn"] + d["test"])
    ok &= good
    lines.append(f"every layout's label and shortest path recomputed: {'yes' if good else 'NO'}")
    key = lambda l: (tuple(sorted(l["walls"])), l["start"], l["goal"])  # noqa: E731
    dis = not ({key(l) for l in d["learn"]} & {key(l) for l in d["test"]})
    ok &= dis
    lines.append(f"no test layout is a learning layout: {'yes' if dis else 'NO'}")
    adv = all(not all(W.efficient(b, l) for b in W.controls()[1:5]) for l in d["test"] if l["set"] == "adversarial")
    ok &= adv
    lines.append(f"every adversarial layout defeats at least one of W, W2, H1, H2: {'yes' if adv else 'NO'}")
    bb = all(W.run(W.Planner(), l)[1] == l["shortest"] for l in d["test"])
    ok &= bb
    lines.append(f"B solves every test layout on its shortest path: {'yes' if bb else 'NO'}")
    # gradients with W1b's sizes (W1's backward, F and untruncated R)
    rng = np.random.default_rng(5)
    for rec in (False, True):
        net = Net([9, 9], rec)
        for k in net.p:
            net.p[k] = net.p[k] * 3
        T = 20
        xs = [rng.normal(0, 1, IN) for _ in range(T)]
        dlc = [rng.normal(0, 1, 5) for _ in range(T)]
        dvc = [float(rng.normal()) for _ in range(T)]

        def loss2():
            net.reset()
            tot = 0.0
            for t in range(T):
                _, h, z, v = net.step(xs[t])
                tot += float(dlc[t] @ z) + dvc[t] * v
            return tot
        keep = B1.TRUNC
        B1.TRUNC = 10 ** 9
        net.reset()
        hps, hs = [], []
        for t in range(T):
            hp, h, z, v = net.step(xs[t])
            hps.append(hp); hs.append(h)
        g = net.backward(xs, hps, hs, dlc, dvc)
        B1.TRUNC = keep
        worst = 0.0
        for name, P in net.p.items():
            flat, gf = P.reshape(-1), g[name].reshape(-1)
            for i in rng.choice(flat.size, min(10, flat.size), replace=False):
                old = flat[i]
                flat[i] = old + 1e-6
                lp = loss2()
                flat[i] = old - 1e-6
                lm = loss2()
                flat[i] = old
                num = (lp - lm) / 2e-6
                worst = max(worst, abs(num - gf[i]) / max(1e-3, abs(num) + abs(gf[i])))
        good = worst < 1e-4
        ok &= good
        lines.append(f"gradients equal finite differences ({'R, untruncated' if rec else 'F'}, 363 -> 64): "
                     f"{'yes' if good else 'NO'} (worst rel. {worst:.1e})")
    global EPISODES
    keep, EPISODES = EPISODES, 200
    outs = []
    for _ in range(2):
        with contextlib.redirect_stdout(io.StringIO()):
            learn("R", 99)
        outs.append((OUT / "R_seed_99.json").read_text())
    (OUT / "R_seed_99.json").unlink()
    EPISODES = keep
    same = outs[0] == outs[1]
    ok &= same
    lines.append(f"the same seed gives the same result twice (R, 200 episodes): {'yes' if same else 'NO'}")
    lines.append(f"All: {'PASS' if ok else 'FAIL'}")
    (HERE / "checks.log").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "checks":
        checks()
    elif cmd == "scripted":
        scripted()
    elif cmd == "learn":
        learn(sys.argv[2], int(sys.argv[3]))
