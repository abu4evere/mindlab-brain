"""WY analysis (descriptive; questions.md). 95% bootstrap intervals over 48 seeds (numpy seed 20261121, 10,000
resamples; paired by seed). Reads output/<ARM><SIZE>_seed_<s>.json. Writes analysis.md and analysis.json."""
import json
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
ARMS, SIZES = ("Base", "YS", "TBYS"), (128, 32)
SEEDS, B = range(1001, 1049), 10_000
IDX = np.random.default_rng(20261121).integers(0, len(SEEDS), (B, len(SEEDS)))
A, Bk = (0, 1, 2), (3, 4, 5)
READS = {"A30": (30, A), "A38": (38, A), "A45": (45, A), "B45": (45, Bk), "B53": (53, Bk), "B60": (60, Bk)}


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3)]


def val(r, key):
    if key == "food":
        return r["food"]
    if key.startswith("stale"):
        d, ks = (33, A) if key == "stale33" else (48, Bk)
        return float(np.mean([r["tests"][str(d)]["stale"][k] for k in ks]))
    d, ks = READS[key]
    return float(np.mean([r["tests"][str(d)]["success"][k] for k in ks]))


f = lambda t: f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"
KEYS = list(READS) + ["stale33", "stale48", "food"]
out, L = {"means": {}, "diffs": {}}, ["# WY analysis (from analyse_wy.py; 48 children per cell)"]
for n in SIZES:
    R = {a: [json.loads((HERE / "output" / f"{a}{n}_seed_{s}.json").read_text()) for s in SEEDS] for a in ARMS}
    L += ["", f"## Size {n}: means", "", "| arm | " + " | ".join(KEYS) + " |", "|---" * (len(KEYS) + 1) + "|"]
    for a in ARMS:
        out["means"][f"{a}{n}"] = {k: ci([val(r, k) for r in R[a]]) for k in KEYS}
        L.append(f"| {a} | " + " | ".join(
            (f"{out['means'][f'{a}{n}'][k][0]:.0f}" if k == "food" else f"{out['means'][f'{a}{n}'][k][0]:.2f}") for k in KEYS) + " |")
    L += ["", f"## Size {n}: each arm minus Base (paired; mean [95% interval])", "",
          "| arm − Base | A45 | B60 | A30 | B45 | food |", "|---|---|---|---|---|---|"]
    for a in ARMS[1:]:
        d = {k: ci(np.array([val(r, k) for r in R[a]]) - np.array([val(r, k) for r in R["Base"]]))
             for k in ("A45", "B60", "A30", "B45", "food")}
        out["diffs"][f"{a}{n}-Base{n}"] = d
        L.append(f"| {a} | " + " | ".join(f(d[k]) for k in ("A45", "B60", "A30", "B45", "food")) + " |")
    # TBYS - TB, with WM's TB children (same seeds, same code for TB's parts)
    RT = [json.loads((HERE.parent / "WM" / "output" / f"TB{n}_seed_{s}.json").read_text()) for s in SEEDS]
    d = {k: ci(np.array([val(r, k) for r in R["TBYS"]]) - np.array([val(r, k) for r in RT])) for k in ("A45", "B60", "A30", "B45", "food")}
    out["diffs"][f"TBYS{n}-TB{n}(WM)"] = d
    L.append(f"| TBYS − TB (WM) | " + " | ".join(f(d[k]) for k in ("A45", "B60", "A30", "B45", "food")) + " |")
(HERE / "analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
(HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
