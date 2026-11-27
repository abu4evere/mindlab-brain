"""V2-1 Revise: independent blind recompute from the frozen plan (questions.md) and raw output files only.

Written without opening the study's analysis script or its outputs.
Per seed = mean over its 50 lives; differences paired by seed; 95% percentile bootstrap over the 16 seeds,
10,000 resamples, numpy default_rng(RNG_SEED).
"""
import json
import os
import platform
import sys

import numpy as np

OUT = r"C:\mindlab\brain_v2\V21\output"
MD = r"C:\mindlab\brain_v2\V21\recompute_v21_blind.md"
ARMS = ["PLAIN", "SURPRISE", "WINDOW", "SHAM"]
CONDS = ["swap", "stable"]
SEEDS = list(range(1, 17))
N_LIVES = 50
N_BOOT = 10_000
RNG_SEED = 20261127


def load(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


checks = []


def check_file(name, lives, land0):
    lands = [r["land"] for r in lives]
    ok = len(lives) == N_LIVES and len(set(lands)) == N_LIVES and set(lands) == set(range(land0 + 1, land0 + 51))
    if not ok:
        checks.append(f"FAIL {name}: n={len(lives)} distinct={len(set(lands))} range={min(lands)}-{max(lands)}")
    return ok


# ---- load Test A ----
A = {}  # (arm, cond) -> dict field -> array over seeds (per-seed means)
nA_ok = 0
plain_resets_total = 0
for arm in ARMS:
    for cond in CONDS:
        surv, res = [], []
        for s in SEEDS:
            name = f"A_{arm}_{cond}_{s}.jsonl"
            lives = load(os.path.join(OUT, name))
            nA_ok += check_file(name, lives, 960000)
            surv.append(np.mean([float(r["survived"]) for r in lives]))
            res.append(np.mean([float(r["resets"]) for r in lives]))
            if arm == "PLAIN":
                plain_resets_total += sum(int(r["resets"]) for r in lives)
        A[(arm, cond)] = {"survived": np.array(surv), "resets": np.array(res)}

# ---- load Test B ----
B = {}
nB_ok = 0
for arm in ARMS:
    ca, cb, rs = [], [], []
    for s in SEEDS:
        name = f"B_{arm}_{s}.jsonl"
        lives = load(os.path.join(OUT, name))
        nB_ok += check_file(name, lives, 970000)
        ca.append(np.mean([float(r["chains_after"]) for r in lives]))
        cb.append(np.mean([float(r["chains_before"]) for r in lives]))
        rs.append(np.mean([float(r["resets"]) for r in lives]))
        if arm == "PLAIN":
            plain_resets_total += sum(int(r["resets"]) for r in lives)
    B[arm] = {"chains_after": np.array(ca), "chains_before": np.array(cb), "resets": np.array(rs)}

# ---- bootstrap ----
rng = np.random.default_rng(RNG_SEED)
IDX = rng.integers(0, len(SEEDS), size=(N_BOOT, len(SEEDS)))  # one shared index matrix for all contrasts


def paired(x, y):
    d = x - y
    boots = d[IDX].mean(axis=1)
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return {"mean": d.mean(), "lo": lo, "hi": hi, "pos": int((d > 0).sum()), "neg": int((d < 0).sum()),
            "zero": int((d == 0).sum())}


def fmt(r):
    return (f"{r['mean']:+.3f} [{r['lo']:+.3f}, {r['hi']:+.3f}]  seeds +{r['pos']} / -{r['neg']} / ={r['zero']}")


res = {}
res["1 swap SURPRISE-PLAIN"] = paired(A[("SURPRISE", "swap")]["survived"], A[("PLAIN", "swap")]["survived"])
res["2 stable SURPRISE-PLAIN"] = paired(A[("SURPRISE", "stable")]["survived"], A[("PLAIN", "stable")]["survived"])
res["3a swap SURPRISE-SHAM"] = paired(A[("SURPRISE", "swap")]["survived"], A[("SHAM", "swap")]["survived"])
res["3b swap SURPRISE-WINDOW"] = paired(A[("SURPRISE", "swap")]["survived"], A[("WINDOW", "swap")]["survived"])
res["x stable WINDOW-PLAIN"] = paired(A[("WINDOW", "stable")]["survived"], A[("PLAIN", "stable")]["survived"])
res["5a B chains_after SURPRISE-PLAIN"] = paired(B["SURPRISE"]["chains_after"], B["PLAIN"]["chains_after"])
res["5b B chains_after WINDOW-PLAIN"] = paired(B["WINDOW"]["chains_after"], B["PLAIN"]["chains_after"])
res["5c B chains_before SURPRISE-PLAIN"] = paired(B["SURPRISE"]["chains_before"], B["PLAIN"]["chains_before"])
res["x B chains_after SURPRISE-SHAM"] = paired(B["SURPRISE"]["chains_after"], B["SHAM"]["chains_after"])
res["x B chains_after SURPRISE-WINDOW"] = paired(B["SURPRISE"]["chains_after"], B["WINDOW"]["chains_after"])

gate_pass = res["2 stable SURPRISE-PLAIN"]["lo"] > -0.03

lines = []
P = lines.append
P("# V2-1 Revise: blind recompute")
P("")
P("Done without seeing the study's analysis script (`analyse_v21.py`) or its outputs (`analysis.json`, `analysis.md`),")
P("findings, roundtable files or worklogs; worked only from the frozen plan `questions.md` and the raw `output/*.jsonl`")
P("(files starting with `pilot` ignored).")
P("")
P(f"- Date: 2026-11-27 (EST)")
P(f"- Script: `recompute_v21_blind.py`")
P(f"- Method: per seed = mean over its 50 lives; differences paired by seed; 95% percentile bootstrap over the 16 seeds,"
  f" {N_BOOT:,} resamples; one shared resample index matrix from `numpy.random.default_rng({RNG_SEED})`.")
P(f"- RNG seed: {RNG_SEED}")
P(f"- Python {platform.python_version()}, numpy {np.__version__}")
P("")
P("Format: mean difference [95% CI]  seeds positive / negative / tied.")
P("")
P("## 1. Primary: swap survival, SURPRISE - PLAIN")
P(f"{fmt(res['1 swap SURPRISE-PLAIN'])}")
P(f"Lower end above 0: {'YES' if res['1 swap SURPRISE-PLAIN']['lo'] > 0 else 'NO'}")
P("")
P("## 2. No-loss gate: stable survival, SURPRISE - PLAIN")
P(f"{fmt(res['2 stable SURPRISE-PLAIN'])}")
P(f"Lower end above -0.03: {'YES (pass)' if gate_pass else 'NO (fail)'}")
P("")
P("## 3. Swap survival, SURPRISE - SHAM and SURPRISE - WINDOW")
P(f"- SURPRISE - SHAM:   {fmt(res['3a swap SURPRISE-SHAM'])}")
P(f"- SURPRISE - WINDOW: {fmt(res['3b swap SURPRISE-WINDOW'])}")
P(f"- (also, stable WINDOW - PLAIN: {fmt(res['x stable WINDOW-PLAIN'])})")
P("")
P("## 4. Per arm and condition (mean over 16 seed means)")
P("")
P("| arm | cond | survival | resets per life |")
P("|---|---|---|---|")
for cond in CONDS:
    for arm in ARMS:
        a = A[(arm, cond)]
        P(f"| {arm} | {cond} | {a['survived'].mean():.3f} | {a['resets'].mean():.3f} |")
P("")
P("Test B per arm:")
P("")
P("| arm | chains_before | chains_after | resets per life |")
P("|---|---|---|---|")
for arm in ARMS:
    b = B[arm]
    P(f"| {arm} | {b['chains_before'].mean():.3f} | {b['chains_after'].mean():.3f} | {b['resets'].mean():.3f} |")
P("")
P("## 5. Test B")
P(f"- chains_after SURPRISE - PLAIN:  {fmt(res['5a B chains_after SURPRISE-PLAIN'])}")
P(f"- chains_after WINDOW - PLAIN:    {fmt(res['5b B chains_after WINDOW-PLAIN'])}")
P(f"- chains_before SURPRISE - PLAIN: {fmt(res['5c B chains_before SURPRISE-PLAIN'])}"
  f"  (|mean| within 0.3: {'YES' if abs(res['5c B chains_before SURPRISE-PLAIN']['mean']) <= 0.3 else 'NO'})")
P(f"- (also, chains_after SURPRISE - SHAM: {fmt(res['x B chains_after SURPRISE-SHAM'])})")
P(f"- (also, chains_after SURPRISE - WINDOW: {fmt(res['x B chains_after SURPRISE-WINDOW'])})")
P("")
P("## 6. Checks")
P(f"- Test A files with 50 lives and 50 distinct lands 960001-960050: {nA_ok}/128")
P(f"- Test B files with 50 lives and 50 distinct lands 970001-970050: {nB_ok}/64")
P(f"- PLAIN total resets (all A and B lives): {plain_resets_total}")
for c in checks:
    P(f"- {c}")
P("")

text = "\n".join(lines)
with open(MD, "w", encoding="utf-8") as f:
    f.write(text)
print(text)
