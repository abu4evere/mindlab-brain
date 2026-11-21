"""W3o's probe (questions.md; GPT, council): does the brain alone step toward what it needs? Frozen before any data.

On each of W3's 50 test lands, the map memory is made fully known (walls, food, shelter), the body is put at the land's
start cell, and the brain's greedy first move is read in two set states, with no reflex:
  - hungry: energy 60, tiredness 0; a move is "toward" when it shortens the shortest true path to the nearest food;
  - tired: energy 150, tiredness 150; "toward" when it shortens the path to the shelter.
The score is the share of lands with a move toward; chance is the mean share of the 5 moves that would do so.
Brains: W3n's HRS (sorted eyes), W3o's RES (fixed colours) and RVS (colours by land), and RES with wall and food
colours swapped.

  python probe_w3o.py        -> probe.json
"""
import json
import sys
from collections import deque
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import w3o  # noqa: E402  (the numerical settings before numpy loads)
import numpy as np  # noqa: E402
from w3o import w3k, W  # noqa: E402
from w3k import R3  # noqa: E402

W3N = HERE.parent / "W3n" / "output"
SEEDS = list(range(1, 9))
STATES = {"hungry": (60.0, 0.0), "tired": (150.0, 150.0)}
BRAINS = {"HRS": (W3N, "HR", "sorted", False), "RES": (HERE / "output", "RE", "fixed", False),
          "RVS": (HERE / "output", "RV", "vary", False), "RES-swap": (HERE / "output", "RE", "fixed", True)}


def dist_map(walls, goals):
    d = np.full((W.N, W.N), np.inf)
    q = deque()
    for (x, y) in goals:
        d[y, x] = 0
        q.append((x, y))
    while q:
        x, y = q.popleft()
        for dx, dy in W.MOVES[:4]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < W.N and 0 <= ny < W.N and not walls[ny, nx] and d[ny, nx] == np.inf:
                d[ny, nx] = d[y, x] + 1
                q.append((nx, ny))
    return d


def probe(net, mode, swap, R):
    w3o.EYES.update(mode=mode, swap=swap)
    out = {k: [0, 0.0] for k in STATES}
    for ls in W.TEST_SEEDS:
        for state, (E, F) in STATES.items():
            w = w3o.RawWorld(W.make_land(ls), R)
            w.m_seen[:] = True
            w.m_wall[:] = w.walls
            w.m_shelter[:] = False
            w.m_shelter[w.shelter[1], w.shelter[0]] = True
            for (x, y) in list(w.food):
                w.m_food[y, x] = w.food_full((x, y))
            w.E, w.F = E, F
            goals = [w.shelter] if state == "tired" else [(x, y) for (x, y) in w.food if w.food_full((x, y))]
            d = dist_map(w.walls, goals)
            here = d[w.pos[1], w.pos[0]]

            def closer(a):
                dx, dy = W.MOVES[a]
                nx, ny = w.pos[0] + dx, w.pos[1] + dy
                return a != 4 and not w.walls[ny, nx] and d[ny, nx] < here
            a, _, _ = net.act(w.obs_map(), R3.levels(w, "D3"), w.pos, None, greedy=True)
            out[state][0] += int(closer(a))
            out[state][1] += sum(closer(b) for b in range(5)) / 5.0
    n = len(W.TEST_SEEDS)
    w3o.EYES.update(mode="sorted", swap=False)
    return {k: {"toward": v[0] / n, "chance": v[1] / n} for k, v in out.items()}


def main():
    w3o.configure("RE", 1)
    R = R3.regrowth()
    res = {}
    for name, (d, arm, mode, swap) in BRAINS.items():
        res[name] = {}
        for s in SEEDS:
            p = d / f"{arm}_CS_{s}.npz"
            if p.exists():
                res[name][s] = probe(w3k.load_npz(p, s), mode, swap, R)
    (HERE / "probe.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    for name, v in res.items():
        for st in STATES:
            xs = [v[s][st]["toward"] for s in v]
            ch = [v[s][st]["chance"] for s in v]
            print(f"{name} {st}: toward {np.mean(xs) if xs else float('nan'):.3f} (chance {np.mean(ch) if ch else float('nan'):.3f}; "
                  f"{len(xs)} seeds)")


if __name__ == "__main__":
    main()
