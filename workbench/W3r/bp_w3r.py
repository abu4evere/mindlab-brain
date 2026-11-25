"""W3r's readout of old abilities (questions.md, amendments 5 and 6): the Bob Profile tests (BP-frozen,
scorecard/bp/bp_tests.py, unchanged) on W3r's kept copies, each with its own eyes. The frozen test file is not edited:
this script tells it where W3r's brains are and how to load them (as W3p's bp_mv.py does).

Arms: RM, RMX, RE5 (the meaning module's eyes) and HRr (W3r's own rerun of HR, sorted eyes; named HRr so it is never
mixed with W3n's HR in the scorecard's output).
Whole-life tests (L2, G2, A5s) start every life with an empty module, which learns as it lives. Single-state probes
(R2, R5d, M2, M2e, A2) build a world with a known memory and read moves at once; there the module is first given a
fixed small history (amendment 6, before data): 5 bumps on the wall colour, 1 rest on the shelter colour, 5 floor steps
(fair negatives for blocked, fed and rested on the floor colour) and 3 meals on the food colour, as if after a short
stretch of life (probe_w3r.py's history with k = 3).

  python bp_w3r.py TEST ARM SEED     TEST in L2 R2 R5d M2 M2e G2 A2 A5s; ARM in RM RMX RE5 HRr
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scorecard" / "bp"))
sys.path.insert(0, str(HERE))
import bp_tests as T  # noqa: E402  (the numerical settings first)
import w3r  # noqa: E402

ARMS = {"RM": "RM", "RMX": "RMX", "RE5": "RE5", "HRr": "HR"}
MEALS = 3
_known = T.known


def history(w):
    c = [w3r.code_of(r) for r in w.codes()]
    for _ in range(5):
        w.mod.add(c[0], 0, True)
        for j in range(3):
            w.mod.add(0, j, False)
    w.mod.add(c[2], 2, True)
    for _ in range(MEALS):
        w.mod.add(c[1], 1, True)


def known(ls, R, food_patch=None, age=0):
    w = _known(ls, R, food_patch=food_patch, age=age)
    if getattr(w, "mod", None) is not None:
        history(w)
    return w


def load_brain(arm, seed):
    w3r.configure(ARMS[arm], seed)                   # W3r's world, eyes and module; W3n's HR body
    return T.w3k.load_npz(HERE / "output" / f"{ARMS[arm]}_CS_{seed}.npz", seed)


T.known = known
T.load_brain = load_brain


def main():
    test, arm, seed = sys.argv[1], sys.argv[2], int(sys.argv[3])
    T.OUT = HERE / "bp_output"
    T.OUT.mkdir(exist_ok=True)
    R = T.R3.regrowth()
    agent = load_brain(arm, seed)
    prev = T.body(test not in T.BARE)
    res = T.TESTS[test](agent, R)
    T.body(prev[0] == "walk")
    res.update(test=test, agent=f"{arm}S_{seed}")
    (T.OUT / f"{test}_{arm}S_{seed}.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res), flush=True)


if __name__ == "__main__":
    main()
