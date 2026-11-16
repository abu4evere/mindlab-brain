"""W3c: when a need is strong, it takes over (questions.md, W3c-frozen). W3b's training loop (../W3b/w3b.py) with a
brain class that adds the need gate g = max(s, f) to W3's reward map, or starts W0 at zero.

  python w3c.py run ARM SEED [HOURS]     ARM in G, GYFR, Gi, Z0 (train, resumable; then test)
  python w3c.py step0 SEED               D3i (W3's weights) with the gate: walks (a), (b), (c)
  python w3c.py f2 SEED                  the fair ceiling on W3's D3 weights
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "W3b"))
import w3b  # noqa: E402  (puts W3 on the path)
from w3b import B, W, R3  # noqa: E402

OUT = HERE / "output"
BaseVIN = B.DriveVIN
CFG = {"gate": False, "z0": False, "fixed": False}
ARMS = {"G": {"gate": True, "z0": False, "fixed": False, "parts": ""},
        "GYFR": {"gate": True, "z0": False, "fixed": False, "parts": "YR"},
        "Gi": {"gate": True, "z0": False, "fixed": True, "parts": ""},
        "Z0": {"gate": False, "z0": True, "fixed": False, "parts": ""}}


class GatedVIN(BaseVIN):
    """W3's DriveVIN; with CFG['gate'] the reward map is (1-g) W0 + s Ws + f Wf + c (1-g) Wc + b, g = max(s, f);
    with CFG['z0'] W0 starts at zero; CFG['fixed'] gives D3i's fixed links (the fixed_map argument is overridden)."""
    def __init__(self, seed, fixed_map=False):
        super().__init__(seed, fixed_map=CFG["fixed"])
        self.gate = CFG["gate"]
        if CFG["z0"]:
            self.p["W0"][:] = 0.0

    def plan(self, maps, levels):
        if not self.gate:
            return super().plan(maps, levels)
        levels = np.asarray(levels, float)
        g = np.maximum(levels[:, 0], levels[:, 1])
        p, T = self.p, maps.shape[0]
        N, A = B.N, B.A
        c_x = B.cols(maps)
        Wstack = np.stack([p["W0"].reshape(-1), p["Ws"].reshape(-1), p["Wf"].reshape(-1), p["Wc"].reshape(-1)], 1)
        parts = c_x @ Wstack
        lev = np.stack([1.0 - g, levels[:, 0], levels[:, 1], levels[:, 2] * (1.0 - g)], 1)
        lev_cells = np.repeat(lev, N * N, axis=0)
        r = (parts * lev_cells).sum(1) + p["br"][0]
        c_r = B.cols(r.reshape(T, 1, N, N))
        Rq = c_r @ p["Wq"].reshape(A, 9).T
        q, trace, idx = Rq, [], np.arange(T * N * N)
        Wv9 = p["Wv"].reshape(A, 9).T
        for _ in range(B.K - 1):
            am = q.argmax(1)
            c_v = B.cols(q[idx, am].reshape(T, 1, N, N))
            trace.append((c_v, am))
            q = Rq + c_v @ Wv9
        return (T, c_x, lev_cells, c_r, trace, q)


def configure(arm):
    c = ARMS[arm] if arm in ARMS else {"gate": arm == "D3i_gate", "z0": False, "fixed": arm == "D3i_gate", "parts": ""}
    CFG.update(gate=c["gate"], z0=c["z0"], fixed=c["fixed"])
    B.DriveVIN = GatedVIN
    w3b.OUT = OUT
    parts = {a: v["parts"] for a, v in ARMS.items()}
    orig = w3b.parts_of
    w3b.parts_of = lambda a: parts[a] if a in parts else orig(a)


class F2Policy(w3b.FPolicy):
    """The fair ceiling: hungry -> the nearest cell remembered as full food; tired -> the shelter; else W3's D3."""
    def act(self, w):
        s, f = w.deficits()
        passable = lambda cell: not w.m_wall[cell[1], cell[0]]
        if s >= w3b.HIGH["s"]:
            foods = [(x, y) for y in range(B.N) for x in range(B.N) if w.m_food[y, x]]
            if foods and w.pos not in foods:
                a = W.bfs_path(passable, w.pos, foods)
                if a is not None:
                    self.walks += 1
                    return a
        if f >= w3b.HIGH["f"] and w.m_shelter.any() and w.pos != w.shelter:
            ys, xs = np.nonzero(w.m_shelter)
            a = W.bfs_path(passable, w.pos, [(int(xs[0]), int(ys[0]))])
            if a is not None:
                self.walks += 1
                return a
        return self.net.act(w.obs_map(), R3.levels(w, "D3"), w.pos, self.rng)[0]


def f2(seed):
    configure("Z0")                                           # any non-gated config; F2 uses W3's own D3 class
    B.DriveVIN = BaseVIN
    R = R3.regrowth()
    net = R3.load("D3", seed)
    lives = []
    for ls in W.TEST_SEEDS:
        land = W.make_land(ls)
        rng = np.random.default_rng(ls)
        pol = F2Policy(net, rng)
        _, m = w3b.run_life_f(pol, land, R, rng)
        m["f_walks"] = pol.walks
        lives.append(m)
    OUT.mkdir(exist_ok=True)
    (OUT / f"test_F2_{seed}.json").write_text(json.dumps(lives))
    print("F2", seed, round(float(np.mean([x["survived"] for x in lives])), 3), flush=True)
    return lives


def step0(seed):
    configure("D3i_gate")
    res = w3b.step0("D3i", seed)                                # writes OUT/step0_D3i_<seed>.json (w3b.OUT = OUT)
    return res


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "run":
        arm, seed = sys.argv[2], int(sys.argv[3])
        configure(arm)
        if w3b.train(arm, seed, float(sys.argv[4]) if len(sys.argv) > 4 else 4.5):
            w3b.test(arm, seed)
            print("done", arm, seed, flush=True)
    elif cmd == "step0":
        step0(int(sys.argv[2]))
    elif cmd == "f2":
        f2(int(sys.argv[2]))
