"""WS frozen analysis (questions.md), written before any data -> results.md, summary.json.

  python analyse_ws.py OUT_DIR
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
BRAINS = ["B0", "Bc", "Bu", "Br", "Bm", "Brm", "Bp", "Bx"]
SEEDS = list(range(1, 49))
DAYS = ["1", "2", "3", "5", "7", "10", "15", "30", "45", "60"]
IDX = np.random.default_rng(20261113).integers(0, len(SEEDS), (10_000, len(SEEDS)))


def ci(x):
    x = np.asarray(x, float)
    b = x[IDX].mean(1)
    return float(x.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))


def f(c):
    return f"{c[0]:+.4f} [{c[1]:+.4f}, {c[2]:+.4f}]"


def main():
    out = Path(sys.argv[1])
    data, missing = {}, []
    for b in BRAINS:
        for s in SEEDS:
            p = out / f"{b}_seed_{s}.json"
            if p.exists():
                data[(b, s)] = json.loads(p.read_text(encoding="utf-8"))
            else:
                missing.append(p.name)
    checks_ok = (HERE / "checks.log").exists() and (HERE / "checks.log").read_text().strip().endswith("All: PASS")
    L = ["# WS results (the frozen analysis, analyse_ws.py)", "", "## Validity", "",
         f"- Code checks (All: PASS): **{'yes' if checks_ok else 'NO'}**",
         f"- All {len(BRAINS) * len(SEEDS)} runs present: **{'yes' if not missing else 'NO'}**", ""]
    if not checks_ok or missing:
        L += ["**NOT VALID.**"]
        (out / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return

    def sk(b, d, key="success"):
        return np.array([data[(b, s)]["tests"][d][key] for s in SEEDS], float)

    def sh(b, d):
        return np.array([data[(b, s)]["show_tests"][d]["success"] for s in SEEDS], float)
    floor = max(sk(b, "30").mean() for b in BRAINS) < 0.05
    r1 = ci(sk("Br", "30") - sk("Bu", "30"))
    r2 = ci(sh("Bm", "30") - sh("B0", "30"))
    r3 = ci(sk("Brm", "30") - np.maximum(sk("Br", "30"), sk("Bm", "30")))
    r4 = ci(sk("Br", "30") - sk("B0", "30"))

    def w(c, guarded=True):
        if guarded and floor:
            return "floor: not readable"
        return "yes" if c[1] > 0 else "no"
    L += [f"- Floor (every brain's day-30 skill below 0.05): **{'YES' if floor else 'no'}**", "",
          "## Readings (frozen; n = 48 per brain)", "",
          f"1. **PRIMARY. Replaying showings helps, beyond the amount of copying** (Br - Bu, skill, day 30): {f(r1)} -> **{w(r1)}**",
          f"2. **A learned memory helps the child copy a sequence** (Bm - B0, after a showing, day 30): {f(r2)} -> **{w(r2, False)}**",
          f"3. **Both together beat either** (Brm - max(Br, Bm), skill, day 30): {f(r3)} -> **{w(r3)}**",
          f"4. **Replay beats the baseline** (Br - B0, skill, day 30): {f(r4)} -> **{w(r4)}**", "",
          "## Checks (reported)", ""]
    for a, b in (("Bx", "B0"), ("Bp", "B0"), ("Bc", "B0"), ("Bu", "B0"), ("Bm", "B0"), ("Brm", "B0")):
        L.append(f"- {a} - {b}, skill day 30: {f(ci(sk(a, '30') - sk(b, '30')))}; day 60: {f(ci(sk(a, '60') - sk(b, '60')))}")
    L += ["", "| brain | skill d7 | skill d30 | skill d60 | retention (d60 - d30) | after a showing d30 | after a showing d60 | partial d30 |",
          "|---|---|---|---|---|---|---|---|"]
    for b in BRAINS:
        L.append(f"| {b} | {sk(b, '7').mean():.3f} | {sk(b, '30').mean():.3f} | {sk(b, '60').mean():.3f} | "
                 f"{f(ci(sk(b, '60') - sk(b, '30')))} | {sh(b, '30').mean():.3f} | {sh(b, '60').mean():.3f} | "
                 f"{sk(b, '30', 'partial').mean():.3f} |")
    reach = [b for b in BRAINS if sk(b, "30").mean() >= 0.5]
    L += ["", f"- Target (skill 0.5 or more by day 30): {', '.join(reach) if reach else 'none'}", "",
          "## Skill by day (full box, mean over 48)", "", "| brain | " + " | ".join(DAYS) + " |", "|---|" + "---|" * len(DAYS)]
    for b in BRAINS:
        L.append(f"| {b} | " + " | ".join(f"{sk(b, d).mean():.3f}" for d in DAYS) + " |")
    (out / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    (out / "summary.json").write_text(json.dumps({"r1": r1, "r2": r2, "r3": r3, "r4": r4, "floor": bool(floor)}, indent=1))
    print("\n".join(L))


if __name__ == "__main__":
    main()
