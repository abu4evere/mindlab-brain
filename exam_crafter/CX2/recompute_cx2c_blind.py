"""Blind recompute for CX2-C (confirmatory Crafter run).

Reads only the four raw per-life JSONL files in CX2/output_confirm and
computes the Crafter score per arm, bootstrap intervals and the frozen-plan
comparisons. Writes recompute_cx2c_blind.md next to this script.

Usage:  python -I recompute_cx2c_blind.py "<timestamp string>"
"""
import json
import math
import os
import platform
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "output_confirm")
ARMS = ["learn", "named", "blind", "random5p"]  # also the fixed RNG draw order
ACH = [
    "collect_coal", "collect_diamond", "collect_drink", "collect_iron",
    "collect_sapling", "collect_stone", "collect_wood", "defeat_skeleton",
    "defeat_zombie", "eat_cow", "eat_plant", "make_iron_pickaxe",
    "make_iron_sword", "make_stone_pickaxe", "make_stone_sword",
    "make_wood_pickaxe", "make_wood_sword", "place_furnace", "place_plant",
    "place_stone", "place_table", "wake_up",
]
assert len(ACH) == 22 and len(set(ACH)) == 22
B = 2000
SEED0 = 100001


def load(arm):
    path = os.path.join(DATA, arm + ".jsonl")
    lives, malformed, blank = [], [], 0
    with open(path, "r", encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            if not line.strip():
                blank += 1
                continue
            try:
                d = json.loads(line)
            except Exception as e:  # noqa: BLE001
                malformed.append((ln, "json: %s" % e))
                continue
            prob = []
            if not isinstance(d, dict):
                prob.append("not an object")
            else:
                if not isinstance(d.get("steps"), int) or isinstance(d.get("steps"), bool):
                    prob.append("steps missing/non-int")
                if not isinstance(d.get("achievements"), dict):
                    prob.append("achievements missing/non-dict")
                else:
                    for k, v in d["achievements"].items():
                        if not isinstance(v, int) or isinstance(v, bool) or v < 0:
                            prob.append("bad count %s=%r" % (k, v))
                if not isinstance(d.get("seed"), int) or isinstance(d.get("seed"), bool):
                    prob.append("seed missing/non-int")
            if prob:
                malformed.append((ln, "; ".join(prob)))
                continue
            lives.append(d)
    return path, lives, malformed, blank


def score_from_rates(s):
    # s: (..., 22) percentages 0-100
    return np.exp(np.mean(np.log1p(s), axis=-1)) - 1.0


def main():
    when = sys.argv[1] if len(sys.argv) > 1 else "(not given)"
    out = []
    p = out.append

    info = {}
    for arm in ARMS:
        path, lives, malformed, blank = load(arm)
        n = len(lives)
        steps = np.array([d["steps"] for d in lives], dtype=np.int64)
        seeds = [d["seed"] for d in lives]
        sset = set(seeds)
        dups = n - len(sset)
        expected = set(range(SEED0, SEED0 + n))
        missing = sorted(expected - sset)
        extra = sorted(sset - expected)
        in_order = seeds == list(range(SEED0, SEED0 + n))
        unknown = {}
        for d in lives:
            for k, v in d["achievements"].items():
                if k not in ACH:
                    unknown[k] = unknown.get(k, 0) + 1
        X = np.zeros((n, 22), dtype=np.float64)
        for i, d in enumerate(lives):
            a = d["achievements"]
            for j, name in enumerate(ACH):
                if a.get(name, 0) > 0:
                    X[i, j] = 1.0
        zero_count_keys = sum(1 for d in lives for k, v in d["achievements"].items() if v == 0)
        keysets = {}
        for d in lives:
            ks = tuple(sorted(d.keys()))
            keysets[ks] = keysets.get(ks, 0) + 1
        rates = 100.0 * X.mean(axis=0)
        S = float(score_from_rates(rates))
        info[arm] = dict(path=path, n=n, steps=steps, seeds=seeds, dups=dups,
                         missing=missing, extra=extra, in_order=in_order,
                         malformed=malformed, blank=blank, unknown=unknown,
                         X=X, rates=rates, S=S, zero_count_keys=zero_count_keys,
                         keysets=keysets)

    # Bootstrap: one generator, per resample draw learn, named, blind, random5p.
    rng = np.random.default_rng(0)
    boot = {arm: np.empty(B) for arm in ARMS}
    for b in range(B):
        for arm in ARMS:
            n = info[arm]["n"]
            idx = rng.integers(0, n, n)
            r = 100.0 * info[arm]["X"][idx].mean(axis=0)
            boot[arm][b] = score_from_rates(r)

    def ci(v):
        lo, hi = np.percentile(v, [2.5, 97.5])
        return float(lo), float(hi)

    for arm in ARMS:
        info[arm]["ci"] = ci(boot[arm])

    comps = [("learn", "random5p", "PRIMARY"), ("learn", "blind", "secondary"),
             ("learn", "named", "secondary"), ("named", "random5p", "gate for 'close'")]
    cres = {}
    for x, y, role in comps:
        pt = info[x]["S"] - info[y]["S"]
        lo, hi = ci(boot[x] - boot[y])
        side = "above 0" if lo > 0 else ("below 0" if hi < 0 else "straddles 0")
        cres[(x, y)] = (pt, lo, hi, side, role)

    # ---------- console output ----------
    print("when:", when)
    print("platform:", platform.platform(), "| python", platform.python_version(), "| numpy", np.__version__)
    for arm in ARMS:
        I = info[arm]
        print("%-9s n=%d total_steps=%d S=%.4f CI=[%.4f, %.4f] malformed=%d blank=%d dups=%d missing=%d extra=%d in_order=%s unknown=%s"
              % (arm, I["n"], I["steps"].sum(), I["S"], I["ci"][0], I["ci"][1], len(I["malformed"]), I["blank"],
                 I["dups"], len(I["missing"]), len(I["extra"]), I["in_order"], I["unknown"]))
        print("   seeds %d..%d  steps min/median/max %d/%g/%d  zero-valued ach keys=%d" % (
            min(I["seeds"]), max(I["seeds"]), I["steps"].min(), np.median(I["steps"]), I["steps"].max(), I["zero_count_keys"]))
        for ks, c in I["keysets"].items():
            print("   keyset (%d lives): %s" % (c, ",".join(ks)))
        for j, name in enumerate(ACH):
            if I["rates"][j] > 0:
                print("   %-20s %.4f%%  (%d lives)" % (name, I["rates"][j], int(I["X"][:, j].sum())))
    for (x, y), (pt, lo, hi, side, role) in cres.items():
        print("%s - %s: %.4f [%.4f, %.4f] %s (%s)" % (x, y, pt, lo, hi, side, role))

    # ---------- readings ----------
    pt, lo, hi, side, _ = cres[("learn", "random5p")]
    confirmed = lo > 0
    nr = cres[("named", "random5p")]
    ln = cres[("learn", "named")]
    close_applies = nr[1] > 0
    if close_applies:
        close_text = ("NAMED - RANDOM-5P is above 0, so 'close' applies; LEARN - NAMED lower bound %.4f is %s -0.10, so LEARN is %s to NAMED."
                      % (ln[1], "above" if ln[1] > -0.10 else "not above", "close" if ln[1] > -0.10 else "not close"))
    else:
        close_text = ("NAMED - RANDOM-5P interval [%.4f, %.4f] is not entirely above 0 (%s), so the 'close' reading does not apply."
                      % (nr[1], nr[2], nr[3]))
    lb = cres[("learn", "blind")]
    print("PRIMARY:", "Confirmed" if confirmed else "not confirmed")
    print("close:", close_text)

    # ---------- markdown report ----------
    p("# CX2-C blind recompute")
    p("")
    p("## Who and blindness")
    p("")
    p("Independent blind recompute by a Claude Code subagent (Claude Opus 5.5). "
      "Opened only the four raw JSONL files listed under Inputs (first by a `head`/`wc`/`ls` peek to learn the field layout, then by this script). "
      "Did NOT open, read, grep or list the contents of analyse_cx2.py, analyse_cx1.py, any analysis.json / analysis.md, any findings*.md, "
      "any recompute_*.md (including CX2/recompute_cx2_blind.md), lane*.log, run_*.out / run_*.err, questions*.md, or anything in C:\\acl, "
      "and did not search the disk for other analyses. Definitions were taken solely from the task brief (frozen plan text).")
    p("")
    p("## Inputs")
    p("")
    for arm in ARMS:
        p("- `%s` (%d lines read)" % (info[arm]["path"], info[arm]["n"] + len(info[arm]["malformed"]) + info[arm]["blank"]))
    p("")
    p("Script: `%s`, run with `python -I`." % os.path.abspath(__file__))
    p("")
    p("## When")
    p("")
    p("%s (from `TZ='EST5EDT,M3.2.0,M11.1.0' date` in Git Bash)." % when)
    p("")
    p("## Machine")
    p("")
    p("- Platform: %s" % platform.platform())
    p("- Python: %s (%s)" % (platform.python_version(), sys.executable))
    p("- numpy: %s" % np.__version__)
    p("")
    p("## Score definition")
    p("")
    p("For each arm, s_i = percent (0-100) of the arm's lives in which achievement i has count > 0 (absent key = 0), "
      "over all 22 Crafter achievements. S = exp(mean_i ln(1 + s_i)) - 1, reported in score points (percent units). "
      "Intervals: 2,000 bootstrap resamples of lives with replacement, independently within each arm, full S recomputed in every resample; "
      "95% percentile interval = numpy.percentile(..., [2.5, 97.5]) with numpy's default linear interpolation. "
      "Differences use the same resamples (S_x,b - S_y,b).")
    p("")
    p("## RNG order")
    p("")
    p("One generator `numpy.random.default_rng(0)`. For b = 1..2000, in this fixed order: "
      "learn, named, blind, random5p, each `rng.integers(0, n_arm, n_arm)` (n_arm = number of well-formed lives in that arm). "
      "No other draws are made from the generator.")
    p("")
    p("## Per-arm results")
    p("")
    p("| Arm | Lives | Total steps | S | 95% interval |")
    p("|---|---:|---:|---:|---|")
    for arm in ARMS:
        I = info[arm]
        p("| %s | %d | %d | %.4f | [%.4f, %.4f] |" % (arm, I["n"], int(I["steps"].sum()), I["S"], I["ci"][0], I["ci"][1]))
    p("")
    p("## Nonzero achievement rates (s_i, percent of lives)")
    p("")
    p("Only achievements with s_i > 0 in at least one arm are listed; a cell of 0 means the achievement was never unlocked in that arm. "
      "Number of lives in parentheses.")
    p("")
    p("| Achievement | " + " | ".join(ARMS) + " |")
    p("|---|" + "---:|" * len(ARMS))
    for j, name in enumerate(ACH):
        if any(info[a]["rates"][j] > 0 for a in ARMS):
            cells = []
            for a in ARMS:
                c = int(info[a]["X"][:, j].sum())
                cells.append("%.4f (%d)" % (info[a]["rates"][j], c) if c else "0")
            p("| %s | %s |" % (name, " | ".join(cells)))
    never = [name for j, name in enumerate(ACH) if not any(info[a]["rates"][j] > 0 for a in ARMS)]
    p("")
    p("Never unlocked in any arm (%d): %s." % (len(never), ", ".join(never) if never else "none"))
    p("")
    p("## Comparisons")
    p("")
    p("| Comparison | Role | Point | 95% interval | Interval vs 0 |")
    p("|---|---|---:|---|---|")
    for (x, y), (pt_, lo_, hi_, side_, role) in cres.items():
        p("| %s - %s | %s | %.4f | [%.4f, %.4f] | %s |" % (x.upper(), y.upper(), role, pt_, lo_, hi_, side_))
    p("")
    p("## Confirmatory reading")
    p("")
    p("- PRIMARY, LEARN - RANDOM-5P: %.4f, 95%% interval [%.4f, %.4f], %s. Reading: **%s**."
      % (pt, lo, hi, side, "Confirmed" if confirmed else "not confirmed"))
    p("- Secondary, LEARN - BLIND: %.4f, [%.4f, %.4f], %s." % (lb[0], lb[1], lb[2], lb[3]))
    p("- Secondary, LEARN - NAMED: %.4f, [%.4f, %.4f], %s. %s" % (ln[0], ln[1], ln[2], ln[3], close_text))
    p("")
    p("## Checks")
    p("")
    p("| Arm | Malformed lines | Blank lines | Seed range | Duplicate seeds | Missing seeds | Out-of-range seeds | Seeds in file order 100001.. | Names outside the 22 | Zero-valued achievement keys | Steps min / median / max |")
    p("|---|---:|---:|---|---:|---:|---:|---|---|---:|---|")
    for arm in ARMS:
        I = info[arm]
        p("| %s | %d | %d | %d-%d | %d | %d | %d | %s | %s | %d | %d / %g / %d |" % (
            arm, len(I["malformed"]), I["blank"], min(I["seeds"]), max(I["seeds"]), I["dups"], len(I["missing"]),
            len(I["extra"]), "yes" if I["in_order"] else "no",
            ("none" if not I["unknown"] else ", ".join("%s (%d)" % kv for kv in sorted(I["unknown"].items()))),
            I["zero_count_keys"], I["steps"].min(), np.median(I["steps"]), I["steps"].max()))
    p("")
    for arm in ARMS:
        I = info[arm]
        tot = int(I["steps"].sum())
        p("- %s: total steps %d (%s 3,000,000 by %d; last life %d steps, so total minus last life = %d)."
          % (arm, tot, "over" if tot > 3_000_000 else "NOT over", abs(tot - 3_000_000), int(I["steps"][-1]), tot - int(I["steps"][-1])))
        if I["malformed"]:
            for ln_, why in I["malformed"][:10]:
                p("  - malformed line %d: %s" % (ln_, why))
    p("")
    p("Noted without interpretation:")
    p("")
    for arm in ARMS:
        I = info[arm]
        p("- %s: %d of 22 achievements have s_i > 0; longest life %d steps; lives per arm differ because each arm stops just past 3,000,000 total steps."
          % (arm, int((I["rates"] > 0).sum()), int(I["steps"].max())))
    lo_arm = min(ARMS, key=lambda a: min(info[a]["rates"][j] for j in range(22) if info[a]["rates"][j] > 0))
    p("- Smallest nonzero s_i across arms: %s in %s (%.4f%%)." % (
        ACH[int(np.argmin(np.where(info[lo_arm]["rates"] > 0, info[lo_arm]["rates"], np.inf)))], lo_arm,
        float(np.min(info[lo_arm]["rates"][info[lo_arm]["rates"] > 0]))))
    p("- All four arms use the same seed sequence starting at 100001, so lives with the same seed exist across arms; per the plan they are treated as unpaired.")
    p("")
    p("Field layout per life (key sets seen):")
    p("")
    for arm in ARMS:
        for ks, c in info[arm]["keysets"].items():
            p("- %s, %d lives: %s" % (arm, c, ", ".join(ks)))
    p("")

    md = os.path.join(HERE, "recompute_cx2c_blind.md")
    with open(md, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")
    print("wrote", md)


if __name__ == "__main__":
    main()
