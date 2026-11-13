"""W1e analysis (questions.md, W1e-frozen). Written before any training.

  python workbench/W1e/analyse_w1e.py        # writes results.md
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
OUT = HERE / "output"
W1D = HERE.parent / "W1d" / "output"
IDX16 = np.random.default_rng(20261121).integers(0, 16, (10_000, 16))
IDX8 = np.random.default_rng(20261121).integers(0, 8, (10_000, 8))


def ci(x):
    x = np.asarray(x, float)
    idx = IDX16 if len(x) == 16 else IDX8
    b = x[idx].mean(1)
    return float(x.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))


def m_of(r, g_eff=0.0):
    det = [x for x in r["test"] if x["detour"]]
    mdet = [x for x in r["map_readout"] if x["detour"]]
    return {"eff": np.mean([x["efficient"] for x in det]),
            "pocket": np.mean([x["efficient"] for x in det if x["family"] == "pocket"]),
            "control": np.mean([x["solved"] for x in r["test"] if not x["detour"]]),
            "empty": np.mean([x["solved"] for x in r["empty"]]),
            "held_eff": np.mean([x["efficient"] for x in r["held"] if x["detour"]]),
            "moving": np.mean([x["efficient"] for x in r["moving"]]),
            "map_eff": np.mean([x["efficient"] for x in mdet]),
            "map_pocket": np.mean([x["efficient"] for x in mdet if x["family"] == "pocket"]),
            "value_corr": r["value_corr"], "step_acc": r["step_accuracy"], "gap": r["gap_mean"],
            "near_tie": r["near_tie_share"]}


def main():
    checks = (HERE / "checks.log").read_text() if (HERE / "checks.log").exists() else ""
    w1b = json.loads((HERE.parent / "W1b" / "output" / "G_seed_0.json").read_text())["rows"]
    g_eff = float(np.mean([r["efficient"] for r in w1b if r["detour"]]))
    need = [f"{k}_seed_{s}" for k in ("V", "Vp") for s in range(1, 17)] + \
        [f"{k}_150k_seed_{s}" for k in ("V", "Vp") for s in range(1, 9)]
    missing = [n for n in need if not (OUT / f"{n}.json").exists()]
    L = ["# W1e: a planner that cannot cut corners (results)", "", "Frozen as `W1e-frozen`. run_w1e.py, analyse_w1e.py "
         "(written before any training).", "", "## Validity", "",
         f"- Code checks (All: PASS): **{'yes' if 'All: PASS' in checks else 'NO'}**",
         f"- All 48 runs present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing)}**"]
    if missing or "All: PASS" not in checks:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    run = lambda n: json.loads((OUT / f"{n}.json").read_text())  # noqa: E731
    rep = all(run(f"V_seed_{s}")["test"] == json.loads((W1D / f"V_seed_{s}.json").read_text())["test"]
              for s in range(1, 17))
    L += [f"- V's 30,000-episode results equal W1d's for every seed (replication): **{'yes' if rep else 'NO'}**", ""]
    keys = [("eff", "efficient detour"), ("pocket", "pocket"), ("control", "control"), ("empty", "empty room"),
            ("held_eff", "held-out detour"), ("moving", "moving food"), ("map_eff", "map read-out: efficient detour"),
            ("map_pocket", "map read-out: pocket"), ("value_corr", "value-map correlation"),
            ("step_acc", "step accuracy (detours)"), ("gap", "mean gap between the two best scores"),
            ("near_tie", "share of near-ties (gap < 0.05)")]
    for tag, seeds, title in (("", range(1, 17), "30,000 episodes (16 seeds)"),
                              ("_150k", range(1, 9), "150,000 episodes (8 seeds, secondary)")):
        mv = [m_of(run(f"V{tag}_seed_{s}")) for s in seeds]
        mp = [m_of(run(f"Vp{tag}_seed_{s}")) for s in seeds]
        L += [f"## {title}: mean [95% bootstrap]", "", "| measure | V | V+ | V+ - V |", "|---|---|---|---|"]
        for k, lab in keys:
            a, b = ci([m[k] for m in mv]), ci([m[k] for m in mp])
            dd = ci([y[k] - x[k] for x, y in zip(mv, mp)])
            L.append(f"| {lab} | {a[0]:.3f} [{a[1]:.3f}, {a[2]:.3f}] | {b[0]:.3f} [{b[1]:.3f}, {b[2]:.3f}] | "
                     f"{dd[0]:+.3f} [{dd[1]:+.3f}, {dd[2]:+.3f}] |")
        for name, ms in (("V", mv), ("V+", mp)):
            mean = {k: float(np.mean([m[k] for m in ms])) for k in ms[0]}
            lo = ci([m["eff"] - g_eff for m in ms])[1]
            rd = ("looks ahead" if mean["eff"] >= 0.80 and mean["pocket"] >= 0.70 and lo > 0 else
                  "reactive" if mean["control"] >= 0.80 and mean["eff"] <= 0.60 else "mixed")
            L.append(f"- {name}: **{rd}**; map read-out above the head by {mean['map_eff'] - mean['eff']:+.3f}"
                     f"{' (the read-out is the bottleneck)' if name == 'V+' and mean['map_eff'] - mean['eff'] > 0.10 else ''}")
        if tag == "":
            pm = ci([y["eff"] - x["eff"] for x, y in zip(mv, mp)])
            L += ["", f"**The plus matters** (V+ - V, efficient detour): {pm[0]:+.3f} [{pm[1]:+.3f}, {pm[2]:+.3f}] -> "
                  f"**{'yes' if pm[1] > 0 else 'no'}**"]
        L.append("")
    L += ["Rules (frozen; W1b's). Even a pass is learned planning inside an engineered structure, and behaviour, not "
          "proof of an inner look-ahead.", ""]
    (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
