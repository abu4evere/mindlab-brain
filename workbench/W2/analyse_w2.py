"""W2 analysis (questions.md, W2-frozen). Written before any training.

  python workbench/W2/analyse_w2.py        # writes results.md
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
OUT = HERE / "output"
SEEDS = range(1, 17)
IDX = np.random.default_rng(20261122).integers(0, 16, (10_000, 16))
REACTIVE = ("B0", "G", "W", "W2", "H2", "M-")


def ci(x, idx=IDX):
    x = np.asarray(x, float)
    b = x[idx].mean(1)
    return float(x.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))


def lci(per_layout):
    """Bootstrap over layouts (2,000 draws) of a per-layout quantity (already averaged over seeds)."""
    x = np.asarray(per_layout, float)
    idx = np.random.default_rng(20261122).integers(0, len(x), (2_000, len(x)))
    b = x[idx].mean(1)
    return float(x.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))


def f(t):
    return f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"


def fd(t):
    return f"{t[0]:+.3f} [{t[1]:+.3f}, {t[2]:+.3f}]"


def eff(rows):
    return float(np.mean([r["efficient"] for r in rows]))


def regret(rows, ref):
    v = [r["steps"] - b["steps"] for r, b in zip(rows, ref) if r["solved"] and b["solved"]]
    return float(np.mean(v)) if v else float("nan")


def main():
    checks = (HERE / "checks.log").read_text() if (HERE / "checks.log").exists() else ""
    need = [f"{k}_seed_{s}" for k in ("M", "M0", "R") for s in SEEDS]
    missing = [n for n in need if not (OUT / f"{n}.json").exists()]
    have_ctl = (OUT / "controls.json").exists()
    L = ["# W2: planning on what one remembers (results)", "",
         "Frozen as `W2-frozen`. world2.py, brains2.py, run_w2.py, analyse_w2.py (written before any training).", "",
         "## Validity", "",
         f"- Code checks (All: PASS): **{'yes' if 'All: PASS' in checks else 'NO'}**",
         f"- All 48 runs present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing)}**",
         f"- Scripted controls run: **{'yes' if have_ctl else 'NO'}**"]
    if missing or "All: PASS" not in checks or not have_ctl:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    ctl = json.loads((OUT / "controls.json").read_text())
    bp_fam = eff(ctl["Bp"]["detour_fam"])
    worst_reactive = max(eff(ctl[b]["detour_new"]) for b in REACTIVE)
    valid = bp_fam >= 0.90 and worst_reactive <= 0.20
    L += [f"- Bp, familiar efficient detour {bp_fam:.3f} (at least 0.90): **{'yes' if bp_fam >= 0.90 else 'NO'}**",
          f"- B0 and the reactive controls, new-room efficient detour at most 0.20 (highest {worst_reactive:.3f}): "
          f"**{'yes' if worst_reactive <= 0.20 else 'NO'}**",
          f"- **W2 is {'valid' if valid else 'INVALID'}.**", "",
          "## The scripted controls", "", "| brain | detour new | detour familiar | control new | control familiar | "
          "empty | look-alike correct side |", "|---|---|---|---|---|---|---|"]
    for b, r in ctl.items():
        L.append(f"| {b} | {eff(r['detour_new']):.3f} | {eff(r['detour_fam']):.3f} | {eff(r['control_new']):.3f} | "
                 f"{eff(r['control_fam']):.3f} | {eff(r['empty']):.3f} | {np.mean(r['pairs']):.3f} |")
    run = {(k, s): json.loads((OUT / f"{k}_seed_{s}.json").read_text()) for k in ("M", "M0", "R") for s in SEEDS}

    def per_seed(k, fn):
        return [fn(run[(k, s)]) for s in SEEDS]
    meas = [("efficient detour, new room", lambda r: eff(r["detour_new"])),
            ("efficient detour, familiar room", lambda r: eff(r["detour_fam"])),
            ("the tour's use (familiar - new)", lambda r: eff(r["detour_fam"]) - eff(r["detour_new"])),
            ("control, new room", lambda r: eff(r["control_new"])),
            ("control, familiar room", lambda r: eff(r["control_fam"])),
            ("empty room", lambda r: eff(r["empty"])),
            ("look-alike: correct side", lambda r: float(np.mean(r["pairs"]))),
            ("regret vs Bp, detour new (steps)", lambda r: regret(r["detour_new"], ctl["Bp"]["detour_new"])),
            ("regret vs Bp, detour familiar (steps)", lambda r: regret(r["detour_fam"], ctl["Bp"]["detour_fam"]))]
    L += ["", "## The learned brains (16 seeds, 150,000 episodes): mean [95% bootstrap over seeds]", "",
          "| measure | M | M0 | R |", "|---|---|---|---|"]
    for lab, fn in meas:
        cells = []
        for k in ("M", "M0", "R"):
            v = [x for x in per_seed(k, fn) if not np.isnan(x)]
            cells.append(f(ci(v, np.random.default_rng(20261122).integers(0, len(v), (10_000, len(v)))))
                         if v else "–")
        L.append(f"| {lab} | " + " | ".join(cells) + " |")
    L.append(f"| value-map correlation (true map) | {f(ci(per_seed('M', lambda r: r['value_corr'])))} | "
             f"{f(ci(per_seed('M0', lambda r: r['value_corr'])))} | – |")
    m_fam = per_seed("M", lambda r: eff(r["detour_fam"]))
    m_er = per_seed("M", lambda r: eff(r["detour_erase"]))
    m_sh = per_seed("M", lambda r: eff(r["detour_shuffle"]))
    L += ["", "### M's memory probes (familiar detours)", "",
          f"- M: {f(ci(m_fam))}; M-erase: {f(ci(m_er))}; M-shuffle: {f(ci(m_sh))}",
          f"- M - M-erase: {fd(ci(np.subtract(m_fam, m_er)))}; M - M-shuffle: {fd(ci(np.subtract(m_fam, m_sh)))}"]
    # the frozen readings
    mm0 = ci(np.subtract(m_fam, per_seed("M0", lambda r: eff(r["detour_fam"]))))
    mr = ci(np.subtract(m_fam, per_seed("R", lambda r: eff(r["detour_fam"]))))
    pairs = ci(per_seed("M", lambda r: float(np.mean(r["pairs"]))))
    mer = ci(np.subtract(m_fam, m_er))
    uses = float(np.mean(m_fam))
    L += ["", "## The frozen readings", "",
          f"- **Memory matters** (M - M0, familiar efficient detour): {fd(mm0)} -> **{'yes' if mm0[1] > 0 else 'no'}**",
          f"- **Decisions follow memory:** M's look-alike correct side {f(pairs)} (lower bound above 0.5: "
          f"{'yes' if pairs[1] > 0.5 else 'no'}); M - M-erase {fd(mer)} (above 0: {'yes' if mer[1] > 0 else 'no'}) "
          f"-> **{'yes' if pairs[1] > 0.5 and mer[1] > 0 else 'no'}**",
          f"- **The given map beats a learned memory** (an architecture comparison; M - R, familiar): {fd(mr)} -> "
          f"**{'yes' if mr[1] > 0 else 'no'}**",
          f"- **Uses what it knows** (M familiar >= 0.80 x Bp's {bp_fam:.3f} = {0.8 * bp_fam:.3f}): M {uses:.3f}, "
          f"absolute gap to Bp {uses - bp_fam:+.3f} -> **{'yes' if uses >= 0.8 * bp_fam else 'no'}**"]
    # secondary: bootstrap over layouts
    def lay_mean(k, key):
        return np.mean([[float(x["efficient"]) for x in run[(k, s)][key]] for s in SEEDS], 0)
    pair_m = np.mean([[np.mean(p) for p in run[("M", s)]["pairs"]] for s in SEEDS], 0)
    L += ["", "## Secondary: bootstrap over layouts (2,000 draws; per-layout means over seeds)", "",
          f"- M - M0, familiar: {fd(lci(lay_mean('M', 'detour_fam') - lay_mean('M0', 'detour_fam')))}",
          f"- M - R, familiar: {fd(lci(lay_mean('M', 'detour_fam') - lay_mean('R', 'detour_fam')))}",
          f"- M - M-erase: {fd(lci(lay_mean('M', 'detour_fam') - lay_mean('M', 'detour_erase')))}",
          f"- M's look-alike correct side (over the 40 pairs): {f(lci(pair_m))}", "",
          "M's memory is engineered (a fixed writer); its planner is learned. Behaviour, not proof of an inner "
          "look-ahead.", ""]
    (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
