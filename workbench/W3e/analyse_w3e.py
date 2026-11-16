"""W3e's frozen analysis (questions.md), written before any data -> analysis.md / analysis.json. Per run: the mean over
its 50 test lives. Intervals: bootstrap over the 8 seeds (numpy seed 20261134); differences paired by seed. G3 rows
appear when its runs exist."""
import json
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
WB = HERE.parent
SEEDS = range(1, 9)
IDX = np.random.default_rng(20261134).integers(0, 8, (10_000, 8))
MEAS = ("survived", "surv1000", "lifespan", "known_end")
SRC = {"YFR (W3b, recipe only)": lambda s: WB / "W3b" / "output" / f"test_YFR_{s}.json",
       "PYFR (W3d, script parent) = G2's parent": lambda s: WB / "W3d" / "output" / f"test_PYFR_{s}.json",
       "G2": lambda s: HERE / "output" / f"test_G2_{s}.json", "G3": lambda s: HERE / "output" / f"test_G3_{s}.json"}


def run_means(p):
    lives = json.loads(p.read_text())
    v = {m: float(np.mean([l[m] for l in lives])) for m in ("survived", "lifespan", "known_end")}
    v["surv1000"] = float(np.mean([l["lifespan"] >= 1000 for l in lives]))
    return v


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3)]


R = {k: [run_means(f(s)) for s in SEEDS if f(s).exists()] for k, f in SRC.items()}
f3 = lambda t: f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"


def diff(a, b, m):
    if len(R[a]) != 8 or len(R[b]) != 8:
        return None
    return ci([x[m] - y[m] for x, y in zip(R[a], R[b])])


P = "PYFR (W3d, script parent) = G2's parent"
Y = "YFR (W3b, recipe only)"
out = {"arms": {}, "readings": {}}
L = ["# W3e analysis (the frozen analysis, analyse_w3e.py)", "", "| arm | runs | survived to 3,000 | to 1,000 | lifespan | known@end |",
     "|---|---|---|---|---|---|"]
for k, rs in R.items():
    if rs:
        out["arms"][k] = {m: ci([r[m] for r in rs]) for m in MEAS} | {"n": len(rs)}
        a = out["arms"][k]
        L.append(f"| {k} | {len(rs)} | {f3(a['survived'])} | {f3(a['surv1000'])} | {a['lifespan'][0]:.0f} "
                 f"[{a['lifespan'][1]:.0f}, {a['lifespan'][2]:.0f}] | {a['known_end'][0]:.2f} |")
L += ["", "## Readings", ""]
for lab, a, b in (("1. Skill passes on (G2 − its parent)", "G2", P), ("2. A learned parent beats no parent (G2 − recipe only)", "G2", Y),
                  ("3. Ratchet or decay (G3 − G2)", "G3", "G2")):
    dl, ds = diff(a, b, "lifespan"), diff(a, b, "survived")
    out["readings"][lab] = {"lifespan": dl, "survived": ds}
    L.append(f"- **{lab}:** lifespan {f3(dl) if dl else 'n/a'}; survival {f3(ds) if ds else 'n/a'}")
for gen in ("G2", "G3"):
    fs = [HERE / "output" / f"fid_{gen}_{s}.json" for s in SEEDS]
    if all(p.exists() for p in fs):
        fd = [json.loads(p.read_text()) for p in fs]
        c, d = ci([x["child"] for x in fd]), ci([x["d3"] for x in fd])
        dd = ci([x["child"] - x["d3"] for x in fd])
        out["readings"][f"4. fidelity {gen}"] = {"child": c, "d3": d, "child-d3": dd}
        L.append(f"- **4. Fidelity ({gen} copies its parent):** child {f3(c)}; D3 baseline {f3(d)}; child − D3 {f3(dd)}")
(HERE / "analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
(HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
