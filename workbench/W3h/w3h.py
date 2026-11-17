"""W3h: pain (questions.md, W3h-frozen). W3d's PYFR (fading parent childhood + Y + FR) in W3's world plus thorns:
2 thorn patches (2 x 2, passable) per land, seen in the 3 x 3 view and written to a sixth map channel ("thorn seen",
its weights start at zero). Every step on a thorn costs HARM energy; in the pain arms it also gives the reward
-P_SCALE * HARM / 8 at that step. The parent is W3's Script, thorn-blind (a plain MapView) or careful (its MapView shows
seen thorns as walls).

  python w3h.py calib                  the harm calibration (Script only, calibration lands) -> calib_h.json
  python w3h.py run ARM SEED [HOURS]   ARM in TH, THP, THw, THPw (train, resumable; then test alone)
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "W3d"))
import w3d  # noqa: E402
from w3d import w3b, B, W, R3  # noqa: E402

OUT = HERE / "output"
CALIB = HERE / "calib_h.json"
HARM_LIST = (4, 6, 8, 12, 16)
PATCH_LIST = (2, 3)
P_SCALE = 1.0
BLOCK = 100_000
ARMS = {"TH": {"pain": False, "careful": False}, "THP": {"pain": True, "careful": False},
        "THw": {"pain": False, "careful": True}, "THPw": {"pain": True, "careful": True}}
CFG = {"harm": None, "patches": None, "pain": False, "careful": False, "zero": False,
       "count": False, "last_harm": 0.0, "curve": None}
BaseWorld, BaseVIN, BaseMapView, base_life_measures, base_reward = (W.World, B.DriveVIN, W.MapView, W.life_measures,
                                                                    R3.reward)


def thorn_corners(land, n):
    """n thorn patches from the land's own seed in a separate stream ([seed, 77]); not on food, shelter or start."""
    rng = np.random.default_rng([land["seed"], 77])
    taken = {land["shelter"], land["start"]}
    for c in land["patches"]:
        taken |= set(W.block_cells(c))
    out = []
    for _ in range(n):
        cand = W._blocks(land["walls"], taken)
        c = cand[int(rng.integers(len(cand)))]
        out.append(c)
        taken |= set(W.block_cells(c))
    return out


class ThornWorld(BaseWorld):
    def __init__(self, land, R):
        self.thorn = np.zeros((W.N, W.N), bool)
        for c in thorn_corners(land, CFG["patches"]):
            for x, y in W.block_cells(c):
                self.thorn[y, x] = True
        self.m_thorn = np.zeros((W.N, W.N), bool)
        self.h = {"thorn_steps": 0, "harm": 0.0, "pain": 0.0, "entries": 0, "opps": 0, "meals": 0, "near_meals": 0}
        super().__init__(land, R)                       # calls write_view, which needs m_thorn
        near = np.zeros((W.N, W.N), bool)
        ys, xs = np.nonzero(self.thorn)
        for y in range(W.N):
            for x in range(W.N):
                near[y, x] = bool(len(xs)) and int(np.min(np.abs(xs - x) + np.abs(ys - y))) <= 2
        self.near = near & ~self.thorn

    def write_view(self):
        super().write_view()
        for cx, cy in self.view_cells():
            self.m_thorn[cy, cx] = self.thorn[cy, cx]

    def step(self, a):
        x, y = self.pos
        was_on = bool(self.thorn[y, x])
        adj = any(0 <= x + dx < W.N and 0 <= y + dy < W.N and self.thorn[y + dy, x + dx] for dx, dy in W.MOVES[:4])
        cur, ate = super().step(a)
        x, y = self.pos
        harm = 0.0
        if self.thorn[y, x]:
            harm = float(CFG["harm"])
            self.E -= harm
            self.h["thorn_steps"] += 1
            self.h["harm"] += harm
            if not was_on:
                self.h["entries"] += 1
            if self.E <= 0:
                self.dead = True
        if adj and not was_on:
            self.h["opps"] += 1
        if ate:
            self.h["meals"] += 1
            self.h["near_meals"] += int(self.near[y, x] or self.thorn[y, x])
        pain = P_SCALE * harm / 8.0 if CFG["pain"] else 0.0
        self.h["pain"] += pain
        CFG["last_harm"] = harm
        if CFG["count"]:
            c = CFG["curve"]
            c["steps"] += 1
            c["thorn"] += int(harm > 0)
            if c["steps"] % BLOCK == 0:
                c["blocks"].append({"step": c["steps"], "thorn_per_1000": 1000.0 * c["thorn"] / BLOCK})
                c["thorn"] = 0
        return cur, ate

    def obs_map(self):
        m = super().obs_map()
        th = np.zeros((1, W.N, W.N)) if CFG["zero"] else self.m_thorn[None].astype(float)
        return np.concatenate([m, th], 0)


class ThornVIN(BaseVIN):
    """W3's DriveVIN with 6 input channels: the first 5 start as W3's own draw, the 6th (thorn seen) at zero."""
    def __init__(self, seed, fixed_map=False):
        B.C = 5
        super().__init__(seed, fixed_map=fixed_map)
        for k in ("W0", "Ws", "Wf", "Wc"):
            self.p[k] = np.concatenate([self.p[k], np.zeros((1, 1, 3, 3))], 1)
        B.C = 6

    def row_norms(self):
        out = super().row_norms()
        out["thorn"] = float(np.sqrt(sum((self.p[k][:, 5] ** 2).sum() for k in ("W0", "Ws", "Wf", "Wc"))))
        return out


class ThornMapView(BaseMapView):
    """The parent's view. Careful: seen thorns look like walls to it. Thorn-blind: W3's MapView unchanged."""
    def __init__(self, w):
        super().__init__(w)
        if CFG["careful"]:
            self.m_wall = self.m_wall | w.m_thorn


def life_measures(w):
    m = base_life_measures(w)
    h = w.h
    m.update({"thorn_steps": h["thorn_steps"], "thorn_per_1000": 1000.0 * h["thorn_steps"] / max(1, w.t),
              "harm": h["harm"], "pain": h["pain"], "entries": h["entries"], "opps": h["opps"],
              "entries_per_opp": (h["entries"] / h["opps"]) if h["opps"] else float("nan"),
              "bout": (h["thorn_steps"] / h["entries"]) if h["entries"] else float("nan"),
              "meals": h["meals"], "near_meal_share": (h["near_meals"] / h["meals"]) if h["meals"] else float("nan"),
              "near_food_share": float(np.mean([w.near[y, x] or w.thorn[y, x] for c in w.land["patches"]
                                                 for x, y in W.block_cells(c)]))})
    return m


def reward(kind, d_before, d_after, cur, died):
    r = base_reward(kind, d_before, d_after, cur, died)
    if CFG["pain"]:
        r -= P_SCALE * CFG["last_harm"] / 8.0
    return r


def install(harm, patches):
    CFG.update(harm=harm, patches=patches)
    W.World = ThornWorld
    W.MapView = ThornMapView
    W.life_measures = life_measures
    R3.reward = reward
    B.DriveVIN = ThornVIN
    B.C = 6


def configure(arm):
    cal = json.loads(CALIB.read_text())
    install(cal["harm"], cal["patches"])
    CFG.update(pain=ARMS[arm]["pain"], careful=ARMS[arm]["careful"])
    w3d.ARMS[arm] = {"parts": "YR", "always": False}
    w3d.configure(arm)
    w3b.OUT = OUT


# --- calibration (Script only; no learned brain) --------------------------------------------------------------------
def script_life(land, R, careful):
    CFG["careful"] = careful
    s = W.Script()
    w = W.World(land, R)
    while not w.done():
        w.step(s.act(W.MapView(w)))
    return w


def calib():
    """Amendment 1 (questions.md): the first (patches, harm), patches 2 before 3 and harm low to high, with thorn-blind
    Script surviving <= 0.60 and careful Script within 0.10 of Script on the same lands with no thorns."""
    R = R3.regrowth()
    install(0, 0)
    ws = [script_life(W.make_land(ls), R, False) for ls in W.CAL_SEEDS]
    none = float(np.mean([w.t >= W.LIFE and not w.dead for w in ws]))
    print({"no_thorns": none}, flush=True)
    rows, chosen = [], None
    for patches in PATCH_LIST:
        for harm in HARM_LIST:
            install(harm, patches)
            res = {}
            for name, careful in (("blind", False), ("careful", True)):
                ws = [script_life(W.make_land(ls), R, careful) for ls in W.CAL_SEEDS]
                res[name] = float(np.mean([w.t >= W.LIFE and not w.dead for w in ws]))
                res[name + "_thorn_per_1000"] = float(np.mean([1000.0 * w.h["thorn_steps"] / w.t for w in ws]))
            rows.append({"patches": patches, "harm": harm, **res})
            print(rows[-1], flush=True)
            if res["blind"] <= 0.60 and res["careful"] >= none - 0.10:
                chosen = (patches, harm)
                break
        if chosen:
            break
    CALIB.write_text(json.dumps({"patches": chosen[0] if chosen else None, "harm": chosen[1] if chosen else None,
                                 "R": R, "no_thorns": none, "rows": rows}, indent=1))
    print("chosen", chosen)


def train_and_test(arm, seed, hours):
    """w3b.train with the training curve (thorn steps per 1,000 per 100,000-step block) kept across pauses."""
    cp = OUT / f"{arm}_{seed}_curve_state.json"
    OUT.mkdir(exist_ok=True)
    CFG["curve"] = json.loads(cp.read_text()) if cp.exists() else {"steps": 0, "thorn": 0, "blocks": []}
    CFG["count"] = True
    done = w3b.train(arm, seed, hours)
    CFG["count"] = False
    cp.write_text(json.dumps(CFG["curve"]))
    if done:
        (OUT / f"{arm}_{seed}_curve.json").write_text(json.dumps(CFG["curve"]["blocks"]))
        w3b.test(arm, seed)
        print("done", arm, seed, flush=True)
    return done


if __name__ == "__main__":
    if sys.argv[1] == "calib":
        calib()
    elif sys.argv[1] == "run":
        arm, seed = sys.argv[2], int(sys.argv[3])
        configure(arm)
        train_and_test(arm, seed, float(sys.argv[4]) if len(sys.argv) > 4 else 4.5)
