"""WL3: does forgetting still help in a richer world? (questions.md, WL3-frozen). WL2's arms (L0, L2, Linf) in three
worlds: K6L2 (WN's), K24L2 (24 kinds), K6L3 (3 lids). WS's module numbers KINDS and LIDS are set per world before a
child is run; everything else is WL2's run_child.

  python wl3.py arm WORLD ARM SIZE OUT_DIR      (seeds 1-24)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "WL2"))
import wl2  # noqa: E402
import ws  # noqa: E402

WORLDS = {"K6L2": (6, 2), "K24L2": (24, 2), "K6L3": (6, 3)}
ARMS = ("L0", "L2", "Linf")


def set_world(world):
    ws.KINDS, ws.LIDS = WORLDS[world]


def run_child(world, arm, n, seed):
    set_world(world)
    r = wl2.run_child(arm, n, seed)
    r["world"] = world
    return r


if __name__ == "__main__":
    if sys.argv[1] == "arm":
        world, arm, n, out = sys.argv[2], sys.argv[3], int(sys.argv[4]), Path(sys.argv[5])
        out.mkdir(parents=True, exist_ok=True)
        for s in range(1, 25):
            (out / f"{world}_{arm}_{n}_seed_{s}.json").write_text(json.dumps(run_child(world, arm, n, s)), encoding="utf-8")
        print("done", world, arm, n, flush=True)
