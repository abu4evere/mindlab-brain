"""W3q: the bad teacher (questions.md). W3n's HR exactly, except the parent during training:
  BF  the corner lie ("food lies in corners") in childhood, gone after the fade (as HR's parent);
  BP  the corner lie in childhood, then staying all life at copy weight 0.05;
  RP  the right parent, then staying all life at copy weight 0.05 (BP's control).
The parent only labels (a copy lesson every 4th step); the child always acts by itself. Tests never see a parent.

  python w3q.py run ARM SEED [HOURS]
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "W3n"))
import w3n  # noqa: E402  (W3n, W3m, W3k: the numerical settings before numpy loads)
import numpy as np  # noqa: E402
from w3n import w3k, w3m, W  # noqa: E402

OUT = HERE / "output"
STAY_W = 0.05                      # the parent who stays: copy weight after the fade (W3j's CV)
ARMS = {"BF": {"lie": True, "stays": False}, "BP": {"lie": True, "stays": True}, "RP": {"lie": False, "stays": True}}
for _a in ARMS:
    w3k.RUNS[_a] = {"steps": 4_000_000, "fade": 2_400_000}
    w3m.ARMS[_a] = {"reflex": "walk", "urge": False}
    w3n.ARMS[_a] = {"cheap": False, "hunger": True}
CFG = {"arm": None, "seed": None}
DOSE = {"acts": 0, "lies": 0, "hungry_acts": 0}
RIGHT_SCRIPT = W.Script
_copy_weight0, _present0 = w3m._ns["copy_weight"], w3m._ns["parent_present"]


def corners(m_wall, m_seen):
    """Open, seen cells with a seen wall left or right AND a seen wall above or below (bool N x N)."""
    w = np.pad(m_wall & m_seen, 1)
    side = w[1:-1, :-2] | w[1:-1, 2:]
    updown = w[:-2, 1:-1] | w[2:, 1:-1]
    return m_seen & ~m_wall & side & updown


class LyingScript(RIGHT_SCRIPT):
    """W3's Script, except that it believes every corner it has seen holds food (only the food it heads for changes)."""

    def act(self, mem):
        right = RIGHT_SCRIPT()
        right.resting = self.resting
        a_right = right.act(mem)
        lied = copy.copy(mem)
        lied.m_food = mem.m_food | corners(mem.m_wall, mem.m_seen)
        a = super().act(lied)
        DOSE["acts"] += 1
        DOSE["hungry_acts"] += int(mem.E < 120)
        DOSE["lies"] += int(a != a_right)
        return a


def _dose_path():
    return OUT / f"dose_{CFG['arm']}_{CFG['seed']}.json"


def _while_training(fn):
    """The arm's parent only while training; the dose counts travel with the training state (split = unsplit)."""
    def wrapped(*a, **k):
        state = k.get("state", a[6] if len(a) > 6 else None)
        DOSE.update((state or {}).get("dose", {"acts": 0, "lies": 0, "hungry_acts": 0}))
        lie = CFG["arm"] in ARMS and ARMS[CFG["arm"]]["lie"]
        if lie:
            W.Script = LyingScript
        try:
            res = fn(*a, **k)
        finally:
            W.Script = RIGHT_SCRIPT
        res[1]["dose"] = dict(DOSE)
        if CFG["arm"] in ARMS:
            OUT.mkdir(exist_ok=True)
            _dose_path().write_text(json.dumps(dict(DOSE, arm=CFG["arm"], seed=CFG["seed"])))
        return res
    return wrapped


TRAIN0 = w3m.train_net_w3m                                         # the unwrapped training (for the checks)
w3k.train_net_w3m = _while_training(w3k.train_net_w3m)            # what train_staged calls
w3m.train_net_w3m = _while_training(w3m.train_net_w3m)            # what the checks call


def configure(arm, seed):
    _configure_n(arm, seed)
    CFG.update(arm=arm, seed=seed)
    fade = w3k.RUNS[arm]["fade"]
    if arm in ARMS and ARMS[arm]["stays"]:            # after the fade the parent stays, at copy weight 0.05
        w3m._ns["copy_weight"] = lambda total: _copy_weight0(total) if total < fade else STAY_W
        w3m._ns["parent_present"] = lambda total: True
    else:
        w3m._ns["copy_weight"], w3m._ns["parent_present"] = _copy_weight0, _present0


_configure_n = w3n.configure


def run(arm, seed, hours):
    w3k.OUT = w3m.OUT = w3n.OUT = OUT
    w3n.configure = configure
    w3n.run(arm, seed, hours)


if __name__ == "__main__":
    if sys.argv[1] == "run":
        assert sys.argv[2] in ARMS, sys.argv[2]
        run(sys.argv[2], int(sys.argv[3]), float(sys.argv[4]) if len(sys.argv) > 4 else 999)
