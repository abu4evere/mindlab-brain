"""W3n: the body's own mind, part 2 (questions.md, W3n-frozen). On W3m's sleep-reflex body (SL), two more inborn parts:

  - CR, cheaper rest (the creator, 19 Nov 2026): a step spent resting at the shelter costs REST_COST energy, not 1.
    A change of the body's energy economy, in training and in every test of the arm.
  - HR, a hunger reflex (GPT and Gemini's pick, 19 Nov 2026): when energy falls to H_LINE and the map memory holds
    food, the body walks the shortest known way to the nearest remembered food, and hands control back as soon as it
    has eaten once (or when no remembered food is left). It reads only the body and the map memory, so a remembered
    patch that has moved is walked to in vain (counted as "stale"). It takes priority over the sleep reflex while on.
  - HC, both.
The brain draws its own move every step (its random stream is unchanged); the body's move is taken; the brain learns
from the steps as taken (as W3m). With both parts off, W3n trains W3m's SL bit for bit (checked).

  python w3n.py run ARM SEED [HOURS]     ARM in CR, HR, HC
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "W3m"))
import w3m  # noqa: E402  (W3m, W3k: the numerical settings before numpy loads)
from w3m import w3k, w3i, W  # noqa: E402

OUT = HERE / "output"
w3k.OUT = w3m.OUT = OUT
H_LINE = 80.0           # calibrated before any data (calib_n.py, calibration lands only: 50-80 within noise; 80 longest)
REST_COST = 0.5
ARMS = {"CR": {"cheap": True, "hunger": False}, "HR": {"cheap": False, "hunger": True},
        "HC": {"cheap": True, "hunger": True}}
for _a in ARMS:
    w3k.RUNS[_a] = {"steps": 4_000_000, "fade": 2_400_000}
    w3m.ARMS[_a] = {"reflex": "walk", "urge": False}         # every W3n arm keeps W3m's sleep reflex
w3k.CY_SEED = 20261211
BODY = {"cheap": False, "hunger": False}
HC = {"steps": 0, "hunger": 0, "meals": 0, "interrupts": 0}


class CheapWorld(w3i.StaleWorld):
    """W3's world (with W3i's counters); with cheaper rest on, a step resting at the shelter costs REST_COST."""
    def step(self, a):
        before = self.pos
        cur, ate = super().step(a)
        if BODY["cheap"] and not self.dead and self.pos == before == self.shelter:
            self.E += 1.0 - REST_COST
        return cur, ate


class Body(w3m.Reflex):
    """W3m's sleep reflex, plus the hunger reflex. One per life."""

    def __init__(self):
        super().__init__()
        self.hungry, self.lastE = False, None

    def act(self, w, a):
        b = super().act(w, a)                          # the sleep reflex decides first (and counts the step)
        if BODY["hunger"]:
            HC["steps"] += 1
            if self.hungry and self.lastE is not None and w.E > self.lastE:
                self.hungry = False                     # it has eaten: control goes back
                HC["meals"] += 1
            mem = W.MapView(w)
            foods = [(x, y) for y in range(W.N) for x in range(W.N) if mem.m_food[y, x]]
            if not self.hungry and w.E <= H_LINE and foods:
                self.hungry = True
            if self.hungry:
                step = W.bfs_path(lambda c: not mem.m_wall[c[1], c[0]], w.pos, foods) if foods else None
                if step is None:
                    self.hungry = False                 # nothing remembered, or no known way: it lets go
                else:
                    if self.on:                         # hunger wins over sleep while it is on
                        self.on = False
                        w3m.COUNT["forced"] -= 1
                        HC["interrupts"] += 1
                    HC["hunger"] += 1
                    b = step
        self.lastE = w.E
        return b


# the training (W3m's exec'd source looks Reflex up in its namespace) and the tests (W3m's policy wrapper) use Body
w3m._ns["Reflex"] = Body
w3m.Reflex = Body
_test_all_m = w3i.test_all


def test_all(net, tag, seeds):
    HC.update(steps=0, hunger=0, meals=0, interrupts=0)
    lives = _test_all_m(net, tag, seeds)
    (OUT / f"hunger_{tag}.json").write_text(json.dumps(dict(HC)))
    return lives


w3i.test_all = test_all


def configure(arm, seed):
    w3m.configure(arm, seed)                            # W3m's (sleep reflex on), which reinstalls W3i's world
    W.World = CheapWorld
    BODY.update(ARMS[arm])


def run(arm, seed, hours):
    if not w3k.right_machine():
        return
    configure(arm, seed)
    w3k.machine(arm, seed)
    if w3m.train_staged(arm, seed, hours):
        snap = w3k.load_npz(OUT / f"{w3k.tag_of(arm, seed, w3k.RUNS[arm]['fade'])}.npz", seed)
        w3k.test_brain(f"{arm}_{seed}", OUT / f"{arm}_{seed}.npz", seed, snap)
        w3k.test_brain(f"{arm}S_{seed}", OUT / f"{arm}_CS_{seed}.npz", seed, snap)
        w3k.test_brain(f"{arm}Y_{seed}", OUT / f"{arm}_CY_{seed}.npz", seed, snap)
        S, body = OUT / f"{arm}_CS_{seed}.npz", dict(BODY)
        if body["hunger"]:                              # the kept copy with the hunger reflex off: what did it learn?
            BODY["hunger"] = False
            w3k.test_brain(f"{arm}S-off_{seed}", S, seed, snap)
            BODY.update(body)
        if body["cheap"]:                               # in the old body, rest at full price (GPT, council)
            BODY["cheap"] = False
            w3k.test_brain(f"{arm}S-old_{seed}", S, seed, snap)
            BODY.update(body)
        # bare: both reflexes off and the old body (GPT): what the brain does on its own
        BODY.update(cheap=False, hunger=False)
        w3m.PART["reflex"] = False
        w3k.test_brain(f"{arm}S-bare_{seed}", S, seed, snap)
        w3m.PART["reflex"] = "walk"
        BODY.update(body)
        print("done", arm, seed, flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "run":
        assert sys.argv[2] in ARMS, sys.argv[2]
        run(sys.argv[2], int(sys.argv[3]), float(sys.argv[4]) if len(sys.argv) > 4 else 4.5)
