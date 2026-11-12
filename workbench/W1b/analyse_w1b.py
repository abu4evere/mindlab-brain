"""W1b analysis (questions.md, W1b-frozen). Written before any run.

  python workbench/W1b/analyse_w1b.py        # writes results.md
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
OUT = HERE / "output"
NEG = ["G", "W", "W2", "H1", "H2", "Mm"]
LEARNED = ["F", "R", "Fimit"]
SEEDS = list(range(1, 17))
IDX = np.random.default_rng(20261116).integers(0, 16, (10_000, 16))
NAME = {"Mm": "M-", "Fimit": "F-imit"}


def measures(rows):
    det = [r for r in rows if r["detour"]]
    m = {"eff": float(np.mean([r["efficient"] for r in det])),
         "pocket": float(np.mean([r["efficient"] for r in det if r["family"] == "pocket"])),
         "control": float(np.mean([r["solved"] for r in rows if not r["detour"]])),
         "first3": float(np.mean([r["first3"] for r in det])),
         "ordinary": float(np.mean([r["efficient"] for r in det if r["set"] == "ordinary"])),
         "adversarial": float(np.mean([r["efficient"] for r in det if r["set"] == "adversarial"])),
         "solved_detour": float(np.mean([r["solved"] for r in det]))}
    return m


def reading(m, above_g):
    if m["eff"] >= 0.80 and m["pocket"] >= 0.70 and above_g:
        return "looks ahead"
    if m["control"] >= 0.80 and m["eff"] <= 0.60:
        return "reactive"
    return "mixed"


def ci(x):
    x = np.asarray(x, float)
    b = x[IDX].mean(1)
    return float(x.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))


def main():
    def load(n, s):
        return json.loads((OUT / f"{n}_seed_{s}.json").read_text())["rows"]
    missing = [n for n in NEG + ["B"] if not (OUT / f"{n}_seed_0.json").exists()]
    missing += [f"{n}:{s}" for n in LEARNED for s in SEEDS if not (OUT / f"{n}_seed_{s}.json").exists()]
    checks = (HERE / "checks.log").read_text() if (HERE / "checks.log").exists() else ""
    L = ["# W1b: the detour, seen (results)", "", "Frozen as `W1b-frozen`. run_w1b.py, analyse_w1b.py (written before "
         "any run).", "", "## Validity", "",
         f"- Code checks (All: PASS): **{'yes' if 'All: PASS' in checks else 'NO'}**",
         f"- All runs present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing)}**"]
    if missing or "All: PASS" not in checks:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    sm = {n: measures(load(n, 0)) for n in NEG + ["B"]}
    g_eff = sm["G"]["eff"]
    rd = {n: reading(m, m["eff"] > g_eff) for n, m in sm.items()}
    valid = rd["B"] == "looks ahead" and all(rd[n] != "looks ahead" for n in NEG)
    L += [f"- B looks ahead: **{'yes' if rd['B'] == 'looks ahead' else 'NO'}**; none of the six negative controls "
          f"does: **{'yes' if all(rd[n] != 'looks ahead' for n in NEG) else 'NO'}**",
          f"- **{'Valid.' if valid else 'NOT VALID: nothing is concluded.'}**", "",
          "## Scripted brains (one run each)", "",
          "| brain | efficient detour | ordinary | adversarial | pocket | first 3 moves | detours solved at all | "
          "control | reading |", "|---|---|---|---|---|---|---|---|---|"]
    for n in NEG + ["B"]:
        m = sm[n]
        L.append(f"| {NAME.get(n, n)} | {m['eff']:.3f} | {m['ordinary']:.3f} | {m['adversarial']:.3f} | "
                 f"{m['pocket']:.3f} | {m['first3']:.3f} | {m['solved_detour']:.3f} | {m['control']:.3f} | {rd[n]} |")
    L += ["", "## Learning brains (16 seeds; mean [95% bootstrap])", "",
          "| brain | efficient detour | ordinary | adversarial | pocket | first 3 moves | control | eff - G | reading |",
          "|---|---|---|---|---|---|---|---|---|"]
    for n in LEARNED:
        ms = [measures(load(n, s)) for s in SEEDS]
        mean = {k: float(np.mean([m[k] for m in ms])) for k in ms[0]}
        dg = ci([m["eff"] - g_eff for m in ms])
        r = reading(mean, dg[1] > 0) if valid else "-"
        f = lambda k: "{:.3f} [{:.3f}, {:.3f}]".format(*ci([m[k] for m in ms]))  # noqa: E731
        L.append(f"| {NAME.get(n, n)} | {f('eff')} | {f('ordinary')} | {f('adversarial')} | {f('pocket')} | "
                 f"{f('first3')} | {f('control')} | {dg[0]:+.3f} [{dg[1]:+.3f}, {dg[2]:+.3f}] | **{r}** |")
    L += ["", "Rules (frozen): 'looks ahead' = efficient detour success (within 1.15 x the shortest) >= 0.80, pocket "
          ">= 0.70, above G's; 'reactive' = control >= 0.80 and efficient detour <= 0.60; else 'mixed'. Valid only if B "
          "looks ahead and none of G, W, W2, H1, H2, M- does. Even a pass is behaviour, not proof of an internal "
          "look-ahead.", ""]
    text = "\n".join(L) + "\n"
    (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
