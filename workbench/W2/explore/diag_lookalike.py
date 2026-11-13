"""Exploratory (after the data, labelled): why does M pick the wrong side on the look-alike pairs?
Retrains M (seed given, 150,000 episodes; the same code and seed as the frozen run), saves its weights, then
classifies each look-alike room: the first sideways move toward the gap / away / none, and how much of the barrier
on each side the tour had shown.

  python workbench/W2/explore/diag_lookalike.py SEED
"""
import json, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
import run_w2 as R, world2 as W2  # noqa: E402

seed = int(sys.argv[1])
d = W2.load()
wp = HERE / f"M_seed_{seed}_weights.npz"
net = R.make("M", [seed, 2])
if wp.exists():
    net.p = dict(np.load(wp))
else:
    rng = np.random.default_rng([seed, 1])
    for _ in range(R.EPISODES):
        R.episode("M", net, d["learn"][int(rng.integers(len(d["learn"])))], rng)
    np.savez(wp, **net.p)
rows = []
for a, b in d["pairs"]:
    for lay in (a, b):
        m = R.mem_tour(lay)
        res = R.run_learned("M", net, lay, m, lay["tour"])
        path = res["path"]
        k = 0 if lay["axis"] == "x" else 1
        first = None
        for p, q in zip(path, path[1:]):
            if p[k] != q[k]:
                first = "toward" if abs(q[k] - lay["gap"][k]) < abs(p[k] - lay["gap"][k]) else "away"
                break
        # the barrier cells on the gap's side and the other side: the share the tour showed
        s = lay["start"]
        gside = [c for c in lay["walls"] if (c[k] - s[k]) * (lay["gap"][k] - s[k]) > 0]
        oside = [c for c in lay["walls"] if (c[k] - s[k]) * (lay["gap"][k] - s[k]) < 0]
        kg = float(np.mean([m.known[y, x] for x, y in gside])) if gside else None
        ko = float(np.mean([m.known[y, x] for x, y in oside])) if oside else None
        rows.append({"first": first, "solved": bool(res["solved"]), "known_gap_side": kg, "known_other_side": ko})
(HERE / f"diag_seed_{seed}.json").write_text(json.dumps(rows), encoding="utf-8")
from collections import Counter
print(seed, Counter(r["first"] for r in rows))
for lab, f in (("toward", lambda r: r["first"] == "toward"), ("away", lambda r: r["first"] == "away"),
               ("none", lambda r: r["first"] is None)):
    sel = [r for r in rows if f(r)]
    if sel:
        print(lab, len(sel), "known barrier, gap side %.2f, other side %.2f" % (
            np.mean([r["known_gap_side"] for r in sel if r["known_gap_side"] is not None]),
            np.mean([r["known_other_side"] for r in sel if r["known_other_side"] is not None])))
