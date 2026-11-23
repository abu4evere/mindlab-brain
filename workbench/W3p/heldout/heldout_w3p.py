"""W3p-H (questions.md): the Bob Profile's detour tests R2 and R5d on 200 new lands (980001-980200), for W3p's MB and
MBb and W3n's HR (kept copies, seeds 1-8) and the controls. Only the list of lands differs from the Bob Profile.

  python heldout_w3p.py run ARM [SEED]     ARM in MB, MBb, HR (with SEED), script, greedy, random
  python heldout_w3p.py analyse            -> heldout_analysis.md / .json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
import bp_mv  # noqa: E402  (the Bob Profile's tests and the numerical settings first)
import numpy as np  # noqa: E402

T = bp_mv.T
LANDS = list(range(980001, 980201))
OUT = HERE / "output"


def run(arm, seed=None):
    T.TEST_LANDS = LANDS
    R = T.R3.regrowth()
    T.w3n.configure("HR", 1)
    agent = arm if arm in ("script", "greedy", "random") else bp_mv.load_brain(arm, seed)
    prev = T.body(False)
    res = {"R2": T.t_R2(agent, R), "R5d": T.t_R5d(agent, R), "arm": arm, "seed": seed}
    T.body(prev[0] == "walk")
    OUT.mkdir(exist_ok=True)
    (OUT / f"heldout_{arm}_{seed or 0}.json").write_text(json.dumps(res))
    print(json.dumps(res), flush=True)


def analyse():
    idx = np.random.default_rng(20261124).integers(0, 8, (10_000, 8))
    ci = lambda v: [round(float(np.mean(v)), 3), round(float(np.percentile(np.asarray(v)[idx].mean(1), 5)), 3),
                    round(float(np.percentile(np.asarray(v)[idx].mean(1), 95)), 3)]
    get = lambda a, s, t: json.loads((OUT / f"heldout_{a}_{s}.json").read_text())[t]["success"]
    res, L = {}, ["# W3p-H: detours on 200 new lands (heldout_w3p.py, frozen)", ""]
    for t in ("R2", "R5d"):
        v = {a: np.array([get(a, s, t) for s in range(1, 9)]) for a in ("MB", "MBb", "HR")}
        ctl = {c: get(c, 0, t) for c in ("script", "greedy", "random")}
        cases = json.loads((OUT / "heldout_HR_1.json").read_text())[t]["cases"]
        d1, d2 = ci(v["MB"] - v["HR"]), ci(v["MBb"] - v["HR"])
        res[t] = {"cases": cases, "means": {a: ci(x) for a, x in v.items()}, "controls": ctl, "MB-HR": d1, "MBb-HR": d2,
                  "MB confirmed": bool(d1[1] > 0), "MBb confirmed": bool(d2[1] > 0), "MBb lower >= 0.80": bool(ci(v["MBb"])[1] >= 0.80)}
        L += [f"## {t} ({cases} detour cases)", "",
              f"- MB {ci(v['MB'])}, MBb {ci(v['MBb'])}, HR {ci(v['HR'])}; controls {ctl}",
              f"- **MB − HR {d1} -> {'confirmed' if d1[1] > 0 else 'not confirmed'}; MBb − HR {d2} -> "
              f"{'confirmed' if d2[1] > 0 else 'not confirmed'}**; MBb's lower bound at least 0.80: {ci(v['MBb'])[1] >= 0.80}",
              f"- per seed: MB {v['MB'].round(2).tolist()}, MBb {v['MBb'].round(2).tolist()}, HR {v['HR'].round(2).tolist()}", ""]
    (HERE / "heldout_analysis.json").write_text(json.dumps(res, indent=1))
    (HERE / "heldout_analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    if sys.argv[1] == "analyse":
        analyse()
    else:
        run(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else None)
