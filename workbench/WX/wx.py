"""WX: why do the best learned brains die? (questions.md, WX-frozen). Replays W3d's PYFR test lives (and Script's) with
a recorder; read-only."""
from __future__ import annotations

import json
import os
import sys
from collections import deque
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "W3"))
import brains3 as B  # noqa: E402
import world3 as W  # noqa: E402
import run_w3 as R3  # noqa: E402


def load(seed):
    net = B.DriveVIN(seed, fixed_map=False)
    with np.load(HERE.parent / "W3d" / "output" / f"PYFR_{seed}.npz") as z:
        for k in net.p:
            net.p[k] = z[k].copy()
    return net


def nearest_food(w):
    foods = [(x, y) for y in range(W.N) for x in range(W.N) if w.m_food[y, x]]
    if not foods:
        return None
    # BFS distance on the map memory (unknown counted open, as W3's Script)
    from collections import deque as dq
    seen, q = {w.pos: 0}, dq([w.pos])
    while q:
        c = q.popleft()
        if w.m_food[c[1], c[0]]:
            return seen[c]
        for dx, dy in W.MOVES[:4]:
            n = (c[0] + dx, c[1] + dy)
            if 0 <= n[0] < W.N and 0 <= n[1] < W.N and not w.m_wall[n[1], n[0]] and n not in seen:
                seen[n] = seen[c] + 1
                q.append(n)
    return 999


def life(policy, land, R, rng):
    rec = {"meals": 0, "first_meal": None, "tired": 0, "last100": deque(maxlen=100)}
    lastE = [None]

    def on_step(w, a, d0, cur):
        if lastE[0] is not None and w.E > lastE[0]:
            rec["meals"] += 1
            if rec["first_meal"] is None:
                rec["first_meal"] = w.t
            rec["last_meal"] = w.t
        lastE[0] = w.E
        rec["tired"] += int(w.F > W.F_TIRED)
        rec["last100"].append((nearest_food(w), w.F > W.F_TIRED))
        if w.t == 500:
            rec["known500"] = w.land_known()
    w, m = R3.run_life(policy, land, R, rng, on_step=on_step)
    tail = list(rec["last100"])
    known_any = any(d is not None for d, _ in tail)
    reachable = any(d is not None and d <= 30 for d, _ in tail)
    out = {"lifespan": w.t, "survived": m["survived"], "meals": rec["meals"], "first_meal": rec["first_meal"],
           "since_meal": (w.t - rec.get("last_meal", 0)), "tired_share": rec["tired"] / max(1, w.t),
           "F_end": w.F, "known500": rec.get("known500", w.land_known()), "dead": bool(w.dead)}
    if w.dead:
        out["labels"] = {"no_food_known": not (tail and tail[-1][0] is not None),
                         "food_known_not_reached": reachable,
                         "exhaustion": sum(t for _, t in tail) >= 50}
    return out


def run(who, seed):
    R = R3.regrowth()
    lives = []
    if who == "PYFR":
        net = load(seed)
    for ls in W.TEST_SEEDS:
        land = W.make_land(ls)
        rng = np.random.default_rng(ls)
        if who == "PYFR":
            pol = lambda w: net.act(w.obs_map(), R3.levels(w, "D3"), w.pos, rng)[0]
        else:
            s = W.Script()
            pol = lambda w: s.act(W.MapView(w))
        lives.append(life(pol, land, R, rng))
    return lives


if __name__ == "__main__":
    out = HERE / "output"
    out.mkdir(exist_ok=True)
    if sys.argv[1] == "PYFR":
        for s in range(1, 9):
            (out / f"PYFR_{s}.json").write_text(json.dumps(run("PYFR", s)))
            print("done PYFR", s, flush=True)
    else:
        (out / "Script.json").write_text(json.dumps(run("Script", 0)))
        print("done Script", flush=True)
