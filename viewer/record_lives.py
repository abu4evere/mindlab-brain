"""Record lives of a trained W3d brain for the life viewer (read-only; learning off, the test's own generator).

  python viewer/record_lives.py ARM SEED LAND_SEED [LAND_SEED ...]   -> viewer/lives_ARM_SEED.json
"""
import json
import string
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "workbench" / "W3b"))
import w3b  # noqa: E402
from w3b import B, W, R3  # noqa: E402

DIG = string.digits + string.ascii_lowercase       # 36 levels for the value map


def load(arm, seed):
    net = B.DriveVIN(seed, fixed_map=False)
    with np.load(ROOT / "workbench" / "W3d" / "output" / f"{arm}_{seed}.npz") as z:
        for k in net.p:
            net.p[k] = z[k].copy()
    return net


def record(net, ls, R):
    land = W.make_land(ls)
    rng = np.random.default_rng(ls)                 # the test's generator for this land
    w = W.World(land, R)
    N = W.N
    seen_before = w.m_seen.copy()
    steps = []
    rel_done = 0
    while not w.done():
        m, lev = w.obs_map(), R3.levels(w, "D3")
        fw = net.plan(m[None], np.asarray(lev, float)[None])
        v = fw[5].max(1).reshape(N, N)
        a, pi, val = net.act(m, lev, w.pos, rng)
        open_ = ~w.walls
        lo, hi = float(v[open_].min()), float(v[open_].max())
        q = np.clip(((v - lo) / (hi - lo + 1e-9) * 35).round().astype(int), 0, 35)
        vmap = "".join(DIG[q[y, x]] if open_[y, x] else "." for y in range(N) for x in range(N))
        pos, E, F = w.pos, w.E, w.F
        _, ate = w.step(a)
        new_seen = np.argwhere(w.m_seen & ~seen_before)
        seen_before = w.m_seen.copy()
        steps.append({
            "p": [pos[0], pos[1]], "E": round(E, 1), "F": round(F, 1), "a": a, "ate": bool(ate),
            "pi": [round(float(x), 2) for x in pi], "lev": [round(float(x), 3) for x in lev],
            "v": vmap,
            "mf": [int(y * N + x) for y, x in np.argwhere(w.m_food)],       # remembered full food (after the step)
            "tf": [int(c[1] * N + c[0]) for c in w.food if w.food_full(c)],  # true full food (after the step)
            "ns": [int(y * N + x) for y, x in new_seen],
        })
        if len(w.events) > rel_done:
            for ev in w.events[rel_done:]:
                steps[-1].setdefault("rel", []).append({"patch": ev[1], "corner": list(ev[2])})
            rel_done = len(w.events)
    cause = None
    if w.dead:
        cause = "exhausted and starving" if w.F > W.F_TIRED else "starved"
    return {"land": ls, "N": N, "walls": [int(y * N + x) for y, x in np.argwhere(land["walls"])],
            "shelter": list(land["shelter"]), "start": list(land["start"]),
            "first_seen": [int(y * N + x) for y, x in np.argwhere(W.World(land, R).m_seen)],
            "lifespan": w.t, "survived": bool(w.t >= W.LIFE and not w.dead), "cause": cause, "steps": steps}


if __name__ == "__main__":
    arm, seed = sys.argv[1], int(sys.argv[2])
    R = R3.regrowth()
    net = load(arm, seed)
    lives = [record(net, int(ls), R) for ls in sys.argv[3:]]
    for l in lives:
        print(l["land"], l["lifespan"], l["survived"], l["cause"])
    (ROOT / "viewer" / f"lives_{arm}_{seed}.json").write_text(json.dumps({"arm": arm, "seed": seed, "lives": lives},
                                                                         separators=(",", ":")))
