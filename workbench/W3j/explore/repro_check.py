"""EXPLORATORY (not in the frozen plan): how far is the reproduced C seed 1 from W3i's C seed 1 in behaviour?

The frozen reproduction job reports the weights are not identical (max difference 0.27). This tests both brains on
the same 50 test lands and compares lifespans, so we know whether the comparisons with the cited C are affected.

  python explore/repro_check.py      -> explore/repro_check.json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import w3j  # noqa: E402
from w3j import w3i, W, R3  # noqa: E402

import numpy as np  # noqa: E402

w3j.configure("C")
again = w3j.load_npz(HERE.parent / "output" / "C_1.npz", 1)
R = R3.regrowth()
lives = [w3i.test_life(again, ls, R) for ls in W.TEST_SEEDS]
orig = json.loads((HERE.parent.parent / "W3i" / "output" / "test_C_1.json").read_text())
a = np.array([x["lifespan"] for x in lives], float)
b = np.array([x["lifespan"] for x in orig], float)
out = {
    "reproduced_mean_lifespan": float(a.mean()), "w3i_mean_lifespan": float(b.mean()),
    "reproduced_survived": float(np.mean([x["survived"] for x in lives])),
    "w3i_survived": float(np.mean([x["survived"] for x in orig])),
    "same_lifespan_on_lands": int((a == b).sum()), "lands": len(a),
}
(HERE / "repro_check.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
