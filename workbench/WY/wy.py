"""WY: "that worked!" (questions.md, WY-frozen). WM's changing world and parts (../WM/wm.py) plus YS: after a practice
try, each lid that opened is copied from the child's own acts, weighted by its positive surprise (1 - expectation).

  python wy.py arm ARM SIZE OUT_DIR      (ARM: Base | YS | TBYS; seeds 1001-1048)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "WM"))
import wm  # noqa: E402
import wc  # noqa: E402
import wt  # noqa: E402
import wn  # noqa: E402
import ws  # noqa: E402

ARMS = ("Base", "YS", "TBYS")
YS_RATE, Y_STEP = 1.0, 0.2


def self_copy(net, look, chosen, weights, prefix):
    """Copy the child's own acts on the lids that opened, through the try's memory steps; lid j weighted weights[j]."""
    xs, hs, h = ws.run_prefix(net, prefix)
    targets = {}
    for j, w in enumerate(weights):
        a1, a2 = chosen[j]
        for x, a in ((ws.x_try(look, j, None, 0), a1), (ws.x_try(look, j, a1, 1), a2)):
            h, _ = net.step(x, h)
            xs.append(x)
            hs.append(h)
            targets[len(xs) - 1] = (a, w)
    net.apply(net.grads(xs, hs, targets), ws.LR * YS_RATE)


def run_child(arm, n, seed):
    ys, tb = arm in ("YS", "TBYS"), arm == "TBYS"
    home = ws.Home(seed)
    old = [list(map(tuple, pr)) for pr in home.pairs]
    new = wc.new_codes(home, seed)
    net = wn.Net(seed, n, True)
    rng = np.random.default_rng([seed, 3, ws.BRAINS.index("Bm")])
    tabu = {k: {j: set() for j in range(ws.LIDS)} for k in range(ws.KINDS)}
    y = np.zeros((ws.KINDS, ws.LIDS))
    food, tests, ys_steps, ys_weight = 0, {}, 0, 0.0
    for d in range(1, ws.DAYS + 1):
        if d in wc.CHANGE_DAY:
            for k in wc.CHANGE_DAY[d]:
                home.pairs[k] = list(new[k])
        here = wt.present(seed, d, wc.P)
        for i, (k, look, rnd) in enumerate(home.day(d)):
            prefix = []
            if d <= ws.DEMO_DAYS and here[i]:
                prefix = ws.show_steps(look, home.pairs[k])
                ws.copy_step(net, look, home.pairs[k], prefix, wn.COPY_RATE)
            opened, chosen = wm.try_box(net, look, home.pairs[k], prefix, rng, True, 1.0, tabu[k] if tb else None)
            food += opened
            weights = []
            for j, (a1, a2) in enumerate(chosen):
                ok = j < opened
                if ok:
                    weights.append(1.0 - y[k, j])
                    tabu[k][j].clear()
                else:
                    tabu[k][j].add((a1, a2))
                    if len(tabu[k][j]) == ws.ACTS * ws.ACTS:
                        tabu[k][j].clear()
                y[k, j] += Y_STEP * ((1.0 if ok else 0.0) - y[k, j])
            if ys and weights and max(weights) > 0:
                self_copy(net, look, chosen, weights, prefix)
                ys_steps += 1
                ys_weight += float(np.mean(weights))
        if d in wc.TEST_DAYS:
            tests[d] = wm.test(home, net, seed, d, old, {}, False)
    return {"arm": arm, "n": n, "seed": seed, "tests": tests, "food": food, "ys_steps": ys_steps,
            "ys_mean_weight": ys_weight / ys_steps if ys_steps else 0.0}


if __name__ == "__main__":
    if sys.argv[1] == "arm":
        arm, n, out = sys.argv[2], int(sys.argv[3]), Path(sys.argv[4])
        out.mkdir(parents=True, exist_ok=True)
        for s in range(1001, 1049):
            (out / f"{arm}{n}_seed_{s}.json").write_text(json.dumps(run_child(arm, n, s)), encoding="utf-8")
        print("done", arm, n, flush=True)
