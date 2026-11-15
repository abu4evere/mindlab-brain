"""WO: shown only once (questions.md, WO-frozen). Two new kinds of box each day (days 1-30), each shown once; retention
tests 1 and 7 days later; review tries on kinds from 1, 2, 4 and 7 days ago. Arms L0, L2, Linf (WL2's episodes).

  python wo.py arm ARM SIZE OUT_DIR      (seeds 1-48)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "WL2"))
import wl2  # noqa: E402  (wait-aware prefix runner; episodes)
import wn  # noqa: E402
import ws  # noqa: E402

ARMS = ("L0", "L2", "Linf")
DAYS, NEW_PER_DAY = 30, 2
REVIEW_AGO, RETAIN_AGO = (1, 2, 4, 7), (1, 7)


def boxes(seed):
    r = np.random.default_rng([seed, 21])
    looks = r.normal(0, 1, (DAYS * NEW_PER_DAY, ws.LOOK))
    codes = []
    for _ in range(DAYS * NEW_PER_DAY):
        ps = r.permutation(ws.ACTS * ws.ACTS)[:ws.LIDS]
        codes.append([(int(p) // ws.ACTS, int(p) % ws.ACTS) for p in ps])
    return looks, codes


def kinds_of(day):
    return [NEW_PER_DAY * (day - 1) + i for i in range(NEW_PER_DAY)] if 1 <= day <= DAYS else []


def full(net, look, code, prefix):
    return 1.0 if ws.try_box(net, look, code, prefix, None, False)[0] == ws.LIDS else 0.0


CHILDHOOD = 30      # correction 1: days 1-30 are WL2's childhood (6 familiar kinds, a showing before every try)


def run_child(arm, n, seed):
    looks, codes = boxes(seed)
    net = wl2.Net(seed, n, True)
    rng = np.random.default_rng([seed, 3, ws.BRAINS.index("Bm")])
    nrng = np.random.default_rng([seed, 13])
    home = ws.Home(seed)
    for d in range(1, CHILDHOOD + 1):                           # childhood: WL2's world, the arm's own memory episodes
        for k, look, rnd in home.day(d):
            ep = wl2.episode(arm, look, home.pairs[k], n, nrng)
            ws.copy_step(net, look, home.pairs[k], ep, wn.COPY_RATE)
            ws.try_box(net, look, home.pairs[k], ep, rng, True)
    immediate, retain, food = {}, {1: {}, 7: {}}, 0
    for d in range(1, DAYS + 1):                                # new boxes: life days 31-60
        lr = np.random.default_rng([seed, 22, d])
        tr = np.random.default_rng([seed, 23, d])
        for ago in RETAIN_AGO:                                  # 1. retention tests
            for k in kinds_of(d - ago):
                retain[ago][k] = full(net, looks[k] + tr.normal(0, 0.2, ws.LOOK), codes[k], [])
        for ago in REVIEW_AGO:                                  # 2. review practice
            for k in kinds_of(d - ago):
                food += ws.try_box(net, looks[k] + lr.normal(0, 0.2, ws.LOOK), codes[k], [], rng, True)[0]
        for k in kinds_of(d):                                   # 3. new kinds
            look = looks[k] + lr.normal(0, 0.2, ws.LOOK)
            ep = wl2.episode(arm, look, codes[k], n, nrng)
            ws.copy_step(net, look, codes[k], ep, wn.COPY_RATE)
            immediate[k] = full(net, look, codes[k], ep)
            food += ws.try_box(net, look, codes[k], ep, rng, True)[0]
            for _ in range(2):
                food += ws.try_box(net, looks[k] + lr.normal(0, 0.2, ws.LOOK), codes[k], [], rng, True)[0]
    return {"arm": arm, "n": n, "seed": seed, "immediate": immediate, "retain1": retain[1], "retain7": retain[7],
            "food": food}


if __name__ == "__main__":
    if sys.argv[1] == "arm":
        arm, n, out = sys.argv[2], int(sys.argv[3]), Path(sys.argv[4])
        out.mkdir(parents=True, exist_ok=True)
        for s in range(1, 49):
            (out / f"{arm}_{n}_seed_{s}.json").write_text(json.dumps(run_child(arm, n, s)), encoding="utf-8")
        print("done", arm, n, flush=True)
