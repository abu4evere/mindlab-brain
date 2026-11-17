"""Exploratory (after the data, labelled): the frozen "stale arrivals" measure is structurally 0 (the 3 x 3 view always
shows a cell before the brain can step onto it). This counts "disappointments" instead: a cell remembered as full food
that turns out empty when it comes back into view (not the cell the brain just ate). Replays the test lives exactly.

  python explore/disappoint.py ARM      ARM in PYFR (W3d's weights), L, LC, C
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import w3i  # noqa: E402
from w3i import B, W, R3  # noqa: E402

Base = w3i.BaseWorld


class DWorld(Base):
    def __init__(self, land, R):
        super().__init__(land, R)
        self.dis = 0

    def step(self, a):
        before = self.m_food.copy()
        cur, ate = super().step(a)
        flips = before & ~self.m_food
        if ate:
            flips[self.pos[1], self.pos[0]] = False
        self.dis += int(flips.sum())
        return cur, ate


arm = sys.argv[1]
W.World = DWorld
R = R3.regrowth()
res = []
for s in range(1, 9):
    net = B.DriveVIN(s, fixed_map=False)
    src = (HERE.parent.parent / "W3d" / "output" / f"PYFR_{s}.npz") if arm == "PYFR" else (HERE.parent / "output" / f"{arm}_{s}.npz")
    with np.load(src) as z:
        for k in net.p:
            net.p[k] = z[k].copy()
    per = []
    for ls in W.TEST_SEEDS:
        rng = np.random.default_rng(ls)
        w, m = R3.run_life(lambda w: net.act(w.obs_map(), R3.levels(w, "D3"), w.pos, rng)[0], W.make_land(ls), R, rng)
        per.append({"lifespan": w.t, "dis": w.dis})
    res.append({"seed": s, "lifespan": float(np.mean([p["lifespan"] for p in per])),
                "dis_per_1000": float(np.mean([1000.0 * p["dis"] / p["lifespan"] for p in per]))})
    print(arm, res[-1], flush=True)
(HERE / f"disappoint_{arm}.json").write_text(json.dumps(res))
