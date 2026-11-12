"""W1 runner (questions.md, W1-frozen).

  python workbench/W1/run_w1.py checks                 # code checks -> checks.log (before any run)
  python workbench/W1/run_w1.py scripted               # G, W, B, M, M- on the test layouts
  python workbench/W1/run_w1.py learn F|R|Fimit SEED   # train 30,000 episodes, then test
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import brains as B  # noqa: E402
from world import Env, load, shortest  # noqa: E402

EPISODES = 30_000
OUT = HERE / "output"
SEEDS = list(range(1, 17))


def run_test(brain, layouts):
    rows = []
    for k, lay in enumerate(layouts):
        env = Env(lay)
        brain.reset(env)
        while not env.done:
            env.step(brain.act(env))
        rows.append({"k": k, "set": lay["set"], "detour": lay["detour"], "solved": env.pos == env.goal,
                     "steps": env.t, "shortest": lay["shortest"]})
    return rows


def save(name, seed, rows, extra=None):
    OUT.mkdir(exist_ok=True)
    (OUT / f"{name}_seed_{seed}.json").write_text(json.dumps({"brain": name, "seed": seed, "rows": rows,
                                                              **(extra or {})}), encoding="utf-8")


def scripted():
    d = load()
    for brain in (B.Greedy(), B.WallFollower(), B.Planner(), B.MapPlanner(True), B.MapPlanner(False)):
        rows = run_test(brain, d["test"])
        save(brain.name.replace("-", "m"), 0, rows)
        det = [r for r in rows if r["detour"]]
        print(brain.name, "detour success", round(np.mean([r["solved"] for r in det]), 3), flush=True)


def learn(kind, seed):
    d = load()
    rng = np.random.default_rng([seed, 1])
    net = B.Net([seed, 2], recurrent=(kind == "R"))
    curve = []
    ok = []
    for ep in range(EPISODES):
        lay = d["learn"][int(rng.integers(len(d["learn"])))]
        env = Env(lay)
        if kind == "Fimit":
            B.episode_imit(net, env, lay)
        else:
            ok.append(B.episode_ac(net, env, rng))
        if (ep + 1) % 3000 == 0:
            curve.append({"episode": ep + 1, "train_success": float(np.mean(ok[-3000:])) if ok else None})
    rows = run_test(B.Learned(kind, net), d["test"])
    save(kind, seed, rows, {"curve": curve})
    det = [r for r in rows if r["detour"]]
    con = [r for r in rows if not r["detour"]]
    print(kind, seed, "detour", round(np.mean([r["solved"] for r in det]), 3), "control",
          round(np.mean([r["solved"] for r in con]), 3), flush=True)


def checks():
    lines, ok = [], True
    d = load()
    # 1. the layouts are what they say they are
    from world import is_detour
    good = all(is_detour(l["walls"], l["start"], l["goal"]) == l["detour"] and
               shortest(l["walls"], l["start"], l["goal"])[0] == l["shortest"] <= 30 for l in d["learn"] + d["test"])
    ok &= good
    lines.append(f"every layout's detour/control label and shortest path recomputed: {'yes' if good else 'NO'}")
    # 2. learning and test layouts do not overlap
    key = lambda l: (tuple(sorted(l["walls"])), l["start"], l["goal"])  # noqa: E731
    disjoint = not ({key(l) for l in d["learn"]} & {key(l) for l in d["test"]})
    ok &= disjoint
    lines.append(f"no test layout is a learning layout: {'yes' if disjoint else 'NO'}")
    # 3. B solves every test layout on its shortest path
    rows = run_test(B.Planner(), d["test"])
    bb = all(r["solved"] and r["steps"] == r["shortest"] for r in rows)
    ok &= bb
    lines.append(f"B solves every test layout in exactly its shortest path: {'yes' if bb else 'NO'}")
    # 4. gradients equal finite differences (F and R, actor-critic and imitation losses)
    rng = np.random.default_rng(5)
    for rec in (False, True):
        net = B.Net([9, 9], rec)
        for k in net.p:
            net.p[k] = net.p[k] * 5
        T = 20
        xs = [rng.normal(0, 1, 52) for _ in range(T)]
        dlc = [rng.normal(0, 1, 5) for _ in range(T)]       # a random linear loss on logits and values
        dvc = [float(rng.normal()) for _ in range(T)]

        def loss():
            net.reset()
            tot = 0.0
            for t in range(T):
                _, h, z, v = net.step(xs[t])
                tot += float(dlc[t] @ z) + dvc[t] * v
            return tot
        net.reset()
        hps, hs = [], []
        for t in range(T):
            hp, h, z, v = net.step(xs[t])
            hps.append(hp); hs.append(h)
        g = net.backward(xs, hps, hs, dlc, dvc)
        worst = 0.0
        for name, P in net.p.items():
            flat, gf = P.reshape(-1), g[name].reshape(-1)
            for i in rng.choice(flat.size, min(10, flat.size), replace=False):
                old = flat[i]
                flat[i] = old + 1e-6
                lp = loss()
                flat[i] = old - 1e-6
                lm = loss()
                flat[i] = old
                num = (lp - lm) / 2e-6
                worst = max(worst, abs(num - gf[i]) / max(1e-3, abs(num) + abs(gf[i])))
        # with truncation, R's gradient is the truncated one: compare only within the first 16 steps' reach
        good = worst < 1e-4 if not rec else True
        if rec:
            B.TRUNC, keep = 10 ** 9, B.TRUNC
            g2 = net.backward(xs, hps, hs, dlc, dvc)
            worst = 0.0
            for name, P in net.p.items():
                flat, gf = P.reshape(-1), g2[name].reshape(-1)
                for i in rng.choice(flat.size, min(10, flat.size), replace=False):
                    old = flat[i]
                    flat[i] = old + 1e-6
                    lp = loss()
                    flat[i] = old - 1e-6
                    lm = loss()
                    flat[i] = old
                    num = (lp - lm) / 2e-6
                    worst = max(worst, abs(num - gf[i]) / max(1e-3, abs(num) + abs(gf[i])))
            B.TRUNC = keep
            good = worst < 1e-4
        ok &= good
        lines.append(f"gradients equal finite differences, {'R (untruncated)' if rec else 'F'}: "
                     f"{'yes' if good else 'NO'} (worst rel. {worst:.1e})")
    # 5. the actor-critic logit gradient (policy term and entropy bonus) equals finite differences of its loss
    z0, a, adv = rng.normal(0, 1, 5), 2, 0.7

    def ac_loss(z):
        pi = B.softmax(z)
        return -adv * np.log(pi[a]) - B.ENT * float(-(pi * np.log(pi)).sum())
    pi = B.softmax(z0)
    d = pi.copy()
    d[a] -= 1.0
    d *= adv
    logp = np.log(pi)
    d += B.ENT * (pi * (logp + 1.0) - pi * float(pi @ (logp + 1.0)))
    num = np.array([(ac_loss(z0 + 1e-6 * np.eye(5)[i]) - ac_loss(z0 - 1e-6 * np.eye(5)[i])) / 2e-6 for i in range(5)])
    good = bool(np.allclose(num, d, atol=1e-6))
    ok &= good
    lines.append(f"the actor-critic logit gradient (policy and entropy terms) equals finite differences: "
                 f"{'yes' if good else 'NO'}")
    # 6. the same seed gives the same result twice
    global EPISODES
    keep, EPISODES = EPISODES, 300
    import io
    import contextlib
    outs = []
    for _ in range(2):
        with contextlib.redirect_stdout(io.StringIO()):
            learn("R", 99)
        outs.append((OUT / "R_seed_99.json").read_text())
    (OUT / "R_seed_99.json").unlink()
    EPISODES = keep
    same = outs[0] == outs[1]
    ok &= same
    lines.append(f"the same seed gives the same result twice (R, 300 episodes): {'yes' if same else 'NO'}")
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
