"""WE: genes decide how the brain grows (questions.md, WE-frozen). WG's task and "awake in, quiet out" growth
(../WG/wg.py); the growth schedule comes from 4 genes, and evolution picks parents by the food each child earns.

  python we.py evolve RUN          (writes evo_run<RUN>.json, one line per generation in evo_run<RUN>.log)
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "WG"))
import wg  # noqa: E402  (imports wn, which patches ws.run_prefix)
import wn  # noqa: E402
import ws  # noqa: E402

HERE = Path(__file__).parent
POP, GENS = 32, 30
SD = np.array([0.25, 0.25, 3.0, 3.0])            # mutation sd for a, g, s, e
MAXLOG = 8


def clamp(gn):
    a, g, s, e = gn
    a = min(max(a, 2.0), MAXLOG)
    g = min(max(g, 0.0), MAXLOG - a)
    s, e = min(max(s, 1.0), 60.0), min(max(e, 1.0), 60.0)
    if s > e:
        s, e = e, s
    return np.array([a, g, s, e])


def schedule(gn):
    """(neurons at birth, {end of day d: neurons})."""
    a, g, s, e = gn
    n0, nf = int(round(2 ** a)), min(256, int(round(2 ** (a + g))))
    si, ei = int(round(s)), int(round(e))
    sched, last = {}, n0
    if nf > n0:
        for d in range(si, ei + 1):
            n = n0 + int(round((nf - n0) * (d - si + 1) / (ei - si + 1)))
            if n > last:
                sched[d], last = n, n
    return n0, sched


def run_child(n0, sched, seed, tests=False):
    home = ws.Home(seed)
    net = wn.Net(seed, n0, True)
    rng = np.random.default_rng([seed, 3, ws.BRAINS.index("Bm")])
    food, out = 0, {"tests": {}, "show_tests": {}}
    for d in range(1, ws.DAYS + 1):
        for k, look, rnd in home.day(d):
            prefix = []
            if d <= ws.DEMO_DAYS:
                prefix = ws.show_steps(look, home.pairs[k])
                ws.copy_step(net, look, home.pairs[k], prefix, wn.COPY_RATE)
            food += ws.try_box(net, look, home.pairs[k], prefix, rng, True)[0]
        if tests and d in wn.TEST_DAYS:
            out["tests"][d] = ws.test(home, net, seed, d)
        if tests and d in wn.SHOW_TEST_DAYS:
            out["show_tests"][d] = ws.test(home, net, seed, d, showing=True)
        if d in sched:
            wg.grow(net, sched[d], "awake_in")
    out.update(food=food, final_n=net.n)
    return out


def gen0(rng):
    pop = []
    for _ in range(POP):
        a = rng.uniform(2, MAXLOG)
        g = rng.uniform(0, MAXLOG - a)
        s, e = sorted(rng.uniform(1, 60, 2))
        pop.append(np.array([a, g, s, e]))
    return pop


def evolve(run):
    rng = np.random.default_rng([run, 77])
    pop, hist = gen0(rng), []
    log = open(HERE / f"evo_run{run}.log", "a", encoding="utf-8")
    for gen in range(GENS):
        t0 = time.time()
        foods, finals = [], []
        for i, gn in enumerate(pop):
            n0, sched = schedule(gn)
            r = run_child(n0, sched, 100000 * run + 1000 * gen + i)
            foods.append(r["food"])
            finals.append(r["final_n"])
        hist.append({"gen": gen, "genes": [list(map(float, g)) for g in pop], "food": foods,
                     "born": [schedule(g)[0] for g in pop], "final": finals})
        (HERE / f"evo_run{run}.json").write_text(json.dumps(hist), encoding="utf-8")
        m = np.mean(pop, axis=0)
        log.write(f"{time.strftime('%Y-%m-%d %H:%M')} run {run} gen {gen} food {np.mean(foods):.1f} "
                  f"a {m[0]:.2f} g {m[1]:.2f} s {m[2]:.1f} e {m[3]:.1f} born {np.median([schedule(g)[0] for g in pop]):.0f} "
                  f"final {np.median(finals):.0f} secs {time.time() - t0:.0f}\n")
        log.flush()
        w = np.array(foods, float) + 1.0
        parents = rng.choice(POP, size=POP, p=w / w.sum())
        pop = [clamp(pop[p] + rng.normal(0, 1, 4) * SD) for p in parents]
    log.close()


if __name__ == "__main__":
    if sys.argv[1] == "evolve":
        for run in map(int, sys.argv[2:]):
            evolve(run)
