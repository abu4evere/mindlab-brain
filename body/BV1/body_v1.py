"""Body v1 (BV1-frozen, body/BV1/questions.md): the standard body, and its adapter for Mind Lab's W3r world.

The body offers the same senses and verbs in any world; a per-world adapter translates formats and judges legality,
and never labels meaning or chooses for the brain. Here (W3r's world, workbench/W3/world3.py):
  verbs:    move_n, move_s, move_e, move_w (the 4 moves), rest (stay), use (always legal, changes nothing; time passes
            as for rest); operate(k): none (K = 0). The brain's 5 outputs map to the first five verbs.
  senses:   eyes  = per remembered cell its raw look (W3r's colour code; floor and never-seen are code 0, as W3r's
                    memory has it) and a never-seen mask;
            touch = the look underfoot and in each direction;
            feelings = hunger and tiredness in 0-1 (thirst and pain 0 here); self = position, facing, steps since the
                    last meal and the last rest.
  feedback: place_changed, and per body quantity (energy, fatigue) two signed parts: the body's own per-step drift
            and the change caused by the world's response to the action, measured after the drift.
Build decision, recorded (consistent with the frozen plan): the feedback's signed parts are taken from the body's own
quantities (energy, fatigue), not from the 0-1 feelings, because the tiredness feeling saturates at F_CAP while
fatigue itself does not (world3.py uses F_CAP only to scale what is sensed).
The body's drift is its own metabolism (world3.py's rule: energy -2 for a move taken while tired, else -1; fatigue
+1); it is the body's, not the world's, so the adapter may use it.

BodyWorld: W3r's MeaningWorld whose meaning table learns ONLY from Body v1's outputs (never the world's flags):
  blocked = a move verb with place unchanged; fed = the world's response raised energy, fair negative when energy is
  below its maximum after the step; rested = the world's response lowered fatigue, fair trial only when fatigue was
  above 0 before the step. Each lesson is keyed to the look (as remembered just before the step) of the cell involved.
BV1["rename"] (BODY-SHUF): colour codes and verb numbers renamed per land (seeded); the brain and table see only the
renamed numbers.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / "workbench" / "W3r"))
import w3r  # noqa: E402  (W3r and its chain: the numerical settings before numpy loads)
import numpy as np  # noqa: E402
from w3r import W, w3o  # noqa: E402

BV1_SEED = 20261126
VERBS = ("move_n", "move_s", "move_e", "move_w", "rest", "use")
WORLD_ACTION = {"move_n": 0, "move_s": 1, "move_e": 2, "move_w": 3, "rest": 4, "use": 4}
DIRS = {"move_n": (0, -1), "move_s": (0, 1), "move_e": (1, 0), "move_w": (-1, 0)}
BV1 = {"rename": False}


class MindLabAdapter:
    """Body v1 <-> W3r's world. Translates formats only; every verb is always legal; the verb list never changes."""

    def __init__(self, world, rename):
        self.w = world
        if rename:
            rng = np.random.default_rng([BV1_SEED, int(world.land["seed"])])
            self.cperm, self.vperm = rng.permutation(8), rng.permutation(len(VERBS))
        else:
            self.cperm, self.vperm = np.arange(8), np.arange(len(VERBS))
        self.vinv = np.argsort(self.vperm)
        self.facing, self.last_meal, self.last_rest = None, 0, 0

    # what the brain may know about the verbs: their numbers, all legal, in a fixed order (no meaning, no grouping)
    def verb_numbers(self):
        return [int(self.vperm[i]) for i in range(len(VERBS))]

    def legal(self, verb_number):
        return 0 <= verb_number < len(VERBS)

    def looks(self):
        """Eyes: the renamed look of every remembered cell (floor and never-seen 0 before renaming) and never-seen."""
        return self.cperm[w3r.MeaningWorld.code_map(self.w)], ~self.w.m_seen

    def senses(self):
        looks, unseen = self.looks()
        x, y = self.w.pos
        touch = {"under": int(looks[y, x])}
        for v, (dx, dy) in DIRS.items():
            touch[v] = int(looks[y + dy, x + dx])
        return {"eyes": looks, "never_seen": unseen, "touch": touch, "hands": {},
                "feelings": {"hunger": 1.0 - self.w.E / W.EMAX, "tiredness": min(self.w.F, W.F_CAP) / W.F_CAP,
                             "thirst": 0.0, "pain": 0.0},
                "self": {"pos": self.w.pos, "facing": self.facing, "since_meal": self.w.t - self.last_meal,
                         "since_rest": self.w.t - self.last_rest}}

    def act(self, verb_number):
        """Do one verb; returns (feedback, cur, ate) where cur and ate are the world's own (for its bookkeeping only)."""
        assert self.legal(verb_number)
        verb = VERBS[int(self.vinv[verb_number])]
        w = self.w
        E0, F0, pos0 = w.E, w.F, w.pos
        cur, ate = w3o.RawWorld.step(w, WORLD_ACTION[verb])
        moved = w.pos != pos0
        drift_E = -(2.0 if (moved and F0 > W.F_TIRED) else 1.0)
        drift_F = 1.0
        fb = {"verb": verb_number, "place_changed": moved,
              "energy": (drift_E, w.E - (E0 + drift_E)), "fatigue": (drift_F, w.F - (F0 + drift_F)),
              "energy_after": w.E, "fatigue_before": F0}
        if verb in DIRS:
            self.facing = verb_number
        if fb["energy"][1] > 0:
            self.last_meal = w.t
        if fb["fatigue"][1] < 0:
            self.last_rest = w.t
        return fb, cur, ate


class BodyWorld(w3r.MeaningWorld):
    """W3r's world lived through Body v1: the brain's output is a verb number; the table learns from feedback only."""

    def __init__(self, land, R):
        super().__init__(land, R)
        self.adapter = MindLabAdapter(self, BV1["rename"])
        self.last_feedback = None

    def code_map(self):
        return self.adapter.looks()[0]                          # the brain's layers read the (renamed) eyes

    def step(self, a):
        verb_number = int(self.adapter.vperm[a])                # the brain's output, as a Body v1 verb number
        s0 = self.adapter.senses()
        looks0, (x0, y0) = s0["eyes"], s0["self"]["pos"]
        fb, cur, ate = self.adapter.act(verb_number)
        self.last_feedback = fb
        verb = VERBS[int(self.adapter.vinv[verb_number])]
        x, y = self.pos
        on = int(looks0[y, x])                                  # the cell now stood on, as remembered before the step
        if verb in DIRS:
            dx, dy = DIRS[verb]
            self.mod.add(int(looks0[y0 + dy, x0 + dx]), 0, not fb["place_changed"])   # blocked
        if fb["energy"][1] > 0:
            self.mod.add(on, 1, True)                           # fed
        elif fb["energy_after"] < W.EMAX:
            self.mod.add(on, 1, False)
        if fb["fatigue_before"] > 0:
            self.mod.add(on, 2, fb["fatigue"][1] < 0)           # rested
        return cur, ate
