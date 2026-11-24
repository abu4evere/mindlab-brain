"""W3r: learning what colours DO within one life (questions.md, W3r-frozen; the creator's sign-off 24 Nov 2026).

W3o's changing-colour lands (the colours of wall, food and shelter dealt anew on each land) and W3n's HR body (both
reflexes, the parent's childhood, the kept copy). A meaning module, reset at every birth, learns from three
consequences the body itself feels, each tied to the colour of the cell involved as remembered just before the step:
  - blocked: the body tried to step into a cell and did not move (the attempted cell);
  - fed:     the body ate on the cell it stands on; a fair negative only when energy is below EMAX after the step;
  - rested:  tiredness fell on the cell it stands on; a fair negative only when tiredness was above 0 before the step.
Steps where a consequence could not happen teach nothing about it. The brain's wall, food and shelter layers are the
module's predictions for each remembered cell's colour (never-seen cells 0); unseen and staleness are unchanged.

Arms (seeds 1-16, paired):
  RV   the 3 colour layers (W3o's RV, the control)
  RM   the table: per colour code, positives / (positives + fair negatives), 0 before any fair trial
  RMX  the sham for the signal: the same table, but each event credited to the colour of a cell drawn at random from
       the 3 x 3 view (seeded), not the cell where it happened
  RE5  Plan2Explore's learner: 5 linear members (3 colour bits + bias -> 3 consequences), seeded random starts
       N(0, 0.1) (a pre-data choice, recorded), bootstrap masks (p = 0.5), one squared-error step per event at the
       learning rate set by the pilot (calib_w3r.py, pilot seeds only; calib_w3r.json); the members' mean, clipped
  HR   the true kinds (sorted memory; W3n's HR)
Test-only probes on the kept copy: S-midswap (from step LIFE/2 the wall and food colours are exchanged, for RV, RM,
RMX, RE5) and, for HR, S-soft (seen cells' wall/food/shelter layers 0.85 where 1, 0.15 where 0).

  python w3r.py run ARM SEED [HOURS]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "W3o"))
import w3o  # noqa: E402  (W3o, W3n, W3m, W3k: the numerical settings before numpy loads)
import numpy as np  # noqa: E402
from w3o import w3k, w3m, w3n, W  # noqa: E402

OUT = HERE / "output"
W3R_SEED = 20261124
ARMS = {"RV": {"eyes": "vary", "module": None}, "RM": {"eyes": "vary", "module": "table"},
        "RMX": {"eyes": "vary", "module": "sham"}, "RE5": {"eyes": "vary", "module": "ens"},
        "HR": {"eyes": "sorted", "module": None}}
for _a in ARMS:
    w3k.RUNS[_a] = {"steps": 4_000_000, "fade": 2_400_000}
    w3m.ARMS[_a] = {"reflex": "walk", "urge": False}           # W3m's sleep reflex
    w3n.ARMS[_a] = {"cheap": False, "hunger": True}             # W3n's HR body
MOD = {"module": None, "oracle": False}                         # oracle: the true colour-to-kind map (checks only)
TEST = {"midswap": False, "soft": False}
ENS = {"lr": None, "init": 0.1, "p": 0.5}
CALIB = HERE / "calib_w3r.json"
if CALIB.exists():
    ENS["lr"] = json.loads(CALIB.read_text())["lr"]
BITS = np.array([[(c >> 2) & 1, (c >> 1) & 1, c & 1, 1] for c in range(8)], float)    # colour code -> bits + bias


def code_of(rgb):
    return int(rgb[0]) * 4 + int(rgb[1]) * 2 + int(rgb[2])


class Table:
    """Per colour code and consequence: positives and fair negatives."""
    def __init__(self):
        self.pos, self.neg = np.zeros((8, 3)), np.zeros((8, 3))

    def add(self, code, j, y):
        (self.pos if y else self.neg)[code, j] += 1

    def pred(self):
        n = self.pos + self.neg
        return np.where(n > 0, self.pos / np.maximum(n, 1), 0.0)


class Ensemble:
    """K = 5 linear members, bootstrap-masked, one squared-error step per event (Plan2Explore's ensemble)."""
    def __init__(self, rng):
        self.rng = rng
        self.w = rng.normal(0.0, ENS["init"], (5, 4, 3))

    def add(self, code, j, y):
        x = BITS[code]
        use = self.rng.random(5) < ENS["p"]
        for k in range(5):
            if use[k]:
                self.w[k, :, j] -= ENS["lr"] * (x @ self.w[k, :, j] - y) * x

    def pred(self):
        return np.clip(np.einsum("ci,kij->cj", BITS, self.w) / 5.0, 0.0, 1.0)


class MeaningWorld(w3o.RawWorld):
    """W3o's world with the meaning module; the truth, the body and the memory are W3n's."""

    def __init__(self, land, R):
        super().__init__(land, R)
        self.codes0 = w3o.codes_for(land["seed"])               # rows: wall, food, shelter -> 3 colour bits
        self.mrng = np.random.default_rng([W3R_SEED, int(land["seed"])])
        kind = MOD["module"]
        self.mod = Table() if kind in ("table", "sham") else Ensemble(self.mrng) if kind == "ens" else None
        self.fair_fed, self.meals_seen, self.food_first, self.food_first_trials = 0, 0, None, None

    # the colours on show (the mid-life swap exchanges wall and food from step LIFE/2, test-only)
    def codes(self):
        c = self.codes0
        if TEST["midswap"] and self.t >= W.LIFE // 2:
            c = c[[1, 0, 2]]
        return c

    def code_map(self):
        """The colour code of every remembered cell (0 for floor and never-seen)."""
        c = [code_of(r) for r in self.codes()]
        cm = np.zeros((W.N, W.N), int)
        cm[self.m_wall], cm[self.m_food], cm[self.m_shelter] = c[0], c[1], c[2]
        return cm

    def step(self, a):
        if self.mod is None:
            return super().step(a)
        dx, dy = W.MOVES[a]
        here, tgt = self.pos, (self.pos[0] + dx, self.pos[1] + dy)
        cm = self.code_map()                                     # the colours as remembered just before the step
        view = self.view_cells()
        E0, F0 = self.E, self.F
        cur, ate = super().step(a)
        moved = self.pos != here
        on = tgt if moved else here
        events = []
        if a != 4:
            events.append((cm[tgt[1], tgt[0]], 0, not moved))  # blocked
        if ate:
            events.append((cm[on[1], on[0]], 1, True))           # fed
        elif self.E < W.EMAX:
            events.append((cm[on[1], on[0]], 1, False))
        if self.F < F0:
            events.append((cm[on[1], on[0]], 2, True))           # rested
        elif F0 > 0:
            events.append((cm[on[1], on[0]], 2, False))
        for code, j, y in events:
            if MOD["module"] == "sham":                          # credited to a random cell in view, not where it happened
                vx, vy = view[int(self.mrng.integers(len(view)))]
                code = cm[vy, vx]
            self.mod.add(int(code), j, bool(y))
            if j == 1:
                self.fair_fed += 1
                self.meals_seen += bool(y)
        if self.food_first is None and self.meals_seen:         # evaluation only: after a meal, fed ranks food first
            p = self.mod.pred()[:, 1]
            land_codes = [code_of(r) for r in self.codes()] + [0]
            food = code_of(self.codes()[1])
            if p[food] > 0 and all(p[food] > p[c] for c in land_codes if c != food):
                self.food_first, self.food_first_trials = self.t, self.fair_fed
        return cur, ate

    def obs_map(self):
        m = w3n.CheapWorld.obs_map(self)                         # the sorted memory (W3's channels)
        kind = MOD["module"]
        if MOD["oracle"]:
            return m                                             # the true colour-to-kind map gives the sorted memory
        if kind is None:
            if w3o.EYES["mode"] == "sorted":
                if TEST["soft"]:
                    seen = self.m_seen
                    for ch in (W.CH_WALL, W.CH_FOOD, W.CH_SHELTER):
                        m[ch] = np.where(seen, 0.15 + 0.7 * m[ch], 0.0)
                return m
            kinds = np.stack([m[W.CH_WALL], m[W.CH_FOOD], m[W.CH_SHELTER]])
            colour = np.tensordot(self.codes().T, kinds, axes=1)
            out = np.empty_like(m)
            out[0], out[1], out[2] = colour
            out[3], out[4] = m[W.CH_UNSEEN], m[W.CH_UNC]
            return out
        pred = self.mod.pred()[self.code_map()]                  # (N, N, 3): blocked, fed, rested
        seen = self.m_seen
        m[W.CH_WALL] = np.where(seen, pred[..., 0], 0.0)
        m[W.CH_FOOD] = np.where(seen, pred[..., 1], 0.0)
        m[W.CH_SHELTER] = np.where(seen, pred[..., 2], 0.0)
        return m


_base_measures = None


def life_measures(w):
    m = _base_measures(w)
    if getattr(w, "mod", None) is not None:
        m.update({"food_first": w.food_first, "food_first_trials": w.food_first_trials, "fair_fed": w.fair_fed})
    return m


def configure(arm, seed):
    global _base_measures
    w3o._configure_n(arm, seed)                                  # W3n's (HR body, sleep reflex); installs W3i's world
    if W.life_measures is not life_measures:
        _base_measures = W.life_measures
        W.life_measures = life_measures
    W.World = MeaningWorld
    w3o.EYES.update(mode=ARMS[arm]["eyes"], swap=False)
    MOD.update(module=ARMS[arm]["module"], oracle=False)
    TEST.update(midswap=False, soft=False)
    if MOD["module"] == "ens":
        assert ENS["lr"] is not None, "the ensemble's learning rate is set by the pilot first (calib_w3r.py)"


_test_brain = w3k.test_brain


def run(arm, seed, hours):
    w3k.OUT = w3m.OUT = w3n.OUT = w3o.OUT = OUT
    w3n.configure = configure                                    # W3n's run() configures through this
    w3n.run(arm, seed, hours)                                    # trains; tests the end, S, Y, S-off and S-bare
    S = OUT / f"{arm}_CS_{seed}.npz"
    if not S.exists():
        return
    snap = w3k.load_npz(OUT / f"{w3k.tag_of(arm, seed, w3k.RUNS[arm]['fade'])}.npz", seed)
    probe = "midswap" if ARMS[arm]["eyes"] == "vary" else "soft"
    if not (OUT / f"test_{arm}S-{probe}_{seed}.json").exists():
        configure(arm, seed)
        TEST[probe] = True
        _test_brain(f"{arm}S-{probe}_{seed}", S, seed, snap)
        TEST[probe] = False
        print(probe, "done", arm, seed, flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "run":
        assert sys.argv[2] in ARMS, sys.argv[2]
        run(sys.argv[2], int(sys.argv[3]), float(sys.argv[4]) if len(sys.argv) > 4 else 999)
