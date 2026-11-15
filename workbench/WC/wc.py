"""WC: a world that changes (questions.md, WC-frozen). WT's p = 0.5 world (../WT/wt.py); the codes of kinds 0-2
change at the start of day 31 and of kinds 3-5 at the start of day 46, with no teacher after day 30.

  python wc.py evolve RUN [RUN ...]       (writes evo_run<RUN>.json/.log)
  python wc.py final                      (writes output/ and evolved.json)
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "WT"))
import wt  # noqa: E402
import we  # noqa: E402
import wg  # noqa: E402
import wn  # noqa: E402
import ws  # noqa: E402

HERE = Path(__file__).parent
P = 0.5
A, B = (0, 1, 2), (3, 4, 5)
CHANGE_DAY = {31: A, 46: B}
TEST_DAYS = (30, 33, 38, 45, 48, 53, 60)


def new_codes(home, seed):
    """New codes for every kind: each lid's pair differs from its old pair; the two lids of a kind differ."""
    r = np.random.default_rng([seed, 8])
    out = []
    for k in range(ws.KINDS):
        pairs = []
        for j in range(ws.LIDS):
            while True:
                q = int(r.integers(0, ws.ACTS * ws.ACTS))
                pr = (q // ws.ACTS, q % ws.ACTS)
                if pr != tuple(home.pairs[k][j]) and pr not in pairs:
                    break
            pairs.append(pr)
        out.append(pairs)
    return out


def changed(k, d):
    return (k in A and d >= 31) or (k in B and d >= 46)


def test(home, net, seed, d, old):
    r = np.random.default_rng([seed, 6, d, 0])
    succ, stale = [], []
    for k in range(ws.KINDS):
        look = home.looks[k] + r.normal(0, 0.2, ws.LOOK)
        opened, chosen = ws.try_box(net, look, home.pairs[k], [], None, False)
        succ.append(1.0 if opened == ws.LIDS else 0.0)
        stale.append((1.0 if tuple(chosen[0]) == tuple(old[k][0]) else 0.0) if changed(k, d) else None)
    return {"success": succ, "stale": stale}


def run_child(n0, sched, seed, p=P, change=True, tests=False):
    home = ws.Home(seed)
    old = [list(map(tuple, pr)) for pr in home.pairs]
    new = new_codes(home, seed)
    net = wn.Net(seed, n0, True)
    rng = np.random.default_rng([seed, 3, ws.BRAINS.index("Bm")])
    food, out = 0, {"tests": {}}
    for d in range(1, ws.DAYS + 1):
        if change and d in CHANGE_DAY:
            for k in CHANGE_DAY[d]:
                home.pairs[k] = list(new[k])
        here = wt.present(seed, d, p)
        for i, (k, look, rnd) in enumerate(home.day(d)):
            prefix = []
            if d <= ws.DEMO_DAYS and here[i]:
                prefix = ws.show_steps(look, home.pairs[k])
                ws.copy_step(net, look, home.pairs[k], prefix, wn.COPY_RATE)
            food += ws.try_box(net, look, home.pairs[k], prefix, rng, True)[0]
        if tests and d in TEST_DAYS:
            out["tests"][d] = test(home, net, seed, d, old)
        if d in sched:
            wg.grow(net, sched[d], "awake_in")
    out.update(food=food, final_n=net.n, final_pairs=[list(map(list, pr)) for pr in home.pairs])
    return out


def evolve(run):
    rng = np.random.default_rng([run, 78])
    pop, hist = we.gen0(rng), []
    log = open(HERE / f"evo_run{run}.log", "a", encoding="utf-8")
    for gen in range(we.GENS):
        t0 = time.time()
        foods, finals = [], []
        for i, gn in enumerate(pop):
            n0, sched = we.schedule(gn)
            r = run_child(n0, sched, 100000 * run + 1000 * gen + i)
            foods.append(r["food"])
            finals.append(r["final_n"])
        hist.append({"gen": gen, "genes": [list(map(float, g)) for g in pop], "food": foods,
                     "born": [we.schedule(g)[0] for g in pop], "final": finals})
        (HERE / f"evo_run{run}.json").write_text(json.dumps(hist), encoding="utf-8")
        m = np.mean(pop, axis=0)
        log.write(f"{time.strftime('%Y-%m-%d %H:%M')} run {run} gen {gen} food {np.mean(foods):.1f} "
                  f"a {m[0]:.2f} g {m[1]:.2f} s {m[2]:.1f} e {m[3]:.1f} "
                  f"born {np.median([we.schedule(g)[0] for g in pop]):.0f} final {np.median(finals):.0f} "
                  f"secs {time.time() - t0:.0f}\n")
        log.flush()
        w = np.array(foods, float) + 1.0
        parents = rng.choice(we.POP, size=we.POP, p=w / w.sum())
        pop = [we.clamp(pop[q] + rng.normal(0, 1, 4) * we.SD) for q in parents]
    log.close()


def final():
    brains = {"GA": (16, {8: 32, 16: 64, 24: 128}), "M32": (32, {}), "M128": (128, {}), "M256": (256, {})}
    evolved = {}
    for run in (1, 2):
        last = json.loads((HERE / f"evo_run{run}.json").read_text())[-1]
        med = np.median(np.array(last["genes"]), axis=0)
        n0, sched = we.schedule(med)
        evolved[f"E{run}"] = {"median_genes": [float(x) for x in med], "born": n0, "schedule": sched}
        brains[f"E{run}"] = (n0, sched)
    tw = json.loads((HERE.parent / "WT" / "evolved_p50.json").read_text())
    for run in (1, 2):
        v = tw[f"E{run}"]
        brains[f"T{run}"] = (v["born"], {int(d): n for d, n in v["schedule"].items()})
    (HERE / "evolved.json").write_text(json.dumps(evolved, indent=1), encoding="utf-8")
    out = HERE / "output"
    out.mkdir(exist_ok=True)
    for b, (n0, sched) in brains.items():
        for s in range(1001, 1049):
            r = run_child(n0, sched, s, tests=True)
            r["brain"], r["seed"] = b, s
            (out / f"{b}_seed_{s}.json").write_text(json.dumps(r), encoding="utf-8")
        print("done", b, flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "evolve":
        for run in map(int, sys.argv[2:]):
            evolve(run)
    elif sys.argv[1] == "final":
        final()
