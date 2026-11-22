"""W3p: a planner that must plan (draft; not frozen). W3n's HR exactly (the body, its reflexes, the parent's childhood,
the recipe, the schedule), except the brain: MoveVIN (brain_mv.py) instead of DriveVIN.

  python w3p.py run ARM SEED [HOURS]       ARM in MV (the full schedule), PMV / PHR (the pilot: a short schedule)
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "W3n"))
import w3n  # noqa: E402  (W3n, W3m, W3k: the numerical settings before numpy loads)
from w3n import w3k, w3m, W  # noqa: E402
import brain_mv  # noqa: E402
import numpy as np  # noqa: E402

B = w3k.B
OUT = HERE / "output"
DRIVE = B.DriveVIN
ARMS = {"MV": ("move", 4_000_000, 2_400_000), "PMV": ("move", 800_000, 480_000), "PHR": ("drive", 800_000, 480_000),
        "MB": ("bump", 4_000_000, 2_400_000), "PMB": ("bump", 800_000, 480_000)}
# Learning from bumps (the "bump" arms): every attempted move is a lesson for the brain's "can I enter here?" filter
# (Wp, bp): the place it tried to enter, as its own map memory showed it before the step, and whether it got there.
# Every BUMP_BATCH attempts, one logistic step (learning rate BUMP_LR) on those lessons. Only while training.
BUMP_LR, BUMP_BATCH = 0.05, 64
LEARN = {"on": False, "net": None, "rows": [], "ys": [], "steps": 0}
for _a, (_b, _s, _f) in ARMS.items():
    w3k.RUNS[_a] = {"steps": _s, "fade": _f}
    w3m.ARMS[_a] = {"reflex": "walk", "urge": False}
    w3n.ARMS[_a] = {"cheap": False, "hunger": True}


class BumpVIN(brain_mv.MoveVIN):
    """MoveVIN that registers itself, so the world can hand it the lessons of its bumps during training."""
    def __init__(self, seed, fixed_map=False):
        super().__init__(seed, fixed_map)
        LEARN["net"] = self


class BumpWorld(w3n.CheapWorld):
    """W3n's world; while training a bump arm, each attempted move (not 'stay') becomes a lesson."""
    def step(self, a):
        if not (LEARN["on"] and LEARN["net"] is not None and a != 4):
            return super().step(a)
        dx, dy = W.MOVES[a]
        tx, ty = self.pos[0] + dx, self.pos[1] + dy
        mp = np.pad(self.obs_map(), ((0, 0), (1, 1), (1, 1)))
        row = mp[:, ty:ty + 3, tx:tx + 3].reshape(-1)          # the 3 x 3 memory patch around the place it tries
        before = self.pos
        out = super().step(a)
        LEARN["rows"].append(row)
        LEARN["ys"].append(1.0 if self.pos != before else 0.0)
        if len(LEARN["ys"]) >= BUMP_BATCH:
            net = LEARN["net"]
            X, y = np.asarray(LEARN["rows"]), np.asarray(LEARN["ys"])
            pr = brain_mv.sig(X @ net.p["Wp"].reshape(-1) + net.p["bp"][0])
            g = pr - y
            net.p["Wp"] -= BUMP_LR * (g @ X / len(y)).reshape(net.p["Wp"].shape)
            net.p["bp"] -= BUMP_LR * g.mean()
            LEARN["rows"], LEARN["ys"] = [], []
            LEARN["steps"] += 1
        return out


def _while_training(fn):
    """Bump lessons only while training. The lessons not yet used travel with the training state, so a run paused and
    resumed (or restarted from its checkpoint) learns exactly as an unbroken one."""
    def wrapped(*a, **k):
        state = k.get("state", a[6] if len(a) > 6 else None)
        buf = (state or {}).get("bump_buf", ([], []))
        LEARN.update(on=True, rows=list(buf[0]), ys=list(buf[1]))
        try:
            res = fn(*a, **k)
        finally:
            LEARN["on"] = False
        res[1]["bump_buf"] = (list(LEARN["rows"]), list(LEARN["ys"]))
        LEARN.update(rows=[], ys=[])
        return res
    return wrapped


w3k.train_net_w3m = _while_training(w3k.train_net_w3m)            # what train_staged calls
w3m.train_net_w3m = _while_training(w3m.train_net_w3m)            # what the checks call


def configure(arm, seed):
    _configure_n(arm, seed)
    kind = ARMS[arm][0]
    B.DriveVIN = {"move": brain_mv.MoveVIN, "bump": BumpVIN, "drive": DRIVE}[kind]   # every 'B.DriveVIN(' builds it
    if kind == "bump":
        W.World = BumpWorld


_configure_n = w3n.configure


def run(arm, seed, hours):
    w3k.OUT = w3m.OUT = w3n.OUT = OUT
    w3n.configure = configure
    w3n.run(arm, seed, hours)


if __name__ == "__main__":
    if sys.argv[1] == "run":
        assert sys.argv[2] in ARMS, sys.argv[2]
        run(sys.argv[2], int(sys.argv[3]), float(sys.argv[4]) if len(sys.argv) > 4 else 999)
