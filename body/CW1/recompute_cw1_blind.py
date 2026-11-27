"""CW1 blind recompute (written fresh from questions.md "Measures" and the raw output files only).

Does not import or read analyse_cw1.py or output/analysis.*.
Run: python recompute_cw1_blind.py   (writes recompute_cw1_blind.md next to this file)
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
ARMS = ["LEARN", "RANDOM-OPS", "NO-MAKE", "PAD"]
SEEDS = list(range(1, 17))
N_LIVES = 50
N_BOOT = 10_000
RNG_SEED = 20261126


def load():
    data = {}
    for arm in ARMS:
        for s in SEEDS:
            p = OUT / f"{arm}_{s}.jsonl"
            lives = [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
            data[(arm, s)] = lives
    return data


def per_seed(data, arm, fn):
    """Per-seed mean of fn(life) over that seed's lives, as an array in seed order."""
    return np.array([np.mean([fn(L) for L in data[(arm, s)]]) for s in SEEDS], dtype=float)


# One fixed matrix of resampled seed indices, shared by every contrast (paired by seed).
_rng = np.random.default_rng(RNG_SEED)
BOOT_IDX = _rng.integers(0, len(SEEDS), size=(N_BOOT, len(SEEDS)))


def boot_ci(diff):
    means = diff[BOOT_IDX].mean(axis=1)
    lo, hi = np.percentile(means, [2.5, 97.5])
    return float(lo), float(hi)


def f3(x):
    return f"{x:.3f}"


def main():
    data = load()
    lines = []
    w = lines.append

    # ---- 6. manipulation / integrity checks ----
    checks = []
    all_ok = True
    for (arm, s), lives in data.items():
        n = len(lives)
        lands = {L["land"] for L in lives}
        ok = n == N_LIVES and len(lands) == N_LIVES
        if not ok:
            all_ok = False
            checks.append(f"{arm}_{s}: lives={n}, distinct lands={len(lands)}")
        for L in lives:
            if L.get("arm") is not None and L["arm"] != arm:
                all_ok = False
                checks.append(f"{arm}_{s}: life with arm field {L['arm']}")
            if L.get("seed") is not None and L["seed"] != s:
                all_ok = False
                checks.append(f"{arm}_{s}: life with seed field {L['seed']}")
    land_sets = {k: sorted(L["land"] for L in v) for k, v in data.items()}
    same_lands = len({tuple(v) for v in land_sets.values()}) == 1
    land_range = (min(land_sets[("LEARN", 1)]), max(land_sets[("LEARN", 1)]))
    nm = [L for s in SEEDS for L in data[("NO-MAKE", s)]]
    nm_chain_bad = sum(1 for L in nm if L["chains"] != 0)
    nm_join_bad = sum(1 for L in nm if L["joins"] != 0)

    # ---- 1. primary ----
    chains = {a: per_seed(data, a, lambda L: L["chains"]) for a in ARMS}
    d_primary = chains["LEARN"] - chains["RANDOM-OPS"]
    p_lo, p_hi = boot_ci(d_primary)
    n_pos = int((d_primary > 0).sum())
    n_neg = int((d_primary < 0).sum())
    n_zero = int((d_primary == 0).sum())

    # ---- 2. share chains >= 3 ----
    def pooled(arm, fn):
        vals = [fn(L) for s in SEEDS for L in data[(arm, s)]]
        return float(np.mean(vals)), len(vals)

    ge3 = lambda L: 1.0 if L["chains"] >= 3 else 0.0
    ge1 = lambda L: 1.0 if L["chains"] >= 1 else 0.0
    ge3_seed = {a: per_seed(data, a, ge3) for a in ARMS}
    ge1_seed = {a: per_seed(data, a, ge1) for a in ARMS}
    d_ge3 = ge3_seed["LEARN"] - ge3_seed["RANDOM-OPS"]
    g3_lo, g3_hi = boot_ci(d_ge3)
    d_ge1 = ge1_seed["LEARN"] - ge1_seed["RANDOM-OPS"]
    g1_lo, g1_hi = boot_ci(d_ge1)

    # ---- 4. LEARN - NO-MAKE lifespan & survival ----
    life = {a: per_seed(data, a, lambda L: L["lifespan"]) for a in ARMS}
    surv = {a: per_seed(data, a, lambda L: float(L["survived"])) for a in ARMS}
    d_life = life["LEARN"] - life["NO-MAKE"]
    d_surv = surv["LEARN"] - surv["NO-MAKE"]
    l_lo, l_hi = boot_ci(d_life)
    s_lo, s_hi = boot_ci(d_surv)

    # ---- 5. PAD - LEARN chains ----
    d_pad = chains["PAD"] - chains["LEARN"]
    pd_lo, pd_hi = boot_ci(d_pad)

    # ---- report ----
    w("# CW1 blind recompute")
    w("")
    w("Done on 2026-11-26 (EST) by a fresh session **without seeing the study's analysis script** "
      "(`analyse_cw1.py`), `output/analysis.*`, any findings or roundtable file, or the WORKLOG. "
      "Sources: the frozen plan `questions.md` (Measures) and the raw files `output/{ARM}_{SEED}.jsonl` "
      "(pilot files ignored).")
    w("")
    w(f"- Script: `recompute_cw1_blind.py`. Python {sys.version.split()[0]}, numpy {np.__version__}.")
    w(f"- Bootstrap: {N_BOOT:,} resamples of the 16 seeds with replacement, 95% percentile interval "
      f"(numpy `percentile`, linear), `numpy.random.default_rng({RNG_SEED})`; one index matrix shared by all "
      "contrasts, so every contrast is paired by seed.")
    w("- Unit: per seed, the mean over its 50 lives; differences are paired by seed; \"mean\" = mean over 16 seeds.")
    w("- Populations: 16 seeds x 50 lives = 800 lives per arm.")
    w("")

    w("## 1. Primary: mean completed chains per life, LEARN - RANDOM-OPS")
    w("")
    w("| seed | LEARN | RANDOM-OPS | diff | NO-MAKE | PAD |")
    w("|---|---|---|---|---|---|")
    for i, s in enumerate(SEEDS):
        w(f"| {s} | {f3(chains['LEARN'][i])} | {f3(chains['RANDOM-OPS'][i])} | {f3(d_primary[i])} | "
          f"{f3(chains['NO-MAKE'][i])} | {f3(chains['PAD'][i])} |")
    w(f"| **mean** | {f3(chains['LEARN'].mean())} | {f3(chains['RANDOM-OPS'].mean())} | **{f3(d_primary.mean())}** | "
      f"{f3(chains['NO-MAKE'].mean())} | {f3(chains['PAD'].mean())} |")
    w("")
    w(f"- LEARN - RANDOM-OPS: **{f3(d_primary.mean())}** chains per life, 95% CI **[{f3(p_lo)}, {f3(p_hi)}]** "
      f"(16 seeds, 800 lives per arm).")
    w(f"- Seeds with a positive difference: **{n_pos} of 16** (negative {n_neg}, zero {n_zero}).")
    w(f"- Lower end above 0: **{'yes' if p_lo > 0 else 'no'}**.")
    w("")

    w("## 2. Share of lives with 3+ chains")
    w("")
    w("| arm | pooled (800 lives) | mean of per-seed shares |")
    w("|---|---|---|")
    for a in ARMS:
        pv, n = pooled(a, ge3)
        w(f"| {a} | {f3(pv)} | {f3(ge3_seed[a].mean())} |")
    w("")
    w(f"- LEARN - RANDOM-OPS in per-seed share: **{f3(d_ge3.mean())}**, 95% CI **[{f3(g3_lo)}, {f3(g3_hi)}]**; "
      f"seeds positive {int((d_ge3 > 0).sum())} of 16.")
    w("")

    w("## 3. Share of lives with 1+ chains")
    w("")
    w("| arm | pooled (800 lives) | mean of per-seed shares |")
    w("|---|---|---|")
    for a in ARMS:
        pv, n = pooled(a, ge1)
        w(f"| {a} | {f3(pv)} | {f3(ge1_seed[a].mean())} |")
    w("")
    w(f"- (Extra) LEARN - RANDOM-OPS in per-seed share: {f3(d_ge1.mean())}, 95% CI [{f3(g1_lo)}, {f3(g1_hi)}].")
    w("")

    w("## 4. LEARN - NO-MAKE: lifespan and full-life survival")
    w("")
    w("| arm | mean lifespan (steps) | survival share |")
    w("|---|---|---|")
    for a in ARMS:
        w(f"| {a} | {f3(life[a].mean())} | {f3(surv[a].mean())} |")
    w("")
    w(f"- Lifespan: LEARN - NO-MAKE **{f3(d_life.mean())}** steps, 95% CI **[{f3(l_lo)}, {f3(l_hi)}]**.")
    w(f"- Survival: LEARN - NO-MAKE **{f3(d_surv.mean())}**, 95% CI **[{f3(s_lo)}, {f3(s_hi)}]**.")
    w("")

    w("## 5. PAD - LEARN: mean chains per life")
    w("")
    w(f"- PAD {f3(chains['PAD'].mean())} vs LEARN {f3(chains['LEARN'].mean())}: difference **{f3(d_pad.mean())}**, "
      f"95% CI **[{f3(pd_lo)}, {f3(pd_hi)}]**; seeds where PAD > LEARN {int((d_pad > 0).sum())} of 16.")
    w("")

    w("## 6. Manipulation and integrity checks")
    w("")
    w(f"- NO-MAKE lives with chains != 0: **{nm_chain_bad}** of {len(nm)}; with joins != 0: **{nm_join_bad}** of {len(nm)}.")
    w(f"- Every file has exactly 50 lives with 50 distinct `land` values (and matching arm/seed fields): "
      f"**{'yes' if all_ok else 'NO'}** ({len(data)} files).")
    for c in checks:
        w(f"  - {c}")
    w(f"- Every file uses the same set of lands: **{'yes' if same_lands else 'no'}** "
      f"(lands {land_range[0]}-{land_range[1]}).")
    w("")

    text = "\n".join(lines) + "\n"
    (HERE / "recompute_cw1_blind.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
