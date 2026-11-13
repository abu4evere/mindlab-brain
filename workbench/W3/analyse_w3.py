"""W3's frozen analysis (questions.md, Readings), written before any data -> results.md.

  python analyse_w3.py
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
OUT = HERE / "output"
SEEDS = range(1, 9)
LEARNED = ("D3", "D2", "Dc", "D3i", "D3-")
MEAS = ("survived", "lifespan", "known500", "known_end", "found_share", "hungry", "exhausted")
B = 10_000


def run_means(lives):
    out = {}
    for m in MEAS:
        vals = [l[m] for l in lives if l[m] is not None and not (isinstance(l[m], float) and math.isnan(l[m]))]
        out[m] = float(np.mean(vals)) if vals else math.nan
    out["n_lives"] = len(lives)
    out["n_with_events"] = sum(1 for l in lives if l["events"] > 0)
    return out


def load():
    runs = {}
    for k in LEARNED:
        runs[k] = {}
        for s in SEEDS:
            p = OUT / f"test_{k}_{s}.json"
            if p.exists():
                runs[k][s] = run_means(json.loads(p.read_text()))
    refs = {n: run_means(json.loads((OUT / f"test_{n}.json").read_text())) for n in ("Rand", "Script")
            if (OUT / f"test_{n}.json").exists()}
    return runs, refs


def boot(vals):
    rng = np.random.default_rng(20261113)
    v = np.asarray(vals, float)
    idx = rng.integers(0, len(v), size=(B, len(v)))
    means = np.nanmean(v[idx], axis=1)
    return float(np.nanmean(v)), float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def paired(runs, a, b, m):
    seeds = [s for s in SEEDS if s in runs[a] and s in runs[b]]
    return boot([runs[a][s][m] - runs[b][s][m] for s in seeds]), len(seeds)


def collapsed(seed):
    p = OUT / f"D3_{seed}_norms.json"
    if not p.exists():
        return None
    norms = json.loads(p.read_text())
    if not norms:
        return None
    last = norms[-1]
    top = max(last["Ws"], last["Wf"], last["Wc"])
    return bool(last["Wc"] < 0.1 * top) if top > 0 else True


def fmt(t):
    return f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"


def main():
    runs, refs = load()
    L = ["# W3 results (the frozen analysis, analyse_w3.py)", ""]
    L.append("Per run: the mean over its 50 test lives; intervals: bootstrap over the training seeds (10,000 draws, "
             "seed 20261113). n = runs x 50 lives.")
    L.append("")
    L.append("| brain | runs | survived to 3,000 | lifespan | known@500 | known@end | found share | hungry | exhausted |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for k in LEARNED:
        if not runs[k]:
            continue
        cells = [fmt(boot([runs[k][s][m] for s in runs[k]])) for m in MEAS]
        L.append(f"| {k} | {len(runs[k])} | " + " | ".join(cells) + " |")
    for n, r in refs.items():
        L.append(f"| {n} | 1 (50 lives) | " + " | ".join(f"{r[m]:.3f}" for m in MEAS) + " |")
    L.append("")
    # reading 1
    if runs["D3"]:
        r1 = boot([runs["D3"][s]["survived"] for s in runs["D3"]])
        ok1 = r1[0] >= 0.80 and r1[1] >= 0.70
        L.append(f"**Reading 1, 'drives are enough to live':** D3 survival share {fmt(r1)} (n = {len(runs['D3'])} runs)"
                 f" -> {'YES' if ok1 else 'NO'} (needs mean >= 0.80 and lower bound >= 0.70).")
    # reading 2
    if runs["D3"] and runs["D2"]:
        (f2, n2) = paired(runs, "D3", "D2", "found_share")
        (s2, _) = paired(runs, "D3", "D2", "survived")
        coll = [collapsed(s) for s in SEEDS if s in runs["D3"]]
        ncoll = sum(1 for c in coll if c)
        if ncoll > 2:
            verdict = "NOT READABLE (curiosity row collapsed in more than 2 of the D3 seeds)"
        else:
            verdict = "YES" if (f2[1] > 0 and s2[1] > -0.10) else "NO"
        L.append(f"**Reading 2, 'curiosity pays':** D3 - D2 found share {fmt(f2)}; survival {fmt(s2)} (n = {n2} seed "
                 f"pairs); D3 curiosity-row collapses: {ncoll} of {len(coll)} -> {verdict} (needs found lower bound > 0, "
                 "survival lower bound > -0.10, at most 2 collapses).")
    # reading 3
    if runs["Dc"] and runs["D3"]:
        (d3, n3) = paired(runs, "Dc", "D3", "survived")
        L.append(f"**Reading 3, 'curiosity alone is not enough':** Dc - D3 survival {fmt(d3)} (n = {n3} seed pairs) -> "
                 f"{'YES' if d3[2] < 0 else 'NO'} (needs upper bound < 0).")
    L.append("")
    L.append("## Secondary (intervals, no gate)")
    for a, b, m in (("D3i", "D3", "survived"), ("D3i", "D3", "found_share"), ("D3-", "D3", "found_share"),
                    ("D3-", "D3", "survived"), ("D3", "D2", "known_end"), ("D3", "D2", "hungry"),
                    ("D3", "D2", "exhausted")):
        if runs[a] and runs[b]:
            (d, n) = paired(runs, a, b, m)
            L.append(f"- {a} - {b}, {m}: {fmt(d)} (n = {n} seed pairs)")
    L.append("")
    L.append("## Learned links (final row norms per run; D3, D2, Dc learn them; D3i's are fixed)")
    for k in ("D3", "D2", "Dc"):
        for s in SEEDS:
            p = OUT / f"{k}_{s}_norms.json"
            if p.exists():
                norms = json.loads(p.read_text())
                if norms:
                    last = norms[-1]
                    L.append(f"- {k} seed {s}: Ws {last['Ws']:.3f}, Wf {last['Wf']:.3f}, Wc {last['Wc']:.3f}")
    L.append("")
    L.append("Which map channel each learned link weights most (the centre tap and its plus neighbours):")
    for k in ("D3", "D2", "Dc"):
        for s in SEEDS:
            p = OUT / f"{k}_{s}.npz"
            if p.exists():
                with np.load(p) as z:
                    parts = []
                    for wk in ("Ws", "Wf", "Wc"):
                        w = z[wk][0]                                    # (C, 3, 3)
                        ch = [float(w[c].sum()) for c in range(w.shape[0])]
                        parts.append(f"{wk}: " + ", ".join(f"{v:+.2f}" for v in ch))
                L.append(f"- {k} seed {s} (sum per channel: wall, unseen, food, shelter, uncertainty): " + "; ".join(parts))
    (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
