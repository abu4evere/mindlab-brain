"""W3o: raw eyes (questions.md, W3o-frozen). The creator, 20 Nov 2026, on the living-brain picture: is the brain built
for its own world? The brain's eyes hand it a sorted world: one layer each for walls, food and shelter. Here the same
memory is shown as three mixed colour layers (each layer is on for two kinds of thing); W3n's HR body, everything else
the same, the same seeds (paired with W3n's HR):

  - RE, mixed colours: wall 110, food 011, shelter 101, floor and never-seen 000. The same information (an exact
    linear mix of the sorted layers), but no layer means one thing: the brain has to untangle them itself.
  - RV, colours that change from land to land: on each land the three colours are dealt to wall, food and shelter at
    random (from the land's seed). Colour alone means nothing; only shape, place and what happens (eating, resting)
    tell food from wall from shelter.
The unseen and staleness layers, the body (sleep and hunger reflexes, which read the world's own memory) and the parent
(W3's Script) are unchanged: only what the brain sees changes. With EYES "sorted", W3o trains W3n's HR bit for bit
(checked).

  python w3o.py run ARM SEED [HOURS]     ARM in RE, RV
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "W3n"))
import w3n  # noqa: E402  (W3n, W3m, W3k: the numerical settings before numpy loads)
import numpy as np  # noqa: E402
from w3n import w3k, w3m, W  # noqa: E402

OUT = HERE / "output"
CODES = np.array([[1, 1, 0], [0, 1, 1], [1, 0, 1]], float)     # rows: wall, food, shelter; columns: colour layers
VARY_SEED = 20261212
ARMS = {"RE": "fixed", "RV": "vary"}
for _a in ARMS:
    w3k.RUNS[_a] = {"steps": 4_000_000, "fade": 2_400_000}
    w3m.ARMS[_a] = {"reflex": "walk", "urge": False}           # W3m's sleep reflex
    w3n.ARMS[_a] = {"cheap": False, "hunger": True}             # W3n's HR body
EYES = {"mode": "sorted", "swap": False}


def codes_for(land_seed):
    """The colour of wall, food and shelter on a land (rows). Fixed (RE) or dealt from the land's seed (RV)."""
    c = CODES.copy()
    if EYES["mode"] == "vary":
        c = c[np.random.default_rng([VARY_SEED, int(land_seed)]).permutation(3)]
    if EYES["swap"]:                                            # the test-only check: wall and food colours swapped
        c = c[[1, 0, 2]]
    return c


class RawWorld(w3n.CheapWorld):
    """W3n's world; only the brain's view of the map memory changes."""

    def obs_map(self):
        m = super().obs_map()
        if EYES["mode"] == "sorted":
            return m
        c = codes_for(self.land["seed"])
        kinds = np.stack([m[W.CH_WALL], m[W.CH_FOOD], m[W.CH_SHELTER]])          # (3, N, N), one kind per cell
        colour = np.tensordot(c.T, kinds, axes=1)                                 # (3 layers, N, N)
        out = np.empty_like(m)
        out[0], out[1], out[2] = colour
        out[3], out[4] = m[W.CH_UNSEEN], m[W.CH_UNC]
        return out


def configure(arm, seed):
    _configure_n(arm, seed)                                     # W3n's (HR body, sleep reflex), then the eyes
    W.World = RawWorld
    EYES.update(mode=ARMS.get(arm, "sorted"), swap=False)


_configure_n = w3n.configure
_test_brain = w3k.test_brain


def run(arm, seed, hours):
    w3k.OUT = w3m.OUT = w3n.OUT = OUT
    w3n.configure = configure                                   # W3n's run() configures through this
    w3n.run(arm, seed, hours)                                   # trains; tests the end, S, Y, S-off and S-bare
    if (OUT / f"{arm}_CS_{seed}.npz").exists() and not (OUT / f"test_{arm}S-swap_{seed}.json").exists():
        snap = w3k.load_npz(OUT / f"{w3k.tag_of(arm, seed, w3k.RUNS[arm]['fade'])}.npz", seed)
        EYES["swap"] = True                                     # does it use what the colours mean?
        _test_brain(f"{arm}S-swap_{seed}", OUT / f"{arm}_CS_{seed}.npz", seed, snap)
        EYES["swap"] = False
        print("swap done", arm, seed, flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "run":
        assert sys.argv[2] in ARMS, sys.argv[2]
        run(sys.argv[2], int(sys.argv[3]), float(sys.argv[4]) if len(sys.argv) > 4 else 999)
