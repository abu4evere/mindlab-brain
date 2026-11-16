"""W3g: a memory of where it has eaten (questions.md, W3g-frozen). W3d's PYFR (fading parent childhood + Y + FR) with a
sixth map channel: 1 on every cell the brain has eaten at in this life. The new channel's weights start at zero; all
other starting weights are W3d's, so at birth the brain is W3d's PYFR child of the same seed.

  python w3g.py run SEED [HOURS]       (train, resumable; then test alone)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "W3d"))
import w3d  # noqa: E402
from w3d import w3b, B, W, R3  # noqa: E402

OUT = HERE / "output"
CFG = {"zero": False}                       # True: the new channel is held at zero (the reproduction check)
BaseWorld, BaseVIN = W.World, B.DriveVIN


class FedWorld(BaseWorld):
    def __init__(self, land, R):
        super().__init__(land, R)
        self.m_fed = np.zeros((W.N, W.N), bool)

    def step(self, a):
        cur, ate = super().step(a)
        if ate:
            self.m_fed[self.pos[1], self.pos[0]] = True
        return cur, ate

    def obs_map(self):
        m = super().obs_map()
        fed = np.zeros((1, W.N, W.N)) if CFG["zero"] else self.m_fed[None].astype(float)
        return np.concatenate([m, fed], 0)


class FedVIN(BaseVIN):
    """W3's DriveVIN with 6 input channels: the first 5 start as W3's own draw, the 6th at zero."""
    def __init__(self, seed, fixed_map=False):
        B.C = 5
        super().__init__(seed, fixed_map=fixed_map)
        for k in ("W0", "Ws", "Wf", "Wc"):
            self.p[k] = np.concatenate([self.p[k], np.zeros((1, 1, 3, 3))], 1)
        B.C = 6


def configure():
    W.World = FedWorld
    B.DriveVIN = FedVIN
    B.C = 6
    w3d.ARMS["FM"] = {"parts": "YR", "always": False}
    w3d.configure("FM")
    w3b.OUT = OUT


if __name__ == "__main__":
    if sys.argv[1] == "run":
        seed = int(sys.argv[2])
        configure()
        if w3b.train("FM", seed, float(sys.argv[3]) if len(sys.argv) > 3 else 4.5):
            w3b.test("FM", seed)
            print("done FM", seed, flush=True)
