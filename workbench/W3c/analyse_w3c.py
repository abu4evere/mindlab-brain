"""W3c's frozen analysis (questions.md, Readings), written before any data -> analysis.md / analysis.json.
Per run: the mean over its 50 test lives. Intervals: bootstrap over the 8 seeds (10,000 draws, numpy seed 20261129);
differences paired by seed."""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
W3O, W3BO, OUT = HERE.parent / "W3" / "output", HERE.parent / "W3b" / "output", HERE / "output"
SEEDS = range(1, 9)
IDX = np.random.default_rng(20261129).integers(0, 8, (10_000, 8))
MEAS = ("survived", "surv1000", "lifespan", "known_end", "hungry", "exhausted")


def life_vals(l):
    out = {m: l.get(m) for m in MEAS if m != "surv1000"}
    out["surv1000"] = 1.0 if l["lifespan"] >= 1000 else 0.0
    return out


def run_means(path):
    lives = json.loads(path.read_text())
    return {m: float(np.mean([life_vals(l)[m] for l in lives])) for m in MEAS}


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3)]


SRC = {"D3 (W3)": lambda s: W3O / f"test_D3_{s}.json", "D3i (W3)": lambda s: W3O / f"test_D3i_{s}.json",
       "YFR (W3b)": lambda s: W3BO / f"test_YFR_{s}.json", "F2": lambda s: OUT / f"test_F2_{s}.json",
       "G": lambda s: OUT / f"test_G_{s}.json", "GYFR": lambda s: OUT / f"test_GYFR_{s}.json",
       "Gi": lambda s: OUT / f"test_Gi_{s}.json", "Z0": lambda s: OUT / f"test_Z0_{s}.json"}
R = {k: [run_means(f(s)) for s in SEEDS if f(s).exists()] for k, f in SRC.items()}
f3 = lambda t: f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"
out = {"arms": {}, "step0c": {}, "readings": {}}
L = ["# W3c analysis (the frozen analysis, analyse_w3c.py)", "",
     "Per run: the mean over its 50 test lives; intervals: bootstrap over the 8 seeds (10,000 draws, seed 20261129).", "",
     "## Step 0c: W3's D3i with the gate (test only)", "", "| walk | survived to 3,000 | lifespan |", "|---|---|---|"]
s0 = [json.loads((OUT / f"step0_D3i_{s}.json").read_text()) for s in SEEDS if (OUT / f"step0_D3i_{s}.json").exists()]
for key, name in (("a", "(a) learned head"), ("b", "(b) greedy value walk"), ("c", "(c) one-step look-ahead")):
    sv = ci([np.mean([l["survived"] for l in r[key]]) for r in s0]) if s0 else [math.nan] * 3
    ls = ci([np.mean([l["lifespan"] for l in r[key]]) for r in s0]) if s0 else [math.nan] * 3
    out["step0c"][key] = {"survived": sv, "lifespan": ls, "n_runs": len(s0)}
    L.append(f"| {name} (n = {len(s0)}) | {f3(sv)} | {ls[0]:.0f} [{ls[1]:.0f}, {ls[2]:.0f}] |")
L += ["", "## Arms", "", "| arm | runs | survived to 3,000 | to 1,000 | lifespan | known@end | hungry | exhausted |",
      "|---|---|---|---|---|---|---|---|"]
for k, rs in R.items():
    if not rs:
        continue
    out["arms"][k] = {m: ci([r[m] for r in rs]) for m in MEAS} | {"n_runs": len(rs)}
    a = out["arms"][k]
    L.append(f"| {k} | {len(rs)} | {f3(a['survived'])} | {f3(a['surv1000'])} | {a['lifespan'][0]:.0f} "
             f"[{a['lifespan'][1]:.0f}, {a['lifespan'][2]:.0f}] | {a['known_end'][0]:.2f} | {a['hungry'][0]:.2f} | "
             f"{a['exhausted'][0]:.2f} |")


def diff(a, b, m):
    if len(R.get(a, [])) != 8 or len(R.get(b, [])) != 8:
        return None
    return ci([x[m] - y[m] for x, y in zip(R[a], R[b])])


learned_all_zero = all(out["arms"].get(k, {}).get("survived", [0])[0] == 0 for k in ("G", "GYFR", "Gi"))
m4 = "lifespan" if learned_all_zero else "survived"
best0 = max((out["step0c"][k]["survived"][0] for k in ("b", "c")), default=math.nan)
f2 = out["arms"].get("F2", {}).get("survived", [math.nan])[0]
r3 = [k for k in ("G", "GYFR", "Gi") if k in out["arms"] and out["arms"][k]["survived"][0] >= 0.5
      and out["arms"][k]["survived"][1] >= 0.3]
L += ["", "## Readings", "",
      f"1. **The gate un-drowns hunger** (D3i + gate, walk (b) or (c) survives >= 0.50): best {best0:.3f} -> "
      f"**{'YES' if best0 >= 0.5 else 'NO'}**",
      f"2. **The fair ceiling is reachable** (F2 >= 0.50): {f2:.3f} -> **{'YES' if f2 >= 0.5 else 'NO'}**",
      f"3. **A learned brain lives** (G, GYFR or Gi: mean >= 0.50, lower >= 0.30): **{'YES: ' + ', '.join(r3) if r3 else 'NO'}**",
      f"4. **The gate helps** (on {m4}{', since every learned survival is 0' if learned_all_zero else ''}):"]
for a, b in (("G", "D3 (W3)"), ("Gi", "D3i (W3)"), ("GYFR", "YFR (W3b)")):
    d = diff(a, b, m4)
    out["readings"][f"{a} - {b}"] = d
    L.append(f"   - {a} − {b}: {f3(d) if d else 'n/a'} -> {'YES' if d and d[1] > 0 else 'NO'}")
d5 = diff("G", "Z0", m4)
out["readings"]["G - Z0"] = d5
L.append(f"5. **Gate or quiet start** (G − Z0 on {m4}): {f3(d5) if d5 else 'n/a'}")
L += ["", "Secondary (survival to 1,000, paired):"]
for a, b in (("G", "D3 (W3)"), ("Gi", "D3i (W3)"), ("GYFR", "YFR (W3b)"), ("G", "Z0")):
    d = diff(a, b, "surv1000")
    L.append(f"- {a} − {b}: {f3(d) if d else 'n/a'}")
out["readings"].update(r1=best0, r2=f2, r3=r3, m4=m4)
(HERE / "analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
(HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
