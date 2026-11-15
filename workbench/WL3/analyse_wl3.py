"""WL3 analysis (descriptive; questions.md). 95% bootstrap intervals over 24 seeds (numpy seed 20261126, 10,000
resamples; paired by seed). Writes analysis.md and analysis.json."""
import json
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
WORLDS, ARMS, SIZES, SEEDS, B = ("K6L2", "K24L2", "K6L3"), ("L0", "L2", "Linf"), (32, 128), range(1, 25), 10_000
IDX = np.random.default_rng(20261126).integers(0, len(SEEDS), (B, len(SEEDS)))
R = {(w, a, n): [json.loads((HERE / "output" / f"{w}_{a}_{n}_seed_{s}.json").read_text()) for s in SEEDS]
     for w in WORLDS for a in ARMS for n in SIZES}
KEYS = {"day 15": lambda r: r["tests"]["15"], "day 30": lambda r: r["tests"]["30"], "day 60": lambda r: r["tests"]["60"],
        "after showing 30": lambda r: r["show30"], "food": lambda r: r["food"]}


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3)]


def vals(w, a, n, k):
    return np.array([KEYS[k](r) for r in R[(w, a, n)]], float)


f = lambda t: f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"
out = {"means": {}, "diffs": {}, "floor": {}}
L = ["# WL3 analysis (from analyse_wl3.py; 24 children per cell; means)", "",
     "| world | arm | size | " + " | ".join(KEYS) + " |", "|---|---|---|" + "---|" * len(KEYS)]
for w in WORLDS:
    for n in SIZES:
        for a in ARMS:
            m = {k: ci(vals(w, a, n, k)) for k in KEYS}
            out["means"][f"{w}-{a}-{n}"] = m
            L.append(f"| {w} | {a} | {n} | " + " | ".join((f"{m[k][0]:.0f}" if k == "food" else f"{m[k][0]:.3f}") for k in KEYS) + " |")
    out["floor"][w] = all(out["means"][f"{w}-{a}-{n}"]["day 60"][0] < 0.10 for a in ARMS for n in SIZES)
L += ["", "Floor rule (every arm at both sizes below 0.10 at day 60 -> not readable): " +
      ", ".join(f"{w}: {'NOT READABLE' if v else 'readable'}" for w, v in out["floor"].items()), "",
      "| paired difference | day 30 | day 60 |", "|---|---|---|"]
for w in WORLDS:
    for n in SIZES:
        for a in ("Linf", "L2"):
            d = {k: ci(vals(w, a, n, k) - vals(w, "L0", n, k)) for k in ("day 30", "day 60")}
            out["diffs"][f"{w} {a}-{n} − L0-{n}"] = d
            L.append(f"| {w} {a}-{n} − L0-{n} | {f(d['day 30'])} | {f(d['day 60'])} |")
(HERE / "analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
(HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
