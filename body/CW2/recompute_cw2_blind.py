"""CW2 blind recompute.

Written from the frozen plan (questions.md, "Measures") and the raw output/{ARM}_{SEED}.jsonl files only,
without opening the study's analysis script or its analysis outputs.

Per seed: mean over that seed's 50 lives. Differences paired by seed. 95% percentile bootstrap over the
16 seeds, 10,000 resamples, numpy default_rng(RNG_SEED), one shared resample-index matrix for all contrasts.
"""
import json
import platform
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
ARMS = ["GUIDE-REFLEX", "GUIDE-MAP", "SHAM-REFLEX", "SHAM-MAP", "NO-GUIDE", "RANDOM-OPS"]
SEEDS = list(range(1, 17))
N_LIVES = 50
LANDS = set(range(940001, 940051))
N_BOOT = 10_000
RNG_SEED = 20261127


def load():
    data = {}
    checks = []
    for arm in ARMS:
        for seed in SEEDS:
            path = OUT / f"{arm}_{seed}.jsonl"
            lives = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
            lands = [l["land"] for l in lives]
            ok = (len(lives) == N_LIVES and len(set(lands)) == N_LIVES and set(lands) == LANDS
                  and all(l.get("arm", arm) == arm for l in lives)
                  and all(l.get("seed", seed) == seed for l in lives))
            checks.append((arm, seed, len(lives), len(set(lands)), ok))
            data[(arm, seed)] = lives
    return data, checks


def per_seed(data, arm, fn):
    return np.array([np.mean([fn(l) for l in data[(arm, s)]]) for s in SEEDS], dtype=float)


def main():
    data, checks = load()
    measures = {
        "chains": lambda l: float(l["chains"]),
        "survival": lambda l: float(l["survived"]),
        "chain_share": lambda l: 1.0 if l["chains"] >= 1 else 0.0,
    }
    ps = {(arm, m): per_seed(data, arm, f) for arm in ARMS for m, f in measures.items()}

    rng = np.random.default_rng(RNG_SEED)
    idx = rng.integers(0, len(SEEDS), size=(N_BOOT, len(SEEDS)))

    def contrast(a, b, m):
        d = ps[(a, m)] - ps[(b, m)]
        boots = d[idx].mean(axis=1)
        lo, hi = np.percentile(boots, [2.5, 97.5])
        return {"mean": d.mean(), "lo": lo, "hi": hi, "pos": int((d > 0).sum()),
                "neg": int((d < 0).sum()), "zero": int((d == 0).sum()), "per_seed": d}

    contrasts = [
        ("1 Primary", "GUIDE-REFLEX", "NO-GUIDE", "chains"),
        ("2 Key secondary", "GUIDE-MAP", "NO-GUIDE", "chains"),
        ("3a", "GUIDE-REFLEX", "SHAM-REFLEX", "chains"),
        ("3b", "GUIDE-MAP", "SHAM-MAP", "chains"),
        ("4a", "GUIDE-REFLEX", "NO-GUIDE", "survival"),
        ("4b", "GUIDE-MAP", "NO-GUIDE", "survival"),
    ]
    res = [(lab, a, b, m, contrast(a, b, m)) for lab, a, b, m in contrasts]

    ro_lives = [l for s in SEEDS for l in data[("RANDOM-OPS", s)]]
    ro_zero = all(l["chains"] == 0 for l in ro_lives)
    ro_max = max(l["chains"] for l in ro_lives)
    files_ok = all(c[4] for c in checks)

    L = []
    L.append("# CW2 blind recompute")
    L.append("")
    L.append("Done without seeing the study's analysis script (analyse_cw2.py) or its analysis outputs, findings, "
             "round-table files or worklog; written only from the frozen plan (questions.md, Measures) and the raw "
             "output/{ARM}_{SEED}.jsonl files (pilot files ignored).")
    L.append("")
    L.append(f"- Date: 2026-11-27 EST")
    L.append(f"- Script: recompute_cw2_blind.py")
    L.append(f"- RNG: numpy.random.default_rng({RNG_SEED}); one shared {N_BOOT} x 16 resample-index matrix")
    L.append(f"- Python {platform.python_version()}, numpy {np.__version__}")
    L.append("- Method: per seed = mean over its 50 lives; differences paired by seed; 95% percentile bootstrap "
             "of the mean difference over the 16 seeds, 10,000 resamples.")
    L.append("")
    L.append("## Contrasts (mean over 16 seeds, 95% CI, seeds positive / negative / tied)")
    L.append("")
    L.append("| item | contrast | measure | mean diff | 95% CI | +/-/0 seeds |")
    L.append("|---|---|---|---|---|---|")
    for lab, a, b, m, r in res:
        L.append(f"| {lab} | {a} − {b} | {m} | {r['mean']:.3f} | [{r['lo']:.3f}, {r['hi']:.3f}] | "
                 f"{r['pos']}/{r['neg']}/{r['zero']} |")
    L.append("")
    L.append("Per-seed differences (seeds 1..16):")
    L.append("")
    for lab, a, b, m, r in res:
        L.append(f"- {lab} {a} − {b} ({m}): " + ", ".join(f"{x:.3f}" for x in r["per_seed"]))
    L.append("")
    L.append("## 5. Per-arm means over seeds")
    L.append("")
    L.append("| arm | chains per life | survival | share of lives with chains >= 1 |")
    L.append("|---|---|---|---|")
    for arm in ARMS:
        L.append(f"| {arm} | {ps[(arm, 'chains')].mean():.3f} | {ps[(arm, 'survival')].mean():.3f} | "
                 f"{ps[(arm, 'chain_share')].mean():.3f} |")
    L.append("")
    L.append("## 6. Manipulation / data checks")
    L.append("")
    L.append(f"- RANDOM-OPS has 0 chains in every life: {'YES' if ro_zero else 'NO'} "
             f"({len(ro_lives)} lives, max chains {ro_max})")
    L.append(f"- Every file ({len(checks)} files) has 50 lives with 50 distinct land values = 940001-940050, "
             f"arm/seed fields matching the filename: {'YES' if files_ok else 'NO'}")
    for c in checks:
        if not c[4]:
            L.append(f"  - FAIL {c[0]}_{c[1]}: lives={c[2]} distinct lands={c[3]}")
    L.append("")
    text = "\n".join(L)
    (HERE / "recompute_cw2_blind.md").write_text(text, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
