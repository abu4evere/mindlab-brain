"""W3d's frozen analysis (questions.md, Readings), written before any data -> analysis.md / analysis.json.
Per run: the mean over its 50 test lives. Intervals: bootstrap over the 8 seeds (10,000 draws, numpy seed 20261130);
differences paired by seed."""
import json
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
W3O, W3BO, OUT = HERE.parent / "W3" / "output", HERE.parent / "W3b" / "output", HERE / "output"
SEEDS = range(1, 9)
IDX = np.random.default_rng(20261130).integers(0, 8, (10_000, 8))
MEAS = ("survived", "surv1000", "lifespan", "known_end", "hungry", "exhausted")
SRC = {"D3 (W3)": lambda s: W3O / f"test_D3_{s}.json", "YFR (W3b)": lambda s: W3BO / f"test_YFR_{s}.json",
       "P": lambda s: OUT / f"test_P_{s}.json", "PYFR": lambda s: OUT / f"test_PYFR_{s}.json",
       "PA": lambda s: OUT / f"test_PA_{s}.json"}


def run_means(path):
    lives = json.loads(path.read_text())
    vals = {m: [l[m] for l in lives] for m in MEAS if m != "surv1000"}
    vals["surv1000"] = [1.0 if l["lifespan"] >= 1000 else 0.0 for l in lives]
    return {m: float(np.mean(v)) for m, v in vals.items()}


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3)]


R = {k: [run_means(f(s)) for s in SEEDS if f(s).exists()] for k, f in SRC.items()}
f3 = lambda t: f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"


def diff(a, b, m):
    if len(R.get(a, [])) != 8 or len(R.get(b, [])) != 8:
        return None
    return ci([x[m] - y[m] for x, y in zip(R[a], R[b])])


out = {"arms": {}, "readings": {}}
L = ["# W3d analysis (the frozen analysis, analyse_w3d.py)", "",
     "Per run: the mean over its 50 test lives (tested alone); intervals: bootstrap over the 8 seeds (seed 20261130).", "",
     "| arm | runs | survived to 3,000 | to 1,000 | lifespan | known@end | hungry | exhausted |",
     "|---|---|---|---|---|---|---|---|"]
for k, rs in R.items():
    if not rs:
        continue
    out["arms"][k] = {m: ci([r[m] for r in rs]) for m in MEAS} | {"n_runs": len(rs)}
    a = out["arms"][k]
    L.append(f"| {k} | {len(rs)} | {f3(a['survived'])} | {f3(a['surv1000'])} | {a['lifespan'][0]:.0f} "
             f"[{a['lifespan'][1]:.0f}, {a['lifespan'][2]:.0f}] | {a['known_end'][0]:.2f} | {a['hungry'][0]:.2f} | "
             f"{a['exhausted'][0]:.2f} |")
r1 = [k for k in ("P", "PYFR") if k in out["arms"] and out["arms"][k]["survived"][0] >= 0.5
      and out["arms"][k]["survived"][1] >= 0.3]
all0 = all(out["arms"].get(k, {}).get("survived", [0])[0] == 0 for k in ("P", "D3 (W3)"))
m2 = "lifespan" if all0 else "survived"
d2 = diff("P", "D3 (W3)", m2)
all0b = all(out["arms"].get(k, {}).get("survived", [0])[0] == 0 for k in ("P", "PYFR"))
m3 = "lifespan" if all0b else "survived"
d3, d4, d4l = diff("PYFR", "P", m3), diff("PA", "P", "survived"), diff("PA", "P", "lifespan")
L += ["", "## Readings", "",
      f"1. **A child taught by a parent lives** (P or PYFR: mean >= 0.50, lower >= 0.30): **{'YES: ' + ', '.join(r1) if r1 else 'NO'}**",
      f"2. **The parent helps** (P − D3 on {m2}): {f3(d2) if d2 else 'n/a'} -> **{'YES' if d2 and d2[1] > 0 else 'NO'}**",
      f"3. **The recipe adds** (PYFR − P on {m3}): {f3(d3) if d3 else 'n/a'}",
      f"4. **A parent who never leaves** (PA − P): survival {f3(d4) if d4 else 'n/a'}; lifespan {f3(d4l) if d4l else 'n/a'}",
      "", "Secondary (survival to 1,000, paired):"]
for a, b in (("P", "D3 (W3)"), ("PYFR", "P"), ("PA", "P"), ("PYFR", "YFR (W3b)")):
    d = diff(a, b, "surv1000")
    L.append(f"- {a} − {b}: {f3(d) if d else 'n/a'}")
out["readings"] = {"r1": r1, "r2": d2, "m2": m2, "r3": d3, "m3": m3, "r4_survival": d4, "r4_lifespan": d4l}
(HERE / "analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
(HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
