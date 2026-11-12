"""W1 analysis (questions.md, W1-frozen). Written before any brain runs.

  python workbench/W1/analyse_w1.py        # writes results.md
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
OUT = HERE / "output"
SCRIPTED = ["G", "W", "B", "M", "Mm"]
LEARNED = ["F", "R", "Fimit"]
SEEDS = list(range(1, 17))
IDX = np.random.default_rng(20261115).integers(0, 16, (10_000, 16))
NAME = {"Mm": "M-", "Fimit": "F-imit"}


def measures(rows):
    det = [r for r in rows if r["detour"]]
    con = [r for r in rows if not r["detour"]]
    pocket = [r for r in rows if r["set"] == "pocket"]
    ratio = [r["steps"] / r["shortest"] for r in det if r["solved"]]
    m = {"detour": float(np.mean([r["solved"] for r in det])), "control": float(np.mean([r["solved"] for r in con])),
         "pocket": float(np.mean([r["solved"] for r in pocket])),
         "ratio": float(np.median(ratio)) if ratio else float("inf")}
    for s in ("learning_shapes", "unseen"):
        m[s] = float(np.mean([r["solved"] for r in rows if r["set"] == s]))
    return m


def reading(m, above_g):
    if m["detour"] >= 0.80 and m["pocket"] >= 0.70 and m["ratio"] <= 1.5 and above_g:
        return "looks ahead"
    if m["control"] >= 0.80 and m["detour"] <= 0.50:
        return "reactive"
    return "neither"


def ci(x):
    x = np.asarray(x, float)
    b = x[IDX].mean(1)
    return float(x.mean()), float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))


def main():
    load = lambda n, s: json.loads((OUT / f"{n}_seed_{s}.json").read_text())["rows"]  # noqa: E731
    missing = [f"{n}_seed_0" for n in SCRIPTED if not (OUT / f"{n}_seed_0.json").exists()]
    missing += [f"{n}_seed_{s}" for n in LEARNED for s in SEEDS if not (OUT / f"{n}_seed_{s}.json").exists()]
    checks = (HERE / "checks.log").read_text() if (HERE / "checks.log").exists() else ""
    L = ["# W1: the detour (results)", "", "Frozen as `W1-frozen`. run_w1.py, analyse_w1.py (written before any run).",
         "", "## Validity", "",
         f"- Code checks (checks.log, All: PASS): **{'yes' if 'All: PASS' in checks else 'NO'}**",
         f"- All runs present: **{'yes' if not missing else 'NO, missing ' + ', '.join(missing)}**"]
    if missing or "All: PASS" not in checks:
        (HERE / "results.md").write_text("\n".join(L) + "\n", encoding="utf-8")
        print("\n".join(L))
        return
    sm = {n: measures(load(n, 0)) for n in SCRIPTED}
    g_detour = sm["G"]["detour"]
    rd = {n: reading(m, m["detour"] > g_detour) for n, m in sm.items()}
    valid = rd["B"] == "looks ahead" and rd["G"] != "looks ahead" and rd["W"] != "looks ahead"
    L += [f"- Controls: B looks ahead **{'yes' if rd['B'] == 'looks ahead' else 'NO'}**; G does not "
          f"**{'yes' if rd['G'] != 'looks ahead' else 'NO'}**; W (wall-follower) does not "
          f"**{'yes' if rd['W'] != 'looks ahead' else 'NO'}**",
          f"- **{'Valid.' if valid else 'NOT VALID: the test cannot tell the controls apart; nothing is concluded.'}**",
          "", "## The scripted brains (one run each)", "",
          "| brain | detour | pocket | unseen shapes | learning shapes | control | path ratio | reading |",
          "|---|---|---|---|---|---|---|---|"]
    for n in SCRIPTED:
        m = sm[n]
        L.append(f"| {NAME.get(n, n)} | {m['detour']:.3f} | {m['pocket']:.3f} | {m['unseen']:.3f} | "
                 f"{m['learning_shapes']:.3f} | {m['control']:.3f} | {m['ratio']:.2f} | {rd[n]} |")
    L += ["", "## The learning brains (16 seeds; mean [95% bootstrap])", "",
          "| brain | detour | pocket | unseen shapes | control | path ratio (median of seeds) | detour - G | reading |",
          "|---|---|---|---|---|---|---|---|"]
    for n in LEARNED:
        ms = [measures(load(n, s)) for s in SEEDS]
        mean = {k: float(np.mean([m[k] for m in ms])) for k in ("detour", "pocket", "unseen", "control")}
        mean["ratio"] = float(np.median([m["ratio"] for m in ms]))
        dg = ci([m["detour"] - g_detour for m in ms])
        r = reading(mean, dg[1] > 0) if valid else "-"
        f = lambda k: "{:.3f} [{:.3f}, {:.3f}]".format(*ci([m[k] for m in ms]))  # noqa: E731
        L.append(f"| {NAME.get(n, n)} | {f('detour')} | {f('pocket')} | {f('unseen')} | {f('control')} | "
                 f"{mean['ratio']:.2f} | {dg[0]:+.3f} [{dg[1]:+.3f}, {dg[2]:+.3f}] | **{r}** |")
    L += ["", "Rules (frozen): 'looks ahead' = detour success >= 0.80, pocket success >= 0.70, median path ratio <= 1.5, "
          "and detour success above G's (for learning brains, the lower bound over seeds above 0); 'reactive' = "
          "control >= 0.80 and detour <= 0.50; otherwise 'neither'. Valid only if B looks ahead and G and W do not. "
          "M is engineered planning on a map it builds; it does not show learned planning.", ""]
    text = "\n".join(L) + "\n"
    (HERE / "results.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
