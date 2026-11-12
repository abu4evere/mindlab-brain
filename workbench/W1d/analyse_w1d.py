"""W1d analysis (questions.md, W1d-frozen). Written before any training.

  python workbench/W1d/analyse_w1d.py        # writes results.md
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
OUT = HERE / "output"
BRAINS = ["V", "V1", "Vm", "Vac"]
SEEDS = list(range(1, 17))
IDX = np.random.default_rng(20261119).integers(0, 16, (10_000, 16))
NAME = {"Vac": "V-ac"}


def m_of(r, g_eff):
    t = r["test"]
    det = [x for x in t if x["detour"]]
    m = {"eff": np.mean([x["efficient"] for x in det]),
         "pocket": np.mean([x["efficient"] for x in det if x["family"] == "pocket"]),
         "control": np.mean([x["solved"] for x in t if not x["detour"]]),
         "empty": np.mean([x["solved"] for x in r["empty"]]),
         "held_eff": np.mean([x["efficient"] for x in r["held"] if x["detour"]]),
         "moving": np.mean([x["efficient"] for x in r["moving"]]),
         "first3": np.mean([x["first3"] for x in det])}
    m["eff_g"] = m["eff"] - g_eff
    return {k: float(v) for k, v in m.items()}


def ci(x):
    x = np.asarray(x, float)
    b = x[IDX[:, :len(x)] % len(x)].mean(1)
    return float(x.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))


def main():
    checks = (HERE / "checks.log").read_text() if (HERE / "checks.log").exists() else ""
    w1b = json.loads((HERE.parent / "W1b" / "output" / "G_seed_0.json").read_text())["rows"]
    g_eff = float(np.mean([r["efficient"] for r in w1b if r["detour"]]))
    missing = [f"{b}:{s}" for b in BRAINS for s in SEEDS if not (OUT / f"{b}_seed_{s}.json").exists()]
    L = ["# W1d: thinking ahead (results)", "", "Frozen as `W1d-frozen`. run_w1d.py, analyse_w1d.py (written before "
         "any training).", "", "## Validity", "",
         f"- Code checks (All: PASS): **{'yes' if 'All: PASS' in checks else 'NO'}**",
         f"- W1b's scripted controls (valid; G's efficient detour {g_eff:.3f}) are the reference.",
         f"- All 64 main runs present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing)}**", ""]
    if missing or "All: PASS" not in checks:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    runs = {b: [json.loads((OUT / f"{b}_seed_{s}.json").read_text()) for s in SEEDS] for b in BRAINS}
    ms = {b: [m_of(r, g_eff) for r in runs[b]] for b in BRAINS}
    L += ["## The brains (30,000 episodes; 16 seeds; mean [95% bootstrap])", "",
          "| brain | efficient detour | pocket | control | empty room | held-out detour | moving food | first 3 | "
          "navigates | reading |", "|---|---|---|---|---|---|---|---|---|---|"]
    for b in BRAINS:
        mean = {k: float(np.mean([m[k] for m in ms[b]])) for k in ms[b][0]}
        lo_g = ci([m["eff_g"] for m in ms[b]])[1]
        rd = ("looks ahead" if mean["eff"] >= 0.80 and mean["pocket"] >= 0.70 and lo_g > 0 else
              "reactive" if mean["control"] >= 0.80 and mean["eff"] <= 0.60 else "mixed")
        nav = mean["control"] >= 0.80 and mean["empty"] >= 0.90
        f = lambda k: "{:.3f} [{:.3f}, {:.3f}]".format(*ci([m[k] for m in ms[b]]))  # noqa: E731
        L.append(f"| {NAME.get(b, b)} | {f('eff')} | {f('pocket')} | {f('control')} | {f('empty')} | {f('held_eff')} | "
                 f"{f('moving')} | {mean['first3']:.3f} | **{'yes' if nav else 'no'}** | **{rd}** |")
    it = ci([a["eff"] - b["eff"] for a, b in zip(ms["V"], ms["V1"])])
    mx = ci([a["eff"] - b["eff"] for a, b in zip(ms["V"], ms["Vm"])])
    L += ["", "## Readings (frozen)", "",
          f"- **Iteration matters** (V - V1, efficient detour): {it[0]:+.3f} [{it[1]:+.3f}, {it[2]:+.3f}] -> "
          f"**{'yes' if it[1] > 0 else 'no'}**",
          f"- **The max matters** (V - Vm): {mx[0]:+.3f} [{mx[1]:+.3f}, {mx[2]:+.3f}] -> **{'yes' if mx[1] > 0 else 'no'}**",
          "", "## The value map (mean Spearman correlation with -(true distance), test layouts)", ""]
    for b in ("V", "V1", "Vm"):
        L.append(f"- {b}: {np.mean([r['value_corr'] for r in runs[b]]):.3f}")
    L += ["", "## The K sweep (V, test time): efficient detour by K, and by the layout's shortest path", "",
          "| K | all detours | shortest <= 10 | 11-15 | > 15 |", "|---|---|---|---|---|"]
    for k in ["1", "5", "10", "15", "20", "30"]:
        rows = [x for r in runs["V"] for x in r["k_sweep"][k] if x["detour"]]
        def part(lo, hi):
            sel = [x["efficient"] for x in rows if lo <= x["shortest"] <= hi]
            return f"{np.mean(sel):.3f} (n {len(sel)})" if sel else "-"
        L.append(f"| {k} | {np.mean([x['efficient'] for x in rows]):.3f} | {part(0, 10)} | {part(11, 15)} | "
                 f"{part(16, 99)} |")
    L += ["", "## The 100,000-episode check (V-ac, 8 seeds)", ""]
    fs = [OUT / f"Vac_100k_seed_{s}.json" for s in range(1, 9)]
    if all(p.exists() for p in fs):
        m8 = [m_of(json.loads(p.read_text()), g_eff) for p in fs]
        L.append("- " + ", ".join(f"{k} {np.mean([m[k] for m in m8]):.3f}" for k in
                                  ("eff", "pocket", "control", "empty", "moving")))
    else:
        L.append("- (not all present)")
    L += ["", "Rules (frozen, W1b's and W1c's). Even a pass is learned planning inside an engineered planning structure, "
          "and behaviour, not proof of an inner look-ahead.", ""]
    text = "\n".join(L) + "\n"
    (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
