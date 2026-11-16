"""W3f's frozen analysis (questions.md), written before any data -> analysis.md / analysis.json. Per run: the mean over
its 50 test lives (alone). Bootstrap over the 8 seeds (numpy seed 20261135); paired by seed. Rows appear as stages exist."""
import json
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
SEEDS = range(1, 9)
IDX = np.random.default_rng(20261135).integers(0, 8, (10_000, 8))


def runs(name):
    ps = [HERE / "output" / f"test_{name}_{s}.json" for s in SEEDS]
    if not all(p.exists() for p in ps):
        return None
    out = []
    for p in ps:
        lives = json.loads(p.read_text())
        out.append({"lifespan": float(np.mean([l["lifespan"] for l in lives])), "survived": float(np.mean([l["survived"] for l in lives])),
                    "surv1000": float(np.mean([l["lifespan"] >= 1000 for l in lives]))})
    return out


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3)]


f3 = lambda t: f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"
G2 = [{"lifespan": float(np.mean([l["lifespan"] for l in json.loads((HERE.parent / "W3e" / "output" / f"test_G2_{s}.json").read_text())]))} for s in SEEDS]
R = {n: runs(n) for n in ("CH1", "RN1", "CH2", "RN2", "CH3", "RN3")}
out = {"arms": {}, "readings": {}}
L = ["# W3f analysis (the frozen analysis, analyse_w3f.py)", "", "| arm | survived to 3,000 | to 1,000 | lifespan |", "|---|---|---|---|",
     f"| G2 pool (W3e) | – | – | {np.mean([g['lifespan'] for g in G2]):.0f} (best {max(g['lifespan'] for g in G2):.0f}) |"]
for n, rs in R.items():
    if rs:
        out["arms"][n] = {k: ci([r[k] for r in rs]) for k in ("survived", "surv1000", "lifespan")}
        a = out["arms"][n]
        L.append(f"| {n} | {f3(a['survived'])} | {f3(a['surv1000'])} | {a['lifespan'][0]:.0f} [{a['lifespan'][1]:.0f}, {a['lifespan'][2]:.0f}] |")


def d(a, b, k="lifespan"):
    ra = R.get(a) if a != "G2" else G2
    rb = R.get(b) if b != "G2" else G2
    return ci([x[k] - y[k] for x, y in zip(ra, rb)]) if ra and rb else None


L += ["", "## Readings", ""]
for lab, a, b in (("1. Choosing helps in one generation (CH1 − RN1)", "CH1", "RN1"), ("2. CH1 − the G2 pool (paired by seed)", "CH1", "G2"),
                  ("3a. CH across generations (CH3 − CH1)", "CH3", "CH1"), ("3b. RN across generations (RN3 − RN1)", "RN3", "RN1"),
                  ("3c. CH3 − RN3", "CH3", "RN3"), ("CH2 − RN2", "CH2", "RN2"), ("CH2 − CH1", "CH2", "CH1"), ("RN2 − RN1", "RN2", "RN1")):
    v = d(a, b)
    out["readings"][lab] = v
    L.append(f"- **{lab}:** lifespan {f3(v) if v else 'n/a'}")
(HERE / "analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
(HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
