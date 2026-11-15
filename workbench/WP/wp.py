"""WP: one big brain among small ones (questions.md, WP-frozen). Groups of six children in one world; a grown-up on
20% of tries on days 1-30 (WT); children watch each other's latest tries all 60 days; optional WC change.

  python wp.py run WORLD          (WORLD: stable | change; writes output_<WORLD>/<GROUP>_g<seed>.json)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "WC"))
import wc  # noqa: E402
import wt  # noqa: E402
import wn  # noqa: E402
import ws  # noqa: E402

HERE = Path(__file__).parent
P_ADULT, COPY = 0.2, 0.5
GROUPS = {"S6": [32] * 6, "B1S5": [128] + [32] * 5, "B6": [128] * 6, "S6alone": [32] * 6}
TEST_DAYS = {"stable": (30, 60), "change": (30, 45, 60)}


def watch(net, look, seen, rate=COPY):
    """Hold the lids the watched child opened in memory and copy them. seen = (chosen pairs, lids opened).
    Returns the memory prefix (empty if nothing opened)."""
    chosen, opened = seen
    shown = [tuple(p) for p in chosen[:opened]]
    if not shown:
        return []
    prefix = ws.show_steps(look, shown)
    ws.copy_step(net, look, shown, prefix, rate)
    return prefix


def run_group(name, g, world, sizes=None):
    sizes = sizes or GROUPS[name]
    alone = name.endswith("alone")
    n = len(sizes)
    home = ws.Home(g)
    old = [list(map(tuple, pr)) for pr in home.pairs]
    new = wc.new_codes(home, g)
    nets = [wn.Net(1000 * g + c, sizes[c], True) for c in range(n)]
    rngs = [np.random.default_rng([1000 * g + c, 3, ws.BRAINS.index("Bm")]) for c in range(n)]
    wrng = np.random.default_rng([g, 11])
    trust = np.full((n, n), 0.5)
    watched = np.zeros((2, n, n), int)              # [phase (days 1-30, 31-60), watcher, watched]
    latest, food, adult_shows = {}, [0] * n, 0
    tests = {c: {} for c in range(n)}
    for d in range(1, ws.DAYS + 1):
        if world == "change" and d in wc.CHANGE_DAY:
            for k in wc.CHANGE_DAY[d]:
                home.pairs[k] = list(new[k])
        here = wt.present(g, d, P_ADULT)
        for i, (k, look, rnd) in enumerate(home.day(d)):
            prefixes = [[] for _ in range(n)]
            if d <= ws.DEMO_DAYS and here[i]:
                adult_shows += 1
                for c in range(n):
                    prefixes[c] = ws.show_steps(look, home.pairs[k])
                    ws.copy_step(nets[c], look, home.pairs[k], prefixes[c], COPY)
            elif not alone:
                for c in range(n):
                    cand = [o for o in range(n) if o != c and (o, k) in latest]
                    if not cand:
                        continue
                    w = np.array([max(trust[c, o], 0.05) for o in cand])
                    o = cand[int(wrng.choice(len(cand), p=w / w.sum()))]
                    seen = latest[(o, k)]
                    prefixes[c] = watch(nets[c], look, seen)
                    trust[c, o] += 0.3 * (seen[1] / ws.LIDS - trust[c, o])
                    watched[0 if d <= 30 else 1, c, o] += 1
            new_latest = {}
            for c in range(n):
                opened, chosen = ws.try_box(nets[c], look, home.pairs[k], prefixes[c], rngs[c], True)
                food[c] += opened
                new_latest[(c, k)] = (chosen, opened)
            latest.update(new_latest)
        if d in TEST_DAYS[world]:
            for c in range(n):
                tests[c][d] = wc.test(home, nets[c], g, d, old)["success"]
    return {"group": name, "g": g, "world": world, "sizes": sizes, "tests": tests, "food": food,
            "watched": watched.tolist(), "trust_end": trust.round(4).tolist(), "adult_shows": adult_shows}


if __name__ == "__main__":
    if sys.argv[1] == "run":
        world = sys.argv[2]
        out = HERE / f"output_{world}"
        out.mkdir(exist_ok=True)
        for name in GROUPS:
            for g in range(1, 49):
                (out / f"{name}_g{g}.json").write_text(json.dumps(run_group(name, g, world)), encoding="utf-8")
            print("done", world, name, flush=True)
