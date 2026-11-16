"""WG2 analysis (descriptive; questions.md). 95% bootstrap intervals over the 8 seeds (numpy seed 20261133, 10,000
resamples; paired by seed). IM and IQ both from this study's cloud run (IM re-run reproduces WI's IM)."""
import json
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
OUT = HERE / "output"
SEEDS = range(1, 9)
IDX = np.random.default_rng(20261133).integers(0, 8, (10_000, 8))


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3)]


f = lambda t: f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"
R = {a: [json.loads((OUT / f"{a}_{s}.json").read_text()) for s in SEEDS] for a in ("IM", "IQ")}
RL = [json.loads((HERE.parent / "WI" / "output" / f"L_{s}.json").read_text()) for s in SEEDS]
win = lambda rs, w, k: np.array([r["windows"][w][k] for r in rs])
ans = lambda rs: np.array([np.mean([q["answered"] is not None for q in r["questions"]]) if r["questions"] else np.nan for r in rs])
life = lambda rs: np.array([np.mean([l["lifespan"] for l in r["after"]]) for r in rs])
out, L = {}, ["# WG2 analysis (from analyse_wg2.py; 8 seeds; mean [95% interval])", "",
              "| arm | activity w10 | reach w10 | pattern w10 | questions answered in 500 steps | lifespan after |",
              "|---|---|---|---|---|---|"]
for name, rs in (("L (WI)", RL), ("IM", R["IM"]), ("IQ", R["IQ"])):
    a = ans(rs) if name != "L (WI)" else None
    out[name] = {"activity": ci(win(rs, 9, "activity")), "reach": ci(win(rs, 9, "reach")),
                 "pattern": ci(win(rs, 9, "pattern")), "answered": ci(a) if a is not None else None, "lifespan": ci(life(rs))}
    o = out[name]
    L.append(f"| {name} | {f(o['activity'])} | {f(o['reach'])} | {f(o['pattern'])} | "
             f"{f(o['answered']) if o['answered'] else '–'} | {o['lifespan'][0]:.0f} [{o['lifespan'][1]:.0f}, {o['lifespan'][2]:.0f}] |")
d = {k: ci(win(R["IQ"], 9, k) - win(R["IM"], 9, k)) for k in ("activity", "reach", "pattern")}
out["IQ-IM"] = d | {"answered": ci(ans(R["IQ"]) - ans(R["IM"])), "lifespan": ci(life(R["IQ"]) - life(R["IM"]))}
L += ["", "## Readings", "",
      f"1. **Dreams now reach waking life** (IQ − IM, last window): reach {f(d['reach'])}; pattern {f(d['pattern'])}; activity {f(d['activity'])}",
      f"2. **It goes to look** (answered within 500 steps): IQ questions {f(out['IQ']['answered'])} against IM's random blocks "
      f"{f(out['IM']['answered'])}; IQ − IM {f(out['IQ-IM']['answered'])}",
      f"3. **No harm to skill** (IQ − IM lifespan after the room): {f(out['IQ-IM']['lifespan'])}",
      "", f"Questions posed per IQ stay: {[len(r['questions']) for r in R['IQ']]}"]
(HERE / "analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
(HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
