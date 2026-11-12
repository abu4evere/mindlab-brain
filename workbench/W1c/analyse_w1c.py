"""W1c analysis (questions.md, W1c-frozen). Written before any training.

  python workbench/W1c/analyse_w1c.py        # writes results.md
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
OUT = HERE / "output"
BRAINS = ["E", "Eimit", "C", "Cimit", "Cdag"]
LONG = ["E", "C", "Cimit"]
SEEDS = list(range(1, 17))
IDX = np.random.default_rng(20261118).integers(0, 16, (10_000, 16))
NAME = {"Eimit": "E-imit", "Cimit": "C-imit", "Cdag": "C-dag"}


def measures(r, g_eff):
    t = r["test"]
    det = [x for x in t if x["detour"]]
    m = {"eff": np.mean([x["efficient"] for x in det]),
         "pocket": np.mean([x["efficient"] for x in det if x["family"] == "pocket"]),
         "control": np.mean([x["solved"] for x in t if not x["detour"]]),
         "first3": np.mean([x["first3"] for x in det]),
         "empty": np.mean([x["solved"] for x in r["empty"]]),
         "held_eff": np.mean([x["efficient"] for x in r["held"] if x["detour"]]),
         "held_control": np.mean([x["solved"] for x in r["held"] if not x["detour"]]),
         "acc_learn": r["imit_acc_learn"], "acc_test": r["imit_acc_test"]}
    m["eff_minus_g"] = m["eff"] - g_eff
    return {k: float(v) for k, v in m.items()}


def ci(x, idx=IDX):
    x = np.asarray(x, float)
    b = x[idx].mean(1)
    return float(x.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))


def main():
    checks = (HERE / "checks.log").read_text() if (HERE / "checks.log").exists() else ""
    w1b = json.loads((HERE.parent / "W1b" / "output" / "G_seed_0.json").read_text())["rows"]
    g_eff = float(np.mean([r["efficient"] for r in w1b if r["detour"]]))
    missing = [f"{b}:{s}" for b in BRAINS for s in SEEDS if not (OUT / f"{b}_seed_{s}.json").exists()]
    L = ["# W1c: spatial structure (results)", "", "Frozen as `W1c-frozen`. run_w1c.py, analyse_w1c.py (written before "
         "any training).", "", "## Validity", "",
         f"- Code checks (All: PASS): **{'yes' if 'All: PASS' in checks else 'NO'}**",
         f"- W1b's scripted controls (valid; G's efficient detour {g_eff:.3f}) are the reference.",
         f"- All 80 main runs present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing)}**", ""]
    if missing or "All: PASS" not in checks:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    L += ["## The brains at 30,000 episodes (16 seeds; mean [95% bootstrap])", "",
          "| brain | efficient detour | pocket | control | empty room | held-out detour | held-out control | "
          "first 3 | imitation acc. (learn / test) | navigates | reading |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for b in BRAINS:
        ms = [measures(json.loads((OUT / f"{b}_seed_{s}.json").read_text()), g_eff) for s in SEEDS]
        mean = {k: float(np.mean([m[k] for m in ms])) for k in ms[0]}
        lo_g = ci([m["eff_minus_g"] for m in ms])[1]
        if mean["eff"] >= 0.80 and mean["pocket"] >= 0.70 and lo_g > 0:
            rd = "looks ahead"
        elif mean["control"] >= 0.80 and mean["eff"] <= 0.60:
            rd = "reactive"
        else:
            rd = "mixed"
        nav = mean["control"] >= 0.80 and mean["empty"] >= 0.90
        f = lambda k: "{:.3f} [{:.3f}, {:.3f}]".format(*ci([m[k] for m in ms]))  # noqa: E731
        L.append(f"| {NAME.get(b, b)} | {f('eff')} | {f('pocket')} | {f('control')} | {f('empty')} | {f('held_eff')} | "
                 f"{f('held_control')} | {mean['first3']:.3f} | {mean['acc_learn']:.3f} / {mean['acc_test']:.3f} | "
                 f"**{'yes' if nav else 'no'}** | **{rd}** |")
    L += ["", "## The 100,000-episode check (secondary; 4 seeds)", "",
          "| brain | efficient detour | control | empty room | imitation acc. (test) |", "|---|---|---|---|---|"]
    for b in LONG:
        fs = [OUT / f"{b}_100k_seed_{s}.json" for s in range(1, 5)]
        if not all(p.exists() for p in fs):
            L.append(f"| {NAME.get(b, b)} | (not all present) | | | |")
            continue
        ms = [measures(json.loads(p.read_text()), g_eff) for p in fs]
        L.append(f"| {NAME.get(b, b)} | " + " | ".join(f"{np.mean([m[k] for m in ms]):.3f}"
                                                       for k in ("eff", "control", "empty", "acc_test")) + " |")
    L += ["", "Rules (frozen, W1b's): 'looks ahead' = efficient detour >= 0.80, pocket >= 0.70, above G's (lower bound "
          "over seeds above 0); 'reactive' = control >= 0.80 and efficient detour <= 0.60; else 'mixed'. 'Navigates' = "
          "control >= 0.80 and empty-room success >= 0.90. Even a pass is behaviour, not proof of an internal "
          "look-ahead.", ""]
    text = "\n".join(L) + "\n"
    (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
