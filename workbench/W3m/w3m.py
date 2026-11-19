"""W3m: the body's own mind (questions.md, W3m-frozen). The creator, 19 November 2026: the brain has two minds, one
ours and one the brain's own (we fall asleep even when we do not want to); give the AI parts that react by themselves.

W3k's run "R" (4.0M steps, 2.4M fade, W3d's PYFR; the kept copies CS and CY), plus one inborn part per arm:
  - SL, the sleep reflex: when tiredness reaches F_LINE and energy is at least E_HUNGER, and the shelter is in the map
    memory, the body takes over: it walks the shortest known way to the shelter and stays there until tiredness is 0.
    Hunger wins: if energy falls below E_HUNGER, the reflex lets go. The brain still chooses every step (its draw is
    made, so its random stream is unchanged), but the body's move is the one taken, and the brain learns from the
    steps as taken. The reflex is part of the body, so it acts in the tests too.
  - SR, rest only (GPT, council): the same lines, but the body only holds the brain at the shelter once the brain is
    there by itself (tiredness at the line, energy at least E_HUNGER); it never walks it there.
  - UR, the urge: nothing is forced; every step, tiredness above F_LINE costs the reward
    URGE * min(1, (F - F_LINE) / (F_CAP - F_LINE)) (at the cap, the same as W3h's thorn pain, 0.75).
With both parts off, training is W3k's run "R" exactly (checked).

  python w3m.py run ARM SEED [HOURS]     ARM in SL, SR, UR (train in stages, resumable; then the tests)
"""
from __future__ import annotations

import inspect
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "W3k"))
import w3k  # noqa: E402  (W3k's numerical settings, set before numpy loads)
import numpy as np  # noqa: E402
from w3k import w3d, w3i, W, R3  # noqa: E402

OUT = HERE / "output"
w3k.OUT = OUT
F_LINE, E_HUNGER, URGE = 90.0, 40.0, 0.75     # E_HUNGER: calibrated (calib_m.py, calibration lands only)
ARMS = {"SL": {"reflex": "walk", "urge": False}, "SR": {"reflex": "rest", "urge": False},
        "UR": {"reflex": False, "urge": True}}
for _a in ARMS:
    w3k.RUNS[_a] = {"steps": 4_000_000, "fade": 2_400_000}
w3k.CY_SEED = 20261201                      # a new draw for this study's CY steps
PART = {"reflex": False, "urge": False}
COUNT = {"steps": 0, "forced": 0}


class Reflex:
    """The sleep reflex, one per life. It reads only the body and the map memory (as W3's Script)."""

    def __init__(self):
        self.on = False

    def act(self, w, a):
        COUNT["steps"] += 1
        if not PART["reflex"]:
            return a
        if self.on and (w.F <= 0 or w.E < E_HUNGER):
            self.on = False
        mem = W.MapView(w)
        if not self.on and w.F >= F_LINE and w.E >= E_HUNGER and mem.shelter_known is not None and (
                PART["reflex"] == "walk" or w.pos == mem.shelter_known):
            self.on = True
        if not self.on:
            return a
        COUNT["forced"] += 1
        if w.pos == mem.shelter_known:
            return 4
        b = W.bfs_path(lambda c: not mem.m_wall[c[1], c[0]], w.pos, [mem.shelter_known])
        if b is None:                       # no known way: the reflex lets go
            self.on = False
            COUNT["forced"] -= 1
            return a
        return b


def urge(w):
    if not PART["urge"]:
        return 0.0
    return URGE * min(1.0, max(0.0, w.F - F_LINE) / (W.F_CAP - F_LINE))


# W3k's training source (already with its hooks), with the two parts inserted at anchors (checked to be present)
_src = w3k._src
_anchors = [
    ("        parent = W.Script()\n", "        parent = W.Script()\n        rfx = Reflex()\n"),
    ("            a, _, _ = net.act(m, lev, cell, rng)\n",
     "            a, _, _ = net.act(m, lev, cell, rng)\n            a = rfx.act(w, a)\n"),
    ("            r = R3.reward(kind, d0, w.drive(), cur, w.dead)\n",
     "            r = R3.reward(kind, d0, w.drive(), cur, w.dead) - urge(w)\n"),
    ("def train_net_w3k(", "def train_net_w3m("),
]
for _a, _b in _anchors:
    assert _src.count(_a) == 1, _a
    _src = _src.replace(_a, _b)
_ns = dict(w3k._ns)
_ns.update(Reflex=Reflex, urge=urge)
exec(compile(_src, "w3m_train_net", "exec"), _ns)
train_net_w3m = _ns["train_net_w3m"]

# W3k's staged training, calling this training and saving both copies for every run
_st = inspect.getsource(w3k.train_staged)
for _a, _b in (('                if run == "R":\n', "                if True:   # W3m: the copies of every run\n"),
               ("train_net_w3k(", "train_net_w3m("), ("def train_staged(", "def train_staged_w3m(")):
    assert _st.count(_a) == 1, _a
    _st = _st.replace(_a, _b)
w3k.train_net_w3m = train_net_w3m
exec(compile(_st, "w3m_train_staged", "exec"), w3k.__dict__)
train_staged = w3k.train_staged_w3m

# the tests: the body's reflex acts in every test life of a reflex arm (a fresh reflex per life)
_policy0 = w3i.policy


def policy(net, rng):
    rfx = Reflex()
    base = _policy0(net, rng)
    return lambda w: rfx.act(w, base(w))


w3i.policy = policy
_test_all0 = w3i.test_all


def test_all(net, tag, seeds):
    COUNT.update(steps=0, forced=0)
    lives = _test_all0(net, tag, seeds)
    (OUT / f"reflex_{tag}.json").write_text(json.dumps(dict(COUNT)))
    return lives


w3i.test_all = test_all


def configure(arm, seed):
    w3k.configure(arm, seed)
    w3k.CFG["cy_step"] = w3k.cy_step_for(seed, arm)
    PART.update(ARMS[arm])


def run(arm, seed, hours):
    if not w3k.right_machine():
        return
    configure(arm, seed)
    w3k.machine(arm, seed)
    if train_staged(arm, seed, hours):
        snap = w3k.load_npz(OUT / f"{w3k.tag_of(arm, seed, w3k.RUNS[arm]['fade'])}.npz", seed)
        w3k.test_brain(f"{arm}_{seed}", OUT / f"{arm}_{seed}.npz", seed, snap)
        w3k.test_brain(f"{arm}S_{seed}", OUT / f"{arm}_CS_{seed}.npz", seed, snap)
        w3k.test_brain(f"{arm}Y_{seed}", OUT / f"{arm}_CY_{seed}.npz", seed, snap)
        if PART["reflex"]:                 # the kept copy with the reflex switched off: did the brain learn to rest?
            kind, PART["reflex"] = PART["reflex"], False
            w3k.test_brain(f"{arm}S-off_{seed}", OUT / f"{arm}_CS_{seed}.npz", seed, snap)
            PART["reflex"] = kind
        print("done", arm, seed, flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "run":
        assert sys.argv[2] in ARMS, sys.argv[2]
        run(sys.argv[2], int(sys.argv[3]), float(sys.argv[4]) if len(sys.argv) > 4 else 4.5)
