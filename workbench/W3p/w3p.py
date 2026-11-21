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

B = w3k.B
OUT = HERE / "output"
DRIVE = B.DriveVIN
ARMS = {"MV": ("move", 4_000_000, 2_400_000), "PMV": ("move", 800_000, 480_000), "PHR": ("drive", 800_000, 480_000)}
for _a, (_b, _s, _f) in ARMS.items():
    w3k.RUNS[_a] = {"steps": _s, "fade": _f}
    w3m.ARMS[_a] = {"reflex": "walk", "urge": False}
    w3n.ARMS[_a] = {"cheap": False, "hunger": True}


def configure(arm, seed):
    _configure_n(arm, seed)
    B.DriveVIN = brain_mv.MoveVIN if ARMS[arm][0] == "move" else DRIVE    # every 'B.DriveVIN(' in the recipe builds it


_configure_n = w3n.configure


def run(arm, seed, hours):
    w3k.OUT = w3m.OUT = w3n.OUT = OUT
    w3n.configure = configure
    w3n.run(arm, seed, hours)


if __name__ == "__main__":
    if sys.argv[1] == "run":
        assert sys.argv[2] in ARMS, sys.argv[2]
        run(sys.argv[2], int(sys.argv[3]), float(sys.argv[4]) if len(sys.argv) > 4 else 999)
