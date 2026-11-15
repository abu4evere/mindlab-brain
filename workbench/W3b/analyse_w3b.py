"""W3b's frozen analysis (questions.md: step 0 readings; W3b readings 1-5), written before any data -> analysis.md
and analysis.json. Intervals: bootstrap over the 8 training seeds (10,000 draws, numpy seed 20261115); differences
paired by seed. D3 is W3's (../W3/output/test_D3_<seed>.json).

  python analyse_w3b.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
OUT = HERE / "output"
W3OUT = HERE.parent / "W3" / "output"
SEEDS = range(1, 9)
LEARNED = ("Y", "FR", "YFR", "RR")
MEAS = ("survived", "lifespan", "known500", "known_end", "found_share", "hungry", "exhausted", "survived1000")
B = 10_000
RNG_SEED = 20261115


def run_means(lives):
    out = {}
    for m in MEAS:
        if m == "survived1000":
            vals = [1.0 if l["lifespan"] >= 1000 else 0.0 for l in lives]
        else:
            vals = [l[m] for l in lives if l[m] is not None and not (isinstance(l[m], float) and math.isnan(l[m]))]
        out[m] = float(np.mean(vals)) if vals else math.nan
    out["n_lives"] = len(lives)
    return out


def load_tests():
    runs = {"D3": {}}
    for s in SEEDS:
        p = W3OUT / f"test_D3_{s}.json"
        if p.exists():
            runs["D3"][s] = run_means(json.loads(p.read_text()))
    for a in LEARNED + ("F",):
        runs[a] = {}
        for s in SEEDS:
            p = OUT / f"test_{a}_{s}.json"
            if p.exists():
                runs[a][s] = run_means(json.loads(p.read_text()))
    return runs


def boot(vals):
    rng = np.random.default_rng(RNG_SEED)
    v = np.asarray(vals, float)
    idx = rng.integers(0, len(v), size=(B, len(v)))
    means = np.nanmean(v[idx], axis=1)
    return float(np.nanmean(v)), float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def paired(runs, a, b, m):
    seeds = [s for s in SEEDS if s in runs[a] and s in runs[b]]
    return boot([runs[a][s][m] - runs[b][s][m] for s in seeds]), len(seeds)


def fmt(t):
    return f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"


def step0_section(L, J):
    L.append("## Step 0: the diagnostic (W3's saved weights; 8 seeds x 50 lives)")
    L.append("")
    L.append("| brain | (a) learned head | (b) greedy value walk | (c) one-step look-ahead | planner-vs-head agreement | hungry steps: sWs / cWc / W0 / fWf (mean abs part) | food cells minus rest |")
    L.append("|---|---|---|---|---|---|---|")
    J["step0"] = {}
    for kind in ("D3i", "D3"):
        rows = []
        for s in SEEDS:
            p = OUT / f"step0_{kind}_{s}.json"
            if p.exists():
                rows.append(json.loads(p.read_text()))
        if not rows:
            continue
        surv = {k: boot([np.mean([x["survived"] for x in r[k]]) for r in rows]) for k in "abc"}
        agree = boot([np.mean(r["agree"]) for r in rows])
        parts = {k: float(np.mean([np.mean([h[k] for h in r["hungry"]]) for r in rows if r["hungry"]])) for k in ("sWs", "cWc", "W0", "fWf")}
        fmr = [np.mean([h["food_minus_rest"] for h in r["hungry"] if h["food_minus_rest"] is not None]) for r in rows
               if any(h["food_minus_rest"] is not None for h in r["hungry"])]
        fm = boot(fmr) if fmr else (math.nan, math.nan, math.nan)
        J["step0"][kind] = {"survival": surv, "agree": agree, "parts": parts, "food_minus_rest": fm, "n_seeds": len(rows)}
        L.append(f"| {kind} (n = {len(rows)}) | {fmt(surv['a'])} | {fmt(surv['b'])} | {fmt(surv['c'])} | {fmt(agree)} | "
                 f"{parts['sWs']:.3f} / {parts['cWc']:.3f} / {parts['W0']:.3f} / {parts['fWf']:.3f} | {fmt(fm)} |")
    if "D3i" in J["step0"]:
        d = J["step0"]["D3i"]
        head = (d["survival"]["b"][0] >= 0.5 or d["survival"]["c"][0] >= 0.5) and d["survival"]["a"][0] < 0.1
        values = d["survival"]["b"][0] < 0.1 and d["survival"]["c"][0] < 0.1 and not (d["food_minus_rest"][1] > 0)
        verdict = "THE HEAD is the broken part" if head else ("THE VALUES are the broken part" if values else "NEITHER ALONE")
        J["step0"]["verdict"] = verdict
        L.append("")
        L.append(f"**Step 0 reading (D3i):** {verdict} (head: (b) or (c) >= 0.50 with (a) about 0; values: (b) and (c) "
                 f"< 0.10 and the food cells' reward not above the rest).")
    L.append("")


def main():
    runs = load_tests()
    J = {}
    L = ["# W3b analysis (the frozen analysis, analyse_w3b.py)", "",
         "Per run: the mean over its 50 test lives; intervals: bootstrap over the training seeds (10,000 draws, seed "
         "20261115); differences paired by seed. n = runs x 50 lives.", ""]
    step0_section(L, J)
    L.append("## The arms")
    L.append("")
    L.append("| arm | runs | survived to 3,000 | survived to 1,000 | lifespan | known@end | found share | hungry | exhausted |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    J["arms"] = {}
    for a in ("D3",) + LEARNED + ("F",):
        if not runs[a]:
            continue
        J["arms"][a] = {m: boot([runs[a][s][m] for s in runs[a]]) for m in MEAS}
        L.append(f"| {a} | {len(runs[a])} | " + " | ".join(fmt(J["arms"][a][m]) for m in
                 ("survived", "survived1000", "lifespan", "known_end", "found_share", "hungry", "exhausted")) + " |")
    L.append("")
    # readings
    J["readings"] = {}
    all_zero = all(J["arms"][a]["survived"][0] == 0.0 for a in J["arms"] if a != "F")
    prim = "lifespan" if all_zero else "survived"
    L.append(f"## Readings (primary survival to 3,000; every learned survival is 0 -> readings 2 and 3 on lifespan: {all_zero})")
    L.append("")
    r1 = any(J["arms"].get(a, {}).get("survived", (0, 0, 0))[0] >= 0.5 and J["arms"][a]["survived"][1] >= 0.3
             for a in ("Y", "FR", "YFR") if a in J["arms"])
    J["readings"]["1 a learned brain lives"] = r1
    L.append(f"1. **A learned brain lives** (Y, FR or YFR: survival mean >= 0.50 and lower bound >= 0.30): **{'YES' if r1 else 'NO'}**")
    r2 = {}
    for a in ("Y", "FR", "YFR"):
        if runs[a] and runs["D3"]:
            d, n = paired(runs, a, "D3", prim)
            r2[a] = {"diff": d, "n": n, "yes": d[1] > 0}
            L.append(f"2. **{a} − D3 on {prim}:** {fmt(d)} (n = {n} seed pairs) -> {'YES' if d[1] > 0 else 'NO'}")
    J["readings"]["2 the parts help"] = r2
    if runs["FR"] and runs["RR"]:
        d, n = paired(runs, "FR", "RR", prim)
        J["readings"]["3 content not compute"] = {"diff": d, "n": n, "yes": d[1] > 0}
        L.append(f"3. **Content, not compute** (FR − RR on {prim}): {fmt(d)} (n = {n}) -> {'YES' if d[1] > 0 else 'NO'}")
    if runs["F"]:
        f = J["arms"]["F"]["survived"]
        J["readings"]["4 the ceiling is reachable"] = f[0] >= 0.5
        L.append(f"4. **The ceiling is reachable** (D3+F survival {fmt(f)} >= 0.50): **{'YES' if f[0] >= 0.5 else 'NO'}**")
    L.append("5. **Survival to 1,000** (secondary):")
    for a in ("Y", "FR", "YFR"):
        if runs[a] and runs["D3"]:
            d, n = paired(runs, a, "D3", "survived1000")
            L.append(f"   - {a} − D3: {fmt(d)} (n = {n})")
    if runs["FR"] and runs["RR"]:
        d, n = paired(runs, "FR", "RR", "survived1000")
        L.append(f"   - FR − RR: {fmt(d)} (n = {n})")
    L.append("")
    L.append("## Secondary: YFR − Y, YFR − FR, Y − RR (lifespan and survival)")
    for a, b in (("YFR", "Y"), ("YFR", "FR"), ("Y", "RR")):
        if runs[a] and runs[b]:
            for m in ("survived", "lifespan"):
                d, n = paired(runs, a, b, m)
                L.append(f"- {a} − {b}, {m}: {fmt(d)} (n = {n})")
    L.append("")
    L.append("## Compute and events (per run: total updates; events and replays per life)")
    J["compute"] = {}
    for a in LEARNED:
        for s in SEEDS:
            p = OUT / f"{a}_{s}_lives.json"
            if p.exists():
                d = json.loads(p.read_text())
                lv = d["lives"]
                J["compute"][f"{a}_{s}"] = {"updates": d["updates"], "lives": len(lv),
                                           "events_per_life": float(np.mean([x["events"] for x in lv])),
                                           "replays_per_life": float(np.mean([x["replays"] for x in lv])),
                                           "mean_t_first200": float(np.mean([x["t"] for x in lv[:200]])),
                                           "mean_t_last200": float(np.mean([x["t"] for x in lv[-200:]]))}
                c = J["compute"][f"{a}_{s}"]
                L.append(f"- {a} seed {s}: updates {c['updates']}; lives {c['lives']}; events/life {c['events_per_life']:.2f}; "
                         f"replays/life {c['replays_per_life']:.2f}; training lifespan first 200 lives {c['mean_t_first200']:.0f} -> last 200 {c['mean_t_last200']:.0f}")
    (HERE / "analysis.json").write_text(json.dumps(J, indent=1), encoding="utf-8")
    (HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
