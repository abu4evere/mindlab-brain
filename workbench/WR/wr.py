"""WR: the recipe in one brain (questions.md, WR-frozen). One generic child for every arm and world.

Parts (letters in the arm name): L = learn without the showing in mind (WL2's Linf), T = don't repeat a failure (WM's
TB with correction 1), Y = "that worked!" (WY's YS), R = a fast memory replayed at night (WF's RP). Base and L0 have
no parts.

Worlds: "change" = WC's changing world (teacher p = 0.5 on days 1-30; kinds 0-2 change at day 31, kinds 3-5 at day
46; seeds 1001-1048); "stable" = WL2's world (a showing before every try on days 1-30, no change; seeds 1-48).

  python wr.py arm WORLD ARM SIZE OUT_DIR
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "WF"))
import wf  # noqa: E402  (imports wy, wm, wc, wt, we, wg, wn, ws; wn patches ws.run_prefix for any size)
import wy  # noqa: E402
import wc  # noqa: E402
import wt  # noqa: E402
import wn  # noqa: E402
import ws  # noqa: E402

PARTS = {"Base": "", "L0": "", "L": "L", "TY": "TY", "TYR": "TYR", "LTYR": "LTYR", "LTY": "LTY", "LYR": "LYR",
         "LTR": "LTR"}
ARMS = {"change": ("Base", "L", "TY", "TYR", "LTYR", "LTY", "LYR", "LTR"), "stable": ("L0", "L", "TYR", "LTYR")}
SEEDS = {"change": range(1001, 1049), "stable": range(1, 49)}
STABLE_TEST_DAYS = (7, 15, 30, 60)                     # WL's (the reproduction check against WL2 covers it)


def prefix_for(parts, look, pairs):
    """What the memory holds before the copy step, the try and the self-copy, when the teacher shows."""
    return [] if "L" in parts else ws.show_steps(look, pairs)


def test_change(home, net, seed, d, old):
    """WC's test: each kind once, no showing, greedy, the network only; success and the stale first-lid habit."""
    r = np.random.default_rng([seed, 6, d, 0])
    succ, stale = [], []
    for k in range(ws.KINDS):
        look = home.looks[k] + r.normal(0, 0.2, ws.LOOK)
        opened, chosen = wf.try_box(net, look, home.pairs[k], [], None, False)
        succ.append(1.0 if opened == ws.LIDS else 0.0)
        stale.append((1.0 if tuple(chosen[0]) == tuple(old[k][0]) else 0.0) if wc.changed(k, d) else None)
    return {"success": succ, "stale": stale}


def test_stable(home, net, seed, d, parts, showing=False):
    """WL2's test: the share of full boxes; with showing, the arm's own memory before the try (blank for L)."""
    r = np.random.default_rng([seed, 6, d, int(showing)])
    full = []
    for k in range(ws.KINDS):
        look = home.looks[k] + r.normal(0, 0.2, ws.LOOK)
        prefix = prefix_for(parts, look, home.pairs[k]) if showing else []
        full.append(1.0 if wf.try_box(net, look, home.pairs[k], prefix, None, False)[0] == ws.LIDS else 0.0)
    return float(np.mean(full))


def run_child(world, arm, n, seed):
    parts = PARTS[arm]
    L, T, Y, R = ("L" in parts), ("T" in parts), ("Y" in parts), ("R" in parts)
    change = world == "change"
    home = ws.Home(seed)
    old = [list(map(tuple, pr)) for pr in home.pairs]
    new = wc.new_codes(home, seed) if change else None
    net = wn.Net(seed, n, True)
    rng = np.random.default_rng([seed, 3, ws.BRAINS.index("Bm")])
    tabu = {k: {j: set() for j in range(ws.LIDS)} for k in range(ws.KINDS)}
    y = np.zeros((ws.KINDS, ws.LIDS))
    store, food, tests, replays, self_copies, show30 = {}, 0, {}, 0, 0, None
    for d in range(1, ws.DAYS + 1):
        if change and d in wc.CHANGE_DAY:
            for k in wc.CHANGE_DAY[d]:
                home.pairs[k] = list(new[k])
        here = wt.present(seed, d, wc.P) if change else np.ones(ws.KINDS * ws.TRIES, bool)
        for i, (k, look, rnd) in enumerate(home.day(d)):
            prefix = []
            if d <= ws.DEMO_DAYS and here[i]:
                prefix = prefix_for(parts, look, home.pairs[k])
                ws.copy_step(net, look, home.pairs[k], prefix, wn.COPY_RATE)
            opened, chosen = wf.try_box(net, look, home.pairs[k], prefix, rng, True, tabu[k] if T else None)
            food += opened
            weights = []
            for j, (a1, a2) in enumerate(chosen):
                ok = j < opened
                if ok:
                    weights.append(1.0 - y[k, j])
                    tabu[k][j].clear()
                    store[(k, j)] = ((a1, a2), True)
                else:
                    tabu[k][j].add((a1, a2))
                    if len(tabu[k][j]) == ws.ACTS * ws.ACTS:          # WM's correction 1: every pair failed -> search again
                        tabu[k][j].clear()
                    if (k, j) in store and store[(k, j)][0] == (a1, a2):
                        store[(k, j)] = (store[(k, j)][0], False)      # the stored pair failed here: stale
                y[k, j] += wy.Y_STEP * ((1.0 if ok else 0.0) - y[k, j])
            if Y and weights and max(weights) > 0:
                wy.self_copy(net, look, chosen, weights, prefix)
                self_copies += 1
        if R:                                                           # WF's nightly replay from the store
            for k in range(ws.KINDS):
                pairs = []
                for j in range(ws.LIDS):
                    if (k, j) in store and store[(k, j)][1]:
                        pairs.append(store[(k, j)][0])
                    else:
                        break
                if pairs:
                    for _ in range(wf.RP_STEPS):
                        ws.copy_step(net, home.looks[k], pairs, [], wf.RP_RATE)
                        replays += 1
        if change:
            if d in wc.TEST_DAYS:
                tests[d] = test_change(home, net, seed, d, old)
        else:
            if d in STABLE_TEST_DAYS:
                tests[d] = test_stable(home, net, seed, d, parts)
            if d == 30:
                show30 = test_stable(home, net, seed, d, parts, showing=True)
    out = {"world": world, "arm": arm, "n": n, "seed": seed, "tests": tests, "food": food, "replays": replays,
           "self_copies": self_copies}
    if not change:
        out["show30"] = show30
    return out


if __name__ == "__main__":
    if sys.argv[1] == "arm":
        world, arm, n, out = sys.argv[2], sys.argv[3], int(sys.argv[4]), Path(sys.argv[5])
        out.mkdir(parents=True, exist_ok=True)
        for s in SEEDS[world]:
            (out / f"{world}_{arm}_{n}_seed_{s}.json").write_text(json.dumps(run_child(world, arm, n, s)), encoding="utf-8")
        print("done", world, arm, n, flush=True)
