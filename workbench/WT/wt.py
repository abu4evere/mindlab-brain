"""WT: a teacher who is sometimes absent (questions.md, WT-frozen). WE's evolution (../WE/we.py), with the teacher
present on each try of days 1-30 with probability p (drawn by the world, [seed, 5, day]).

  python wt.py evolve P RUN [RUN ...]       (P as a percentage, e.g. 50; writes evo_p<P>_run<RUN>.json/.log)
  python wt.py final P                      (final test in the P world; writes output_p<P>/ and evolved_p<P>.json)
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "WE"))
import we  # noqa: E402
import wg  # noqa: E402
import wn  # noqa: E402
import ws  # noqa: E402

HERE = Path(__file__).parent


def present(seed, d, p):
    """The teacher's presence on each of day d's 18 tries (the same for every brain in this world)."""
    u = np.random.default_rng([seed, 5, d]).random(ws.KINDS * ws.TRIES)
    return u < p


def run_child(n0, sched, seed, p, tests=False):
    home = ws.Home(seed)
    net = wn.Net(seed, n0, True)
    rng = np.random.default_rng([seed, 3, ws.BRAINS.index("Bm")])
    food, shows, out = 0, 0, {"tests": {}, "show_tests": {}}
    for d in range(1, ws.DAYS + 1):
        here = present(seed, d, p)
        for i, (k, look, rnd) in enumerate(home.day(d)):
            prefix = []
            if d <= ws.DEMO_DAYS and here[i]:
                prefix = ws.show_steps(look, home.pairs[k])
                ws.copy_step(net, look, home.pairs[k], prefix, wn.COPY_RATE)
                shows += 1
            food += ws.try_box(net, look, home.pairs[k], prefix, rng, True)[0]
        if tests and d in wn.TEST_DAYS:
            out["tests"][d] = ws.test(home, net, seed, d)
        if tests and d in wn.SHOW_TEST_DAYS:
            out["show_tests"][d] = ws.test(home, net, seed, d, showing=True)
        if d in sched:
            wg.grow(net, sched[d], "awake_in")
    out.update(food=food, final_n=net.n, shows=shows)
    return out


def evolve(P, run):
    p = P / 100
    rng = np.random.default_rng([run, 77, P])
    pop, hist = we.gen0(rng), []
    log = open(HERE / f"evo_p{P}_run{run}.log", "a", encoding="utf-8")
    for gen in range(we.GENS):
        t0 = time.time()
        foods, finals = [], []
        for i, gn in enumerate(pop):
            n0, sched = we.schedule(gn)
            r = run_child(n0, sched, 100000 * run + 1000 * gen + i, p)
            foods.append(r["food"])
            finals.append(r["final_n"])
        hist.append({"gen": gen, "genes": [list(map(float, g)) for g in pop], "food": foods,
                     "born": [we.schedule(g)[0] for g in pop], "final": finals})
        (HERE / f"evo_p{P}_run{run}.json").write_text(json.dumps(hist), encoding="utf-8")
        m = np.mean(pop, axis=0)
        log.write(f"{time.strftime('%Y-%m-%d %H:%M')} p {P} run {run} gen {gen} food {np.mean(foods):.1f} "
                  f"a {m[0]:.2f} g {m[1]:.2f} s {m[2]:.1f} e {m[3]:.1f} "
                  f"born {np.median([we.schedule(g)[0] for g in pop]):.0f} final {np.median(finals):.0f} "
                  f"secs {time.time() - t0:.0f}\n")
        log.flush()
        w = np.array(foods, float) + 1.0
        parents = rng.choice(we.POP, size=we.POP, p=w / w.sum())
        pop = [we.clamp(pop[q] + rng.normal(0, 1, 4) * we.SD) for q in parents]
    log.close()


def final(P):
    p = P / 100
    brains = {"GA": (16, {8: 32, 16: 64, 24: 128}), "M32": (32, {}), "M128": (128, {})}
    evolved = {}
    for run in (1, 2):
        last = json.loads((HERE / f"evo_p{P}_run{run}.json").read_text())[-1]
        med = np.median(np.array(last["genes"]), axis=0)
        n0, sched = we.schedule(med)
        evolved[f"E{run}"] = {"median_genes": [float(x) for x in med], "born": n0, "schedule": sched}
        brains[f"E{run}"] = (n0, sched)
    (HERE / f"evolved_p{P}.json").write_text(json.dumps(evolved, indent=1), encoding="utf-8")
    out = HERE / f"output_p{P}"
    out.mkdir(exist_ok=True)
    for b, (n0, sched) in brains.items():
        for s in range(1001, 1049):
            r = run_child(n0, sched, s, p, tests=True)
            r["brain"], r["seed"] = b, s
            (out / f"{b}_seed_{s}.json").write_text(json.dumps(r), encoding="utf-8")
        print("done", P, b, flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "evolve":
        for run in map(int, sys.argv[3:]):
            evolve(int(sys.argv[2]), run)
    elif sys.argv[1] == "final":
        final(int(sys.argv[2]))
