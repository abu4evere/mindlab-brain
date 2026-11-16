"""WG2: dreams that leave a question (questions.md, WG2-frozen). WI's IM (W3c's GYFR in WQ's silent room, dreaming
200 imagined steps every 500 room steps); arm IQ also marks the dream's best patch as long unseen in the waking map
memory. Arm IM (re-run, it must reproduce WI) tracks random blocks the same way without marking them.

  python wg2.py run ARM SEED OUT_DIR      ARM in IM, IQ
"""
from __future__ import annotations

import json
import os
import sys
import zlib
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")   # added after the run (findings, caution 2)
import numpy as np  # noqa: E402

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "WI"))
import wi  # noqa: E402
from wi import W, R3, wq  # noqa: E402

ANSWER_WITHIN, BACK = 500, 10_000


def dream(net, room, drng, rng, R):
    """WI's dream, also returning the cells of the imagined patch where the most food was eaten (None if none)."""
    land = wi.imagined_land(room, drng)
    w = W.World(land, R)
    w.E, w.F = float(drng.uniform(40, 150)), float(drng.uniform(0, 150))
    seg = wi.Segments(net, rng)
    eats = [0] * len(land["patches"])
    for _ in range(wi.DREAM_LEN):
        if w.done():
            break
        m, lev, cell = w.obs_map(), R3.levels(w, wi.KIND), w.pos
        a = net.act(m, lev, cell, rng)[0]
        d0 = w.drive()
        cur, ate = w.step(a)
        if ate:
            for i, p in enumerate(land["patches"]):
                if w.pos in W.block_cells(p):
                    eats[i] += 1
        seg.add(m, lev, cell, a, R3.reward(wi.KIND, d0, w.drive(), cur, w.dead))
        seg.flush_if(w, w.done())
    seg.flush_if(w, True)
    best = None
    if max(eats, default=0) > 0:
        best = list(W.block_cells(land["patches"][int(np.argmax(eats))]))
    return {"eaten": sum(eats), "died": bool(w.dead), "steps": w.t}, best


def run(arm, seed, test=True):
    net = wi.load(seed)
    R = R3.regrowth()
    room = wq.Room(W.make_land(wi.ROOM), R)
    rng = np.random.default_rng([seed, wi.ROOM, 41])
    drng = np.random.default_rng([seed, 51])
    qrng = np.random.default_rng([seed, 52])
    seg = wi.Segments(net, rng)
    moves, cells, dreams, questions = [], [], [], []
    while not room.done():
        m, lev, cell = room.obs_map(), R3.levels(room, wi.KIND), room.pos
        a = net.act(m, lev, cell, rng)[0]
        d0 = room.drive()
        before = room.pos
        cur, _ = room.step(a)
        moves.append(a if room.pos != before else 4)
        cells.append(room.pos)
        seg.add(m, lev, cell, a, R3.reward(wi.KIND, d0, room.drive(), cur, False))
        seg.flush_if(room, room.done())
        for q in questions:                                  # answered = any of its cells seen after it was posed
            if q["answered"] is None and room.t - q["t"] <= ANSWER_WITHIN and \
                    any(room.m_last[y, x] > q["t"] for x, y in q["cells"]):
                q["answered"] = room.t - q["t"]
        if room.t % wi.DREAM_EVERY == 0 and not room.done():
            seg.flush_if(room, True)
            d, best = dream(net, room, drng, rng, R)
            dreams.append(d)
            if arm == "IQ":
                if best is not None:
                    for x, y in best:
                        room.m_last[y, x] = room.t - BACK
                    questions.append({"t": room.t, "cells": best, "answered": None})
            else:                                            # IM: a random block of the same remembered land, not marked
                walls = room.m_wall.copy()
                walls[0, :] = walls[-1, :] = walls[:, 0] = walls[:, -1] = True
                cand = W._blocks(walls, {room.pos})
                c = cand[int(qrng.integers(len(cand)))]
                questions.append({"t": room.t, "cells": list(W.block_cells(c)), "answered": None})
    windows = []
    for i in range(wi.T_ROOM // wi.WIN):
        mv, cl = moves[i * wi.WIN:(i + 1) * wi.WIN], cells[i * wi.WIN:(i + 1) * wi.WIN]
        windows.append({"activity": float(np.mean([x != 4 for x in mv])), "reach": len(set(cl)),
                        "pattern": len(zlib.compress(bytes(mv), 9)) / len(mv)})
    out = {"arm": arm, "seed": seed, "windows": windows, "dreams": dreams,
           "questions": [{"t": q["t"], "answered": q["answered"]} for q in questions]}
    if test:
        out["after"] = wi.test_after(net, seed)
    return out


if __name__ == "__main__":
    if sys.argv[1] == "run":
        arm, seed, outd = sys.argv[2], int(sys.argv[3]), Path(sys.argv[4])
        outd.mkdir(parents=True, exist_ok=True)
        (outd / f"{arm}_{seed}.json").write_text(json.dumps(run(arm, seed)), encoding="utf-8")
        print("done", arm, seed, flush=True)
