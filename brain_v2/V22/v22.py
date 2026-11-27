"""V2-2 Goals (questions.md, V22-frozen): a goal layer and level on the walker (W3n's DriveVIN), learned by adult
fine-tuning in CW2's world.

GoalVIN = DriveVIN plus new parameters, all zero at the start:
  G0, Gs, Gf, Gc (1, 1, 3, 3): the goal channel's taps in the old reward map terms (weighted by 1, s, f, c);
  Wg (1, 6, 3, 3): a new term over all six channels weighted by the goal level g.
  r = r_old(5 channels, levels s, f, c)  +  sum_k lev_k * conv(G_k, goal)  +  g * conv(Wg, [5 channels, goal]).
r_old is computed exactly as DriveVIN computes it, and the new terms are added after, so with the new weights at 0 the
walker is DriveVIN bit for bit (the exact zero check). With the goal channel empty and g = 0, a fine-tuned GoalVIN is a
DriveVIN with its old parameters (saved as such for the Bob Profile and the plain-land gate).
Fine-tuning: W3's actor-critic (64-step segments, gamma 0.97, lr 0.01, entropy 0.01, clip 1.0) with the drive reward
unchanged (R3.reward, kind D3), in CW2's world with the consequence model and the station; the walker's reflexes act as
in training (w3m: rfx.act after net.act). Hand steps happen between the walker's moves; each walker move's reward is the
drive change from that move until the walker's next move (hand-step meals included).
  python v22.py train ARM SEED STEPS [pilot]  -> output/net_{ARM}_{SEED}.npz (+ checkpoints, a log)
  python v22.py test ARM SEED [test|unseen]    -> output/{test|unseen}_{ARM}_{SEED}.jsonl
"""
from __future__ import annotations

import json
import pickle
import platform
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / "body" / "CW2"))
import cw2  # noqa: E402  (W3r's chain first)
import numpy as np  # noqa: E402
from cw2 import cw1, W, w3k, R3  # noqa: E402

B = w3k.B
w3m = cw2.w3m
OUT = HERE / "output"
BRAINS = HERE.parents[1] / "body" / "CW1" / "brains"
V22_SEED = 20261130
TEST_LANDS, UNSEEN_LANDS = range(990001, 990051), range(995001, 995051)
ARMS = {"GOAL": ("real", True), "GOAL-NOFLOOR": ("real", False), "FT-NOGOAL": ("none", True),
        "SHAM-GOAL": ("sham", True), "GOAL-ABLATE": ("none", True)}
NEW = ("G0", "Gs", "Gf", "Gc", "Wg")
CKPT_EVERY = 100_000
SNAPS = (300_000, 600_000)          # the length rule's candidates (questions.md); a snapshot equals a run stopped there


class GoalVIN(B.DriveVIN):
    def __init__(self, seed):
        super().__init__(seed, fixed_map=False)
        for k in ("G0", "Gs", "Gf", "Gc"):
            self.p[k] = np.zeros((1, 1, 3, 3))
        self.p["Wg"] = np.zeros((1, B.C + 1, 3, 3))

    def plan(self, maps, levels):
        """maps (T, 6, N, N), levels (T, 4) = (s, f, c, g). The old reward map exactly, then the goal terms."""
        p, T, N = self.p, maps.shape[0], B.N
        levels = np.asarray(levels, float)
        c_x = B.cols(np.ascontiguousarray(maps[:, :B.C]))
        Wstack = np.stack([p["W0"].reshape(-1), p["Ws"].reshape(-1), p["Wf"].reshape(-1), p["Wc"].reshape(-1)], 1)
        parts = c_x @ Wstack
        lev = np.concatenate([np.ones((T, 1)), levels[:, :3]], 1)
        lev_cells = np.repeat(lev, N * N, axis=0)
        r = (parts * lev_cells).sum(1) + p["br"][0]
        g_x = B.cols(np.ascontiguousarray(maps[:, B.C:B.C + 1]))         # (T*N*N, 9)
        f_x = B.cols(np.ascontiguousarray(maps))                         # (T*N*N, 54)
        gstack = np.stack([p[k].reshape(-1) for k in ("G0", "Gs", "Gf", "Gc")], 1)
        g_cells = np.repeat(levels[:, 3], N * N)
        r = r + (g_x @ gstack * lev_cells).sum(1) + g_cells * (f_x @ p["Wg"].reshape(-1))
        c_r = B.cols(r.reshape(T, 1, N, N))
        Rq = c_r @ p["Wq"].reshape(B.A, 9).T
        q, trace, idx = Rq, [], np.arange(T * N * N)
        Wv9 = p["Wv"].reshape(B.A, 9).T
        for _ in range(B.K - 1):
            am = q.argmax(1)
            c_v = B.cols(q[idx, am].reshape(T, 1, N, N))
            trace.append((c_v, am))
            q = Rq + c_v @ Wv9
        return (T, c_x, lev_cells, c_r, trace, q, g_x, f_x, g_cells)

    def backprop(self, fw, rows, dl, dv):
        p, N, A = self.p, B.N, B.A
        T, c_x, lev_cells, c_r, trace, q, g_x, f_x, g_cells = fw
        g = {k: np.zeros_like(v) for k, v in p.items()}
        qa = q[rows]
        g["Wo"] += dl.T @ qa
        g["bo"] += dl.sum(0)
        g["wv"] += dv @ qa
        g["bv"] += dv.sum()
        dq = np.zeros((T * N * N, A))
        np.add.at(dq, rows, dl @ p["Wo"] + dv[:, None] * p["wv"][None, :])
        dRq = np.zeros_like(dq)
        Wv9 = p["Wv"].reshape(A, 9)
        idx = np.arange(T * N * N)
        for c_v, am in reversed(trace):
            dRq += dq
            g["Wv"] += (dq.T @ c_v).reshape(A, 1, 3, 3)
            dv_map = B.uncols(dq @ Wv9, T).ravel()
            dq = np.zeros((T * N * N, A))
            dq[idx, am] = dv_map
        dRq += dq
        g["Wv"] *= self.mask
        g["Wq"] += (dRq.T @ c_r).reshape(A, 1, 3, 3)
        dr = B.uncols(dRq @ p["Wq"].reshape(A, 9), T).ravel()
        g["br"] += dr.sum()
        gW = c_x.T @ (dr[:, None] * lev_cells)
        for j, k in enumerate(("W0", "Ws", "Wf", "Wc")):
            g[k] += gW[:, j].reshape(1, B.C, 3, 3)
        gG = g_x.T @ (dr[:, None] * lev_cells)
        for j, k in enumerate(("G0", "Gs", "Gf", "Gc")):
            g[k] += gG[:, j].reshape(1, 1, 3, 3)
        g["Wg"] += (f_x.T @ (dr * g_cells)).reshape(1, B.C + 1, 3, 3)
        return g

    def old_params(self):
        """The DriveVIN this walker equals when the goal channel is empty and g = 0."""
        return {k: v.copy() for k, v in self.p.items() if k not in NEW}


def goalvin_from_rms(seed):
    net = GoalVIN(seed)
    old = w3k.load_npz(BRAINS / f"RM_CS_{seed}.npz", seed)
    for k in old.p:
        net.p[k] = old.p[k].copy()
    return net


def best_target(model, h, u_now):
    """CW2's target rule with its value: (look, best experienced value) or (None, 0)."""
    Vp = model.values(extra=(h,), bonus=0.0)[cw2.H - 1]
    uverbs = [v for v in model.verbs if v == "take" or v.startswith("op")]

    def best_at(u):
        if h == (0, 0) and u == 0:
            return 0.0
        return max(model._q(model.key(h, u, v), Vp, 0.0) for v in uverbs)
    here = max([best_at(u_now)] + [model._q(model.key(h, u_now, v), Vp, 0.0) for v in model.verbs if v not in uverbs])
    best, look = here, None
    for u in sorted(model.places):
        if u != u_now:
            b = best_at(u)
            if b > best + 1e-9:
                best, look = b, u
    return (look, best) if (look is not None and best > 0) else (None, 0.0)


class Goal:
    """Chooses and clears the goal place (CW2's rules); kind 'real', 'sham' or 'none'; floor_kept True/False."""

    def __init__(self, kind, floor_kept, srng):
        self.kind, self.floor_kept, self.srng = kind, floor_kept, srng
        self.cell, self.hands, self.look, self.g = None, None, None, 0.0
        self.starts = 0

    def update(self, w, model, h, u):
        if self.kind == "none":
            return
        ok = w.above_floor() or not self.floor_kept
        if self.cell is not None and (h != self.hands or w.pos == self.cell or not ok):
            self.cell, self.hands, self.look, self.g = None, None, None, 0.0
        if self.cell is None and ok:
            look, val = best_target(model, h, u)
            if look is None:
                return
            dist = cw2.path_dists(lambda c: not w.m_wall[c[1], c[0]], w.pos)
            cells = [cl for cl in model.places[look] if cl in dist and cl != w.pos]
            if not cells:
                return
            real = min(cells, key=lambda cl: (dist[cl], cl))
            cell = real
            if self.kind == "sham":
                bad = model.places[look]
                opts = [cl for cl in dist if w.m_seen[cl[1], cl[0]] and cl not in bad and cl != w.pos]
                if not opts:
                    return
                gap = min(abs(dist[cl] - dist[real]) for cl in opts)
                near = sorted(cl for cl in opts if abs(dist[cl] - dist[real]) == gap)
                cell = near[int(self.srng.integers(len(near)))]
            self.cell, self.hands, self.look = cell, h, look
            self.g = min(1.0, val / (2.0 * W.MEAL))
            self.starts += 1

    def layer(self):
        m = np.zeros((W.N, W.N))
        if self.cell is not None:
            m[self.cell[1], self.cell[0]] = 1.0
        return m


def observe(w, goal):
    m = w.obs_map()
    lev = list(R3.levels(w, "D3"))
    return np.concatenate([m, goal.layer()[None]], 0), lev + [goal.g]


def configure(seed):
    cw2.configure("GUIDE-REFLEX", seed)
    W.World = cw2.CW2World


def life(net, seed, ls, arm, learn=None, rng=None, on_step=None, ablate=False):
    """One life in CW2's world. learn: None (test) or the training state (segment, counters)."""
    kind, floor_kept = ARMS[arm]
    if ablate:
        kind = "none"
    land, R = W.make_land(ls), R3.regrowth()
    rng = rng if rng is not None else np.random.default_rng(ls)
    rfx = w3m.Reflex()
    w = W.World(land, R)
    crng = np.random.default_rng([cw1.CW1_SEED, seed, ls])
    model = cw2.Model(w.K, crng)
    goal = Goal(kind, floor_kept, np.random.default_rng([V22_SEED, seed, ls]))
    pend = None                                          # the walker's last move, waiting for its reward
    st = {"walker_steps": 0, "hand_acts": 0, "toward_fed": 0, "toward_hungry": 0, "goal_steps_fed": 0,
          "goal_steps_hungry": 0}

    def close(pend):
        if learn is None or pend is None:
            return
        m, lev, cell, a, d0, cur, val = pend
        r = R3.reward("D3", d0, w.drive(), cur, w.dead)
        seg = learn["seg"]
        for k, v in (("maps", m), ("levels", lev), ("cells", cell), ("acts", a), ("rews", r), ("vals", val)):
            seg[k].append(v)
        learn["total"] += 1
        if len(seg["acts"]) == B.SEG or w.done() or learn["total"] >= learn["steps"] or learn["total"] in SNAPS:
            flush(learn, w, goal)
        if learn["total"] in SNAPS and learn["total"] < learn["steps"]:
            np.savez(OUT / f"snap{learn['total'] // 1000}k_{learn['name']}.npz", **learn["net"].p)   # = a run stopped here

    while not w.done():
        h, u = w.held(), w.underfoot()
        model.feel(u, w.pos)
        goal.update(w, model, h, u)
        m, lev = observe(w, goal)
        a_net, _, val = net.act(m, lev, w.pos, rng)
        a = rfx.act(w, a_net)
        if w.moment() and w.above_floor():
            v, _ = model.choose(h, u)
            if v != cw1.PASS:
                h2, gain, changed = w.hand_step(v)
                model.learn(h, u, v, h2, gain)
                st["hand_acts"] += 1
                continue
        close(pend)
        pend = None
        if learn is not None and learn["total"] >= learn["steps"]:
            break
        d0, pos0 = w.drive(), w.pos
        band = None
        if goal.cell is not None:
            band = "fed" if w.E >= 150 else "hungry"
            st[f"goal_steps_{band}"] += 1
            dist0 = abs(pos0[0] - goal.cell[0]) + abs(pos0[1] - goal.cell[1])
        cur, _ = w.step(a)
        if band is not None:
            st[f"toward_{band}"] += abs(w.pos[0] - goal.cell[0]) + abs(w.pos[1] - goal.cell[1]) < dist0
        st["walker_steps"] += 1
        pend = (m, lev, pos0, a, d0, cur, val)
        if on_step is not None:
            on_step(w, a, d0, cur)
    close(pend)
    mm = W.life_measures(w)
    mm.update({"land": ls, "chains": w.stats["chains"], "joins": w.stats["joins"], "goal_starts": goal.starts,
               "first_join": w.stats["first_join"], **st})
    return w, mm


def flush(learn, w, goal):
    seg, net = learn["seg"], learn["net"]
    if not seg["acts"]:
        return
    if w.dead or w.t >= W.LIFE:
        G = 0.0
    else:
        m, lev = observe(w, goal)
        _, _, G = net.act(m, lev, w.pos, learn["rng"])
    rets = []
    for rr in reversed(seg["rews"]):
        G = rr + B.GAMMA * G
        rets.append(G)
    rets = rets[::-1]
    learn["vloss_sum"] = learn.get("vloss_sum", 0.0) + float(sum((g_ - v_) ** 2 for g_, v_ in zip(rets, seg["vals"])))
    learn["vloss_n"] = learn.get("vloss_n", 0) + len(rets)
    net.update(seg["maps"], seg["levels"], seg["cells"], seg["acts"], rets)
    learn["updates"] += 1
    learn["seg"] = {"maps": [], "levels": [], "cells": [], "acts": [], "rews": [], "vals": []}


def machine():
    return {"platform": platform.platform(), "python": platform.python_version(), "numpy": np.__version__,
            "node": platform.node()}


def train(arm, seed, steps, tag=""):
    OUT.mkdir(exist_ok=True)
    name = f"{arm}_{seed}{tag}"
    ck = OUT / f"ckpt_{name}.pkl"
    if ck.exists():
        learn = pickle.loads(ck.read_bytes())
        net = GoalVIN(seed)
        net.p = learn.pop("p")
        rng = np.random.default_rng()
        rng.bit_generator.state = learn.pop("rng_state")
    else:
        net, rng = goalvin_from_rms(seed), np.random.default_rng([V22_SEED, seed, 7])
        learn = {"total": 0, "life": 0, "updates": 0, "log": []}
    configure(seed)
    learn.update(name=name, net=net, rng=rng, steps=steps, seg={"maps": [], "levels": [], "cells": [], "acts": [], "rews": [], "vals": []})
    t0 = time.time()
    next_ck = (learn["total"] // CKPT_EVERY + 1) * CKPT_EVERY
    while learn["total"] < steps:
        learn["life"] += 1
        ls = 70_000_000 + 1000 * seed + learn["life"]          # training lands, never test lands
        w, m = life(net, seed, ls, arm, learn=learn, rng=rng)
        if learn["total"] >= next_ck or learn["total"] >= steps:
            row = {"step": learn["total"], "life": learn["life"], "Wg_norm": float(np.linalg.norm(net.p["Wg"])),
                   "G_norm": float(sum(np.linalg.norm(net.p[k]) for k in ("G0", "Gs", "Gf", "Gc"))),
                   "critic_loss": learn.get("vloss_sum", 0.0) / max(1, learn.get("vloss_n", 0)),
                   "chains_last_life": m["chains"], "lifespan_last_life": m["lifespan"],
                   "seconds": round(time.time() - t0, 1)}
            learn["log"].append(row)
            learn["vloss_sum"], learn["vloss_n"] = 0.0, 0
            print(json.dumps(row), flush=True)
            state = {k: v for k, v in learn.items() if k not in ("net", "rng", "seg")}
            state["p"] = {k: v.copy() for k, v in net.p.items()}
            state["rng_state"] = rng.bit_generator.state
            ck.write_bytes(pickle.dumps(state))
            next_ck += CKPT_EVERY
    np.savez(OUT / f"net_{name}.npz", **net.p)
    np.savez(OUT / f"old_{name}.npz", **net.old_params())
    (OUT / f"trainlog_{name}.json").write_text(json.dumps({"log": learn["log"], "machine": machine()}))
    print("trained", arm, seed, steps, flush=True)


def load(arm, seed):
    net = GoalVIN(seed)
    src = "GOAL" if arm == "GOAL-ABLATE" else arm
    with np.load(OUT / f"net_{src}_{seed}.npz") as z:
        for k in net.p:
            net.p[k] = z[k].copy()
    return net


def test(arm, seed, lands="test"):
    configure(seed)
    net = load(arm, seed)
    L = {"test": TEST_LANDS, "unseen": UNSEEN_LANDS}[lands]
    path = OUT / f"{lands}_{arm}_{seed}.jsonl"
    done = set()
    if path.exists():
        done = {json.loads(x)["land"] for x in path.read_text().splitlines() if x.strip()}
    keep = cw1.CW1_SEED
    with open(path, "a") as f:
        for ls in L:
            if ls in done:
                continue
            if lands == "unseen":
                cw1.CW1_SEED = V22_SEED + 1                    # a fresh deal of looks, operations and spots
            try:
                _, m = life(net, seed, ls, arm, ablate=(arm == "GOAL-ABLATE"))
            finally:
                cw1.CW1_SEED = keep
            m.update({"arm": arm, "seed": seed, "machine": machine()})
            f.write(json.dumps(m, default=float) + "\n")
            f.flush()
    print("tested", arm, seed, lands, flush=True)


if __name__ == "__main__":
    a = sys.argv
    if a[1] == "train":
        train(a[2], int(a[3]), int(a[4]), "_pilot" if len(a) > 5 and a[5] == "pilot" else "")
    elif a[1] == "test":
        test(a[2], int(a[3]), a[4] if len(a) > 4 else "test")
