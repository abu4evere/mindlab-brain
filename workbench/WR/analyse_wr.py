"""WR analysis (descriptive; questions.md, Measures and Readings), written before the data. 95% bootstrap intervals
over 48 seeds (numpy seed 20261126, 10,000 resamples; paired by seed). Reads output/<world>_<arm>_<n>_seed_<s>.json.
Writes analysis.md and analysis.json.

  python analyse_wr.py
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
SIZES, B = (128, 32), 10_000
IDX = np.random.default_rng(20261126).integers(0, 48, (B, 48))
ARMS_C = ("Base", "L", "TY", "TYR", "LTYR", "LTY", "LYR", "LTR")
ARMS_S = ("L0", "L", "TYR", "LTYR")
SEEDS = {"change": range(1001, 1049), "stable": range(1, 49)}
A, Bk = (0, 1, 2), (3, 4, 5)
READS = {"A30": (30, A), "A38": (38, A), "A45": (45, A), "B45": (45, Bk), "B53": (53, Bk), "B60": (60, Bk)}
KEYS_C = list(READS) + ["stale33", "stale48", "food"]
DIFF_C = ("A45", "B60", "A30", "B45", "food")
KEYS_S = ("day 7", "day 15", "day 30", "day 60", "after showing 30", "food")


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3)]


def val_c(r, key):
    if key == "food":
        return r["food"]
    if key.startswith("stale"):
        d, ks = (33, A) if key == "stale33" else (48, Bk)
        return float(np.mean([r["tests"][str(d)]["stale"][k] for k in ks]))
    d, ks = READS[key]
    return float(np.mean([r["tests"][str(d)]["success"][k] for k in ks]))


def val_s(r, key):
    if key == "food":
        return r["food"]
    if key == "after showing 30":
        return r["show30"]
    return r["tests"][key.split()[1]]


def load(world, arm, n):
    return [json.loads((HERE / "output" / f"{world}_{arm}_{n}_seed_{s}.json").read_text()) for s in SEEDS[world]]


f = lambda t: f"{t[0]:+.3f} [{t[1]:+.3f}, {t[2]:+.3f}]"
fm = lambda x, k: f"{x:.0f}" if k == "food" else f"{x:.2f}"
out = {"means": {}, "diffs": {}, "readings": {}}
L = ["# WR analysis (from analyse_wr.py; 48 children per cell; paired differences: mean [95% interval])"]

for n in SIZES:
    R = {a: load("change", a, n) for a in ARMS_C}
    V = {a: {k: np.array([val_c(r, k) for r in R[a]]) for k in KEYS_C} for a in ARMS_C}
    L += ["", f"## Changing world, size {n}: means", "", "| arm | " + " | ".join(KEYS_C) + " |", "|---" * (len(KEYS_C) + 1) + "|"]
    for a in ARMS_C:
        out["means"][f"change {a}-{n}"] = {k: ci(V[a][k]) for k in KEYS_C}
        L.append(f"| {a} | " + " | ".join(fm(V[a][k].mean(), k) for k in KEYS_C) + " |")
    L += ["", f"## Changing world, size {n}: differences", "", "| difference | " + " | ".join(DIFF_C) + " |", "|---" * (len(DIFF_C) + 1) + "|"]
    pairs = [("LTYR", "TYR"), ("LTYR", "LTY"), ("LTYR", "LYR"), ("LTYR", "LTR")] + [(a, "Base") for a in ARMS_C if a != "Base"]
    for a, b in pairs:
        d = {k: ci(V[a][k] - V[b][k]) for k in DIFF_C}
        out["diffs"][f"change {a}-{n} − {b}-{n}"] = d
        L.append(f"| {a} − {b} | " + " | ".join(f(d[k]) for k in DIFF_C) + " |")

for n in SIZES:
    R = {a: load("stable", a, n) for a in ARMS_S}
    V = {a: {k: np.array([val_s(r, k) for r in R[a]]) for k in KEYS_S} for a in ARMS_S}
    L += ["", f"## Stable world, size {n}: means", "", "| arm | " + " | ".join(KEYS_S) + " |", "|---" * (len(KEYS_S) + 1) + "|"]
    for a in ARMS_S:
        out["means"][f"stable {a}-{n}"] = {k: ci(V[a][k]) for k in KEYS_S}
        L.append(f"| {a} | " + " | ".join(fm(V[a][k].mean(), k) for k in KEYS_S) + " |")
    L += ["", f"## Stable world, size {n}: differences", "", "| difference | " + " | ".join(KEYS_S) + " |", "|---" * (len(KEYS_S) + 1) + "|"]
    for a, b in (("LTYR", "L"), ("LTYR", "L0"), ("TYR", "L0"), ("TYR", "L")):
        d = {k: ci(V[a][k] - V[b][k]) for k in KEYS_S}
        out["diffs"][f"stable {a}-{n} − {b}-{n}"] = d
        L.append(f"| {a} − {b} | " + " | ".join(f(d[k]) for k in KEYS_S) + " |")

# Readings (questions.md): size 128 is the reading size; reading 4 at both sizes
D = out["diffs"]
lo = lambda key, k: D[key][k][1]
r1 = all(lo("change LTYR-128 − TYR-128", k) > -0.05 for k in ("A45", "B60", "A30", "B45"))
r2 = any(lo("change LTYR-128 − TYR-128", k) > 0 for k in ("A45", "B60"))
parts = {"L": "change LTYR-128 − TYR-128", "R": "change LTYR-128 − LTY-128", "T": "change LTYR-128 − LYR-128",
         "Y": "change LTYR-128 − LTR-128"}
earned = {p: any(lo(key, k) > 0 for k in DIFF_C) for p, key in parts.items()}
r3 = all(earned.values())
r4 = all(lo(f"stable LTYR-{n} − L-{n}", k) > -0.05 for n in SIZES for k in ("day 30", "day 60"))
m5 = out["means"]["stable TYR-128"]["day 30"][0]
r5 = m5 >= 0.50
out["readings"] = {"1 loses nothing": r1, "2 gains": r2, "3 each part earns its place": r3, "3 by part": earned,
                   "4 no cost in the stable world": r4, "5 replay alone cures the parrot": r5, "TYR-128 stable day 30": m5}
L += ["", "## Readings (size 128; reading 4 at both sizes)", "",
      f"1. The recipe loses nothing (LTYR − TYR lower bounds above −0.05 on A45, B60, A30, B45): **{'YES' if r1 else 'NO'}**",
      f"2. The recipe gains (LTYR − TYR lower bound above 0 on A45 or B60): **{'YES' if r2 else 'NO'}**",
      f"3. Each part earns its place: **{'YES' if r3 else 'NO'}** (" + ", ".join(f"{p}: {'yes' if v else 'no'}" for p, v in earned.items()) + ")",
      f"4. No cost in the stable world (LTYR − L lower bounds above −0.05 at days 30 and 60, both sizes): **{'YES' if r4 else 'NO'}**",
      f"5. Night replay alone cures the parrot (stable TYR-128 day 30 mean {m5:.3f} ≥ 0.50): **{'YES' if r5 else 'NO'}**"]
(HERE / "analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
(HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
