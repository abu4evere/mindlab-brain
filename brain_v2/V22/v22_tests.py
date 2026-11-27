"""V2-2's test lives (questions.md, Measures), after fine-tuning (length 1M by the frozen rule, length_rule.md).
  T ARM SEED        fine-tuned walker (GOAL, GOAL-NOFLOOR, FT-NOGOAL, SHAM-GOAL, GOAL-ABLATE) on CW2 test lands 990001-050
  U ARM SEED        the same on the unseen world (lands 995001-050, a fresh deal of looks, operations and spots)
  R REF SEED        references with the frozen RMS walker on the same test lands: CW2's GUIDE-REFLEX and NO-GUIDE
  P WHO SEED        plain-land gate: W3r's world, no things, W3r's fresh lands 910001-910050; WHO = RMS (the parent) or a
                    fine-tuned arm, whose walker with the goal channel empty is the DriveVIN saved as old_{ARM}_{SEED}.npz
  B TEST WHO SEED   the Bob Profile test TEST (W3r's bp_w3r.py, unchanged except where the brain is loaded from)
  python v22_tests.py KIND ...   -> output/{test|unseen|ref|plain}_*.jsonl, bp_output/{TEST}_{WHO}_{SEED}.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import v22  # noqa: E402
import numpy as np  # noqa: E402
from v22 import cw2, w3k, R3, W, OUT, BRAINS, TEST_LANDS  # noqa: E402

w3r = cw2.cw1.w3r
W3R = HERE.parents[1] / "workbench" / "W3r"


def write_lives(path, lands, one):
    done = set()
    if path.exists():
        done = {json.loads(x)["land"] for x in path.read_text().splitlines() if x.strip()}
    with open(path, "a") as f:
        for ls in lands:
            if ls in done:
                continue
            m = one(ls)
            m["land"] = ls
            m["machine"] = v22.machine()
            f.write(json.dumps(m, default=float) + "\n")
            f.flush()


def ref(arm, seed):
    rms = w3k.load_npz(BRAINS / f"RM_CS_{seed}.npz", seed)

    def one(ls):
        cw2.configure(arm, seed)
        m = cw2.life(rms, seed, ls, arm)[1]
        m.pop("acts_by_verb", None)
        return m
    write_lives(OUT / f"ref_{arm}_{seed}.jsonl", TEST_LANDS, one)


def driveVIN(who, seed):
    if who == "RMS":
        return w3k.load_npz(BRAINS / f"RM_CS_{seed}.npz", seed)
    return w3k.load_npz(OUT / f"old_{who}_{seed}.npz", seed)


def plain(who, seed):
    net = driveVIN(who, seed)
    w3i = w3r.w3n.w3i

    def one(ls):
        w3r.configure("RM", seed)
        W.World = w3r.MeaningWorld
        rng = np.random.default_rng(ls)
        w, m = R3.run_life(w3i.policy(net, rng), W.make_land(ls), R3.regrowth(), rng)
        return {"survived": m["survived"], "lifespan": m["lifespan"]}
    write_lives(OUT / f"plain_{who}_{seed}.jsonl", w3i.FRESH_SEEDS, one)


def bob_profile(test, who, seed):
    sys.path.insert(0, str(W3R))
    sys.argv = ["bp_w3r.py", test, "RM", str(seed)]
    import bp_w3r
    T = bp_w3r.T

    def load_brain(arm, s):
        w3r.configure("RM", s)
        return driveVIN(who, s)
    T.load_brain = bp_w3r.load_brain = load_brain
    T.OUT = HERE / "bp_output"
    T.OUT.mkdir(exist_ok=True)
    R = T.R3.regrowth()
    agent = load_brain("RM", seed)
    prev = T.body(test not in T.BARE)
    res = T.TESTS[test](agent, R)
    T.body(prev[0] == "walk")
    res.update(test=test, agent=f"{who}_{seed}")
    (T.OUT / f"{test}_{who}_{seed}.json").write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "T":
        v22.test(a[1], int(a[2]), "test")
    elif a[0] == "U":
        v22.test(a[1], int(a[2]), "unseen")
    elif a[0] == "R":
        ref(a[1], int(a[2]))
    elif a[0] == "P":
        plain(a[1], int(a[2]))
    elif a[0] == "B":
        bob_profile(a[1], a[2], int(a[3]))
    print("done", *a, flush=True)
