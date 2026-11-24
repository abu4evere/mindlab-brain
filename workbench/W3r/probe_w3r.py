"""W3r's learning-curve probe (questions.md: toward-food-alone on a fresh land after k = 0, 1, 3, 5 meals). Written
before any study data.

On each of W3's 50 test lands (W3o's changing colours), the map memory is made fully known, the body is put at the
land's start, hungry (energy 60, tiredness 0), no reflex, and the kept copy's greedy first move is read: "toward" when
it shortens the shortest true path to the nearest full food (W3o's probe). For the module arms the module is given a
fixed small history first: 5 bumps on the wall colour, 1 rest on the shelter colour, 5 untired-and-unfed floor steps
(5 fair negatives for blocked, fed and rested on the floor colour), and k meals on the food colour (k positives).
k = 0 shows food as unknown (0). RV sees its colours (no module) at every k. Chance: the mean share of the 5 moves that
would be toward.

  python probe_w3r.py        -> probe.json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import w3r  # noqa: E402  (the numerical settings before numpy loads)
import numpy as np  # noqa: E402
from w3r import w3k, w3o, W  # noqa: E402
from w3k import R3  # noqa: E402

sys.path.insert(0, str(HERE.parent / "W3o"))
from probe_w3o import dist_map  # noqa: E402

SEEDS = list(range(1, 17))
KS = (0, 1, 3, 5)


def history(w, k):
    c = [w3r.code_of(r) for r in w.codes()]
    for _ in range(5):
        w.mod.add(c[0], 0, True)
        for j in range(3):
            w.mod.add(0, j, False)
    w.mod.add(c[2], 2, True)
    for _ in range(k):
        w.mod.add(c[1], 1, True)


def probe(net, arm, k, R):
    w3r.configure(arm, 1)
    tow, ch = 0, 0.0
    for ls in W.TEST_SEEDS:
        w = w3r.MeaningWorld(W.make_land(ls), R)
        w.m_seen[:] = True
        w.m_wall[:] = w.walls
        w.m_shelter[:] = False
        w.m_shelter[w.shelter[1], w.shelter[0]] = True
        for (x, y) in list(w.food):
            w.m_food[y, x] = w.food_full((x, y))
        w.E, w.F = 60.0, 0.0
        if w.mod is not None:
            history(w, k)
        d = dist_map(w.walls, [(x, y) for (x, y) in w.food if w.food_full((x, y))])
        here = d[w.pos[1], w.pos[0]]

        def closer(a):
            dx, dy = W.MOVES[a]
            nx, ny = w.pos[0] + dx, w.pos[1] + dy
            return a != 4 and not w.walls[ny, nx] and d[ny, nx] < here
        a, _, _ = net.act(w.obs_map(), R3.levels(w, "D3"), w.pos, None, greedy=True)
        tow += int(closer(a))
        ch += sum(closer(b) for b in range(5)) / 5.0
    n = len(W.TEST_SEEDS)
    return {"toward": tow / n, "chance": ch / n}


def main():
    R = R3.regrowth()
    res = {}
    for arm in ("RV", "RM", "RMX", "RE5", "HR"):
        res[arm] = {}
        for s in SEEDS:
            p = HERE / "output" / f"{arm}_CS_{s}.npz"
            if p.exists():
                net = w3k.load_npz(p, s)
                res[arm][s] = {k: probe(net, arm, k, R) for k in KS}
    w3o.EYES.update(mode="sorted", swap=False)
    (HERE / "probe.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    for arm, v in res.items():
        print(arm, {k: round(float(np.mean([v[s][k]["toward"] for s in v])), 3) if v else None for k in KS},
              "seeds", len(v))


if __name__ == "__main__":
    main()
