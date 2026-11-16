"""WI analysis (descriptive; questions.md). 95% bootstrap intervals over the 8 seeds (numpy seed 20261132, 10,000
resamples; paired by seed)."""
import json
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
OUT = HERE / "output"
SEEDS = range(1, 9)
IDX = np.random.default_rng(20261132).integers(0, 8, (10_000, 8))


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3)]


f = lambda t: f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"
R = {a: [json.loads((OUT / f"{a}_{s}.json").read_text()) for s in SEEDS] for a in ("L", "IM")}
PRE = [json.loads((HERE.parent / "W3c" / "output" / f"test_GYFR_{s}.json").read_text()) for s in SEEDS]
win = lambda a, w, k: np.array([r["windows"][w][k] for r in R[a]])
after = lambda lives, k: float(np.mean([l[k] for l in lives]))
out, L = {}, ["# WI analysis (from analyse_wi.py; 8 seeds; mean [95% interval])", "", "## In the silent room (living)", "",
              "| arm | activity w1 | activity w10 | reach w10 | pattern w10 |", "|---|---|---|---|---|"]
for a in ("L", "IM"):
    out[a] = {"activity_w1": ci(win(a, 0, "activity")), "activity_w10": ci(win(a, 9, "activity")),
              "reach_w10": ci(win(a, 9, "reach")), "pattern_w10": ci(win(a, 9, "pattern"))}
    o = out[a]
    L.append(f"| {a} | {f(o['activity_w1'])} | {f(o['activity_w10'])} | {f(o['reach_w10'])} | {f(o['pattern_w10'])} |")
d1 = {k: ci(win("IM", 9, k) - win("L", 9, k)) for k in ("activity", "reach", "pattern")}
out["IM-L room w10"] = d1
L += ["", f"**Reading 1, IM − L (last window):** activity {f(d1['activity'])}; reach {f(d1['reach'])}; pattern {f(d1['pattern'])}", "",
      "## After the room (W3's 50 test lands, learning off)", "", "| | survived to 3,000 | lifespan |", "|---|---|---|"]
for name, lives_list in (("Pre (W3c GYFR, before the room)", PRE), ("L", [r["after"] for r in R["L"]]), ("IM", [r["after"] for r in R["IM"]])):
    sv, ls = ci([after(x, "survived") for x in lives_list]), ci([after(x, "lifespan") for x in lives_list])
    out[f"after {name}"] = {"survived": sv, "lifespan": ls}
    L.append(f"| {name} | {f(sv)} | {ls[0]:.0f} [{ls[1]:.0f}, {ls[2]:.0f}] |")
for a, b, lb in (("IM", "L", "IM − L"), ("IM", "Pre", "IM − Pre"), ("L", "Pre", "L − Pre")):
    A = [r["after"] for r in R[a]] if a != "Pre" else PRE
    Bv = [r["after"] for r in R[b]] if b != "Pre" else PRE
    dl = ci([after(x, "lifespan") - after(y, "lifespan") for x, y in zip(A, Bv)])
    ds = ci([after(x, "survived") - after(y, "survived") for x, y in zip(A, Bv)])
    out[f"after {lb}"] = {"lifespan": dl, "survived": ds}
    L.append(f"- **{lb}:** lifespan {f(dl)}; survived {f(ds)}")
first = [np.mean([d["eaten"] for d in r["dreams"][:5]]) for r in R["IM"]]
last = [np.mean([d["eaten"] for d in r["dreams"][-5:]]) for r in R["IM"]]
out["dreams"] = {"first5": ci(first), "last5": ci(last), "last-first": ci(np.array(last) - np.array(first))}
L += ["", "## Dreams (IM)", "", f"- Food eaten per dream: first 5 {f(ci(first))}; last 5 {f(ci(last))}; last − first {f(out['dreams']['last-first'])}",
      f"- Dreams per stay: {len(R['IM'][0]['dreams'])}"]
(HERE / "analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
(HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
