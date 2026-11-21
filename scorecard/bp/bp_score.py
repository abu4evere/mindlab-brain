"""The Bob Profile scorer (levels 2 and 5; scorecard/bob_profile_draft.md v2). DRAFT until tag BP-frozen.

Reads output/<TEST>_<agent>.json, applies the pass rules (one-sided 95% bootstrap lower bound over training seeds,
numpy seed 20261121, 10,000 resamples), checks the controls, and prints the profile.

  python bp_score.py ARM [SEEDS]      e.g.  python bp_score.py HR 1,2,3,5,6,7,8,9
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
OUT = HERE / "output"


def get(test, agent):
    p = OUT / f"{test}_{agent}.json"
    return json.loads(p.read_text()) if p.exists() else None


def lb(v):
    v = np.asarray(v, float)
    idx = np.random.default_rng(20261121).integers(0, len(v), (10_000, len(v)))
    return float(np.percentile(v[idx].mean(axis=1), 5))


def main():
    arm = sys.argv[1]
    seeds = [int(s) for s in sys.argv[2].split(",")] if len(sys.argv) > 2 else list(range(1, 9))
    br = lambda t: [get(t, f"{arm}S_{s}") for s in seeds]  # noqa: E731
    rows, lines = {}, [f"# Bob Profile, levels 2 and 5: {arm}S, seeds {seeds}", ""]

    def verdict(name, ok, detail, controls_ok=True):
        state = ("PASS" if ok else "fail") if controls_ok else "INVALID (a control failed)"
        rows[name] = ok and controls_ok
        lines.append(f"- **{name}: {state}.** {detail}")

    def ready(*vals):
        return all(v is not None for v in vals) and all(all(x is not None for x in v) if isinstance(v, list) else True
                                                         for v in vals)

    # Learning 2: normalised lifespan on the test lands, (brain - random) / (Script - random), lower bound >= 0.5
    b, sc, rn = br("L2"), get("L2", "script"), get("L2", "random")
    if ready(b, sc, rn):
        n = [(x["lifespan"] - rn["lifespan"]) / (sc["lifespan"] - rn["lifespan"]) for x in b]
        verdict("Learning 2", lb(n) >= 0.5, f"normalised lifespan mean {np.mean(n):.2f}, lower bound {lb(n):.2f} "
                f"(random {rn['lifespan']:.0f}, Script {sc['lifespan']:.0f} steps; pass >= 0.50)")
    # Reasoning 2: detour success lower bound >= 0.8; Script >= 0.95; greedy and random <= 0.2
    for name, t in (("Reasoning 2", "R2"), ("Reasoning 5 (detour half)", "R5d")):
        b, sc, gr, rn = br(t), get(t, "script"), get(t, "greedy"), get(t, "random")
        if ready(b, sc, gr, rn):
            s = [x["success"] for x in b]
            ctl = sc["success"] >= 0.95 and gr["success"] <= 0.2 and rn["success"] <= 0.2
            verdict(name, lb(s) >= 0.8, f"success mean {np.mean(s):.2f}, lower bound {lb(s):.2f} over {b[0]['cases']} "
                    f"cases (Script {sc['success']:.2f}, greedy {gr['success']:.2f}, random {rn['success']:.2f}; "
                    f"pass >= 0.80)", ctl)
    # Memory 2: success lower bound >= 0.8, and the erased-memory control lower by at least 0.2 (lower bound)
    b, be, sc, rn = br("M2"), br("M2e"), get("M2", "script"), get("M2", "random")
    if ready(b, be, sc, rn):
        s = [x["success"] for x in b]
        d = [x["success"] - y["success"] for x, y in zip(b, be)]
        ctl = sc["success"] >= 0.95 and rn["success"] <= 0.2
        verdict("Memory 2", lb(s) >= 0.8 and lb(d) >= 0.2,
                f"success mean {np.mean(s):.2f} (lower bound {lb(s):.2f}); memory erased {np.mean([y['success'] for y in be]):.2f}, "
                f"drop lower bound {lb(d):.2f} (Script {sc['success']:.2f}, random {rn['success']:.2f}; pass >= 0.80 and "
                f"drop >= 0.20). Source: the designer's map memory (allowed at level 2)", ctl)
    lines.append("- Memory 5: **fail by construction**: the brain has no learned memory of its own (its map memory is "
                 "written by our code)" if arm in ("HR", "RE", "RV") else "- Memory 5: — (test not built)")
    # Generalization 2: lifespan on the new kind of land (twice the walls) / its standard test lifespan, lb >= 0.5
    b, sc = br("G2"), get("G2", "script")
    if ready(b, sc):
        r = [x["ratio"] for x in b]
        verdict("Generalization 2", lb(r) >= 0.5, f"ratio mean {np.mean(r):.2f}, lower bound {lb(r):.2f} (Script "
                f"{sc['ratio']:.2f}; pass >= 0.50)", sc["ratio"] >= 0.5)
    # Autonomy 2: the first move follows the larger need: tracks lower bound >= 0.3; Script >= 0.9; random <= 0.1
    b, sc, rn = br("A2"), get("A2", "script"), get("A2", "random")
    if ready(b, sc, rn):
        t = [x["tracks"] for x in b]
        ctl = sc["tracks"] >= 0.9 and abs(rn["tracks"]) <= 0.15
        verdict("Autonomy 2", lb(t) >= 0.3, f"tracks mean {np.mean(t):.2f}, lower bound {lb(t):.2f} over "
                f"{b[0]['cases']} lands (Script {sc['tracks']:.2f}, random {rn['tracks']:.2f}; pass >= 0.30). Source: "
                "the drives and their mix are the designer's; the weights are learned", ctl)
    # Autonomy 5, survival half: bare fresh-land survival lower bound >= 0.5 (the information half is not built)
    b, sc = br("A5s"), get("A5s", "script")
    if ready(b, sc):
        s = [x["survived"] for x in b]
        ok = lb(s) >= 0.5
        lines.append(f"- **Autonomy 5: {'— (survival half passes; the information half is not built)' if ok else 'fail'}.** "
                     f"bare fresh-land survival mean {np.mean(s):.2f}, lower bound {lb(s):.2f} (Script "
                     f"{sc['survived']:.2f}; pass >= 0.50)")
        rows["Autonomy 5"] = False
    lines.append("- Learning 5, Generalization 5, Reasoning 5 (value half): — (tests not built yet)")

    def level(ab):
        two = rows.get(f"{ab} 2")
        return "—" if two is None else (2 if two else 0)
    prof = {ab: level(ab) for ab in ("Learning", "Reasoning", "Memory", "Generalization", "Autonomy")}
    tot = sum(v for v in prof.values() if isinstance(v, int))
    lines += ["", "| Learning | Reasoning | Memory | Generalization | Autonomy | measured total |",
              "|---|---|---|---|---|---|",
              "| " + " | ".join(str(prof[k]) for k in prof) + f" | {tot} |",
              "", "Levels above 2 are not awarded until their tests are built and frozen; the goal is at least 10 in each."]
    print("\n".join(lines))
    (OUT / f"profile_{arm}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
