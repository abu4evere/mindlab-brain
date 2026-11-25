"""CX2: learned meanings in Crafter (CX2/questions.md, CX2-frozen; the creator's sign-off 24 Nov 2026).

MBb as it is (no training). The bridge's told meanings are replaced, in LEARN, by meaning tables reset at every life's
start and learned from what the body feels:
  - blocked:   a move (while awake) into a cell of a kind (the kind seen there at that moment) did / did not move it;
  - fed-food, fed-drink: per interaction bout (consecutive "do"s on the same target; it ends when the target's kind
    changes, the body does anything else, food or drink rises, or after 5 "do"s): positive if that need rose during
    the bout; a fair negative for that need only if it was below its maximum (9) before every "do" of the bout.
  prediction = positives / (positives + fair negatives), 0 before any trial.
The brain's layers (amendment 1, before data): food = max(P(fed-food), P(fed-drink)); wall = P(blocked) except where
food > 0.5 (as CX1: a food place is somewhere the brain goes, and the hand turns going there into face and "do").
The hand (every arm): CX1's rule (a move into a cell whose food layer is above 0.5 = face it, then "do"; stay = sleep)
plus bump and poke (a move that is blocked = "do" on that cell until the bout ends), except LEARN-NP (no poke).

Arms: learn, named (CX1's told meanings, bridge.Memory), blind (learned layers held at 0), learn_np, random5p (random
moves, the tables updated as LEARN and used by the hand).

  python cx2.py ARM BUDGET [FIRST_SEED] [OUTDIR]     -> OUTDIR/<arm>.jsonl (resumes), as play.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import crafter

import bridge as BR
import play as P
from bridge import N, H, CH_WALL, CH_UNSEEN, CH_FOOD, CH_SHELTER, CH_UNC, A, DIRS, FACE, TAU

HERE = Path(__file__).parent
K = len(BR.SEM)                                   # 18 kinds
MAX_DOS = 5
ARMS = ("learn", "named", "blind", "learn_np", "random5p")
FOOD, DRINK = 0, 1


class Tables:
    """Per kind: blocked, and fed-food / fed-drink, as positive and fair-negative counts."""

    def __init__(self):
        self.bp, self.bn = np.zeros(K), np.zeros(K)
        self.fp, self.fn = np.zeros((K, 2)), np.zeros((K, 2))

    @staticmethod
    def _p(pos, neg):
        n = pos + neg
        return np.where(n > 0, pos / np.maximum(n, 1), 0.0)

    def blocked(self):
        return self._p(self.bp, self.bn)

    def fed(self):
        return self._p(self.fp, self.fn)          # (K, 2): food, drink

    def food_layer(self):
        return self.fed().max(1)


class LearnPlayer:
    """The CX2 player. arm in ARMS; net is MBb (None for random5p)."""

    def __init__(self, net, rng, arm, perm=None):
        assert arm in ARMS
        self.net, self.rng, self.arm = net, rng, arm
        self.perm = perm                          # checks only: a relabelling of kind ids (must change nothing)

    def reset(self):
        self.tab = Tables()
        self.mem = BR.Memory()                    # CX1's told meanings (used by NAMED only)
        self.kind = np.full((64, 64), -1, int)    # the kind last seen per cell (used by the learned eyes)
        self.last = np.full((64, 64), -1, int)
        self.t, self.facing, self.visited = 0, (0, 1), set()
        self.bout, self.pending, self.prev = None, None, None
        self.n_bouts = self.n_pokes = self.n_moves_blocked = self.bout_hurt = 0
        self.first = {"drink": None, "food": None}

    # ── eyes ────────────────────────────────────────────────────────────────────────────────────────────────────
    def sem(self, info):
        s = info["semantic"]
        return self.perm[s] if self.perm is not None else s

    def write(self, sem, pos):
        x0, y0 = pos
        for x in range(x0 - 4, x0 + 5):
            for y in range(y0 - 3, y0 + 4):
                if 0 <= x < 64 and 0 <= y < 64:
                    self.kind[x, y], self.last[x, y] = int(sem[x, y]), self.t

    def window(self, pos):
        m = np.zeros((5, N, N))
        food = self.tab.food_layer() if self.arm != "blind" else np.zeros(K)
        blk = self.tab.blocked() if self.arm != "blind" else np.zeros(K)
        x0, y0 = pos
        for wy in range(N):
            for wx in range(N):
                x, y = x0 + wx - H, y0 + wy - H
                if not (0 <= x < 64 and 0 <= y < 64):
                    m[CH_WALL, wy, wx] = 1.0
                    continue
                k = self.kind[x, y]
                if k < 0:
                    m[CH_UNSEEN, wy, wx] = m[CH_UNC, wy, wx] = 1.0
                    continue
                f = food[k]
                w = blk[k] if f <= 0.5 else 0.0
                m[CH_FOOD, wy, wx], m[CH_WALL, wy, wx] = f, w
                if w <= 0.5:
                    m[CH_UNC, wy, wx] = 1.0 - np.exp(-(self.t - self.last[x, y]) / TAU)
        m[CH_SHELTER, H, H] = 1.0
        return m

    # ── the bout ────────────────────────────────────────────────────────────────────────────────────────────────
    def close_bout(self):
        b = self.bout
        if b is None:
            return
        for j in (FOOD, DRINK):
            if b["rose"][j]:
                self.tab.fp[b["kind"], j] += 1
            elif b["ok"][j]:
                self.tab.fn[b["kind"], j] += 1
        self.bout = None
        self.measure_first()

    def measure_first(self):
        """Evaluation only (never read by the eyes or the hand): the step at which the tables first rank water (drink)
        and cow (food) above every other kind seen so far, after a positive."""
        fed = self.tab.fed()
        seen = set(int(k) for k in np.unique(self.kind[self.kind >= 0]))
        for need, j, name in (("drink", DRINK, "water"), ("food", FOOD, "cow")):
            k = BR.SEM.index(name)
            if self.perm is not None:
                k = int(self.perm[k])
            if self.first[need] is None and self.tab.fp[k, j] > 0 and all(fed[k, j] > fed[o, j] for o in seen if o != k):
                self.first[need] = self.t

    # ── the hand ────────────────────────────────────────────────────────────────────────────────────────────────
    def choose(self, m, info):
        if self.arm == "random5p":
            return int(self.rng.integers(5))
        lev = BR.levels(info["inventory"], m)
        fw = self.net.plan(m[None], lev[None])
        z, _ = self.net.head(fw, np.array([H * N + H]))
        return int(self.rng.choice(5, p=BR.softmax(z[0])))

    def act(self, env, info):
        pos = tuple(int(v) for v in info["player_pos"])
        sem = self.sem(info)
        self.write(sem, pos)
        if self.arm == "named":
            self.mem.write(info["semantic"], pos, self.t, BR.ripe_plants(env))
        self.visited.add(pos)
        asleep = bool(env._player.sleeping)
        inv = dict(info["inventory"])
        b = self.bout
        if b is not None and b["poke"] and not asleep and self.facing == b["dir"] and int(sem[b["cell"]]) == b["kind"]:
            act = A["do"]                                           # the poke goes on until the bout ends
            self.prev = {"kind": "do", "cell": b["cell"], "dir": b["dir"], "inv": inv, "asleep": asleep}
            self.t += 1
            return act
        m = self.mem.window(pos, self.t) if self.arm == "named" else self.window(pos)
        a = self.choose(m, info)
        self.t += 1
        if a == 4:
            self.close_bout()
            self.prev = {"kind": "sleep", "asleep": asleep}
            return A["sleep"]
        dx, dy = DIRS[a]
        cell = (pos[0] + dx, pos[1] + dy)
        if not (0 <= cell[0] < 64 and 0 <= cell[1] < 64):
            self.close_bout()
            self.prev = {"kind": "edge", "asleep": asleep}
            return A[FACE[a]]
        if m[CH_FOOD, H + dy, H + dx] > 0.5:                           # CX1's rule: into food, face it, then "do"
            if self.facing == (dx, dy):
                k = int(sem[cell])
                if self.bout is None or self.bout["cell"] != cell or self.bout["kind"] != k:
                    self.close_bout()
                    self.open_bout(cell, (dx, dy), k, poke=False)
                self.prev = {"kind": "do", "cell": cell, "dir": (dx, dy), "inv": inv, "asleep": asleep}
                return A["do"]
            self.close_bout()
            self.prev = {"kind": "turn", "asleep": asleep}
            return A[FACE[a]]
        self.close_bout()
        self.prev = {"kind": "move", "cell": cell, "dir": (dx, dy), "from": pos, "k": int(sem[cell]),
                     "asleep": asleep}
        return A[FACE[a]]

    def open_bout(self, cell, d, k, poke):
        self.bout = {"cell": cell, "dir": d, "kind": k, "poke": poke, "dos": 0, "rose": [False, False],
                     "ok": [True, True]}
        self.n_bouts += 1
        self.n_pokes += poke

    def after(self, env):
        p = env._player
        self.facing = tuple(int(v) for v in p.facing)
        pr, self.prev = self.prev, None
        if pr is None or pr["asleep"]:
            return
        if pr["kind"] == "move":
            moved = tuple(int(v) for v in p.pos) != pr["from"]
            if moved:
                self.tab.bn[pr["k"]] += 1
            else:
                self.tab.bp[pr["k"]] += 1
                self.n_moves_blocked += 1
                if self.arm != "learn_np":                           # bump and poke
                    self.open_bout(pr["cell"], pr["dir"], pr["k"], poke=True)
            return
        if pr["kind"] == "do" and self.bout is not None:
            b, inv0, inv1 = self.bout, pr["inv"], p.inventory
            b["dos"] += 1
            for j, name in ((FOOD, "food"), (DRINK, "drink")):
                b["ok"][j] = b["ok"][j] and inv0[name] < 9
                b["rose"][j] = b["rose"][j] or inv1[name] > inv0[name]
            self.bout_hurt += int(inv1["health"] < inv0["health"])
            kind_now = int(self.perm[env._sem_view()[b["cell"]]]) if self.perm is not None else \
                int(env._sem_view()[b["cell"]])
            if kind_now != b["kind"] or any(b["rose"]) or b["dos"] >= MAX_DOS:
                self.close_bout()

    def extra(self):
        self.close_bout()
        fed = self.tab.fed()
        return {"bouts": self.n_bouts, "pokes": self.n_pokes, "blocked_moves": self.n_moves_blocked,
                "bout_hurt": self.bout_hurt, "first_drink": self.first["drink"], "first_food": self.first["food"],
                "trials_fed": int((self.tab.fp + self.tab.fn).sum()), "trials_blocked": int((self.tab.bp + self.tab.bn).sum())}


def main():
    arm, budget = sys.argv[1], int(sys.argv[2])
    first = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    out = Path(sys.argv[4]) if len(sys.argv) > 4 else HERE / "CX2" / "output"
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{arm}.jsonl"
    recs = [json.loads(x) for x in open(path)] if path.exists() else []
    total, s = sum(r["steps"] for r in recs), first + len(recs)
    net = BR.load(str(HERE / "mbb_seed1.npz")) if arm != "random5p" else None
    while total < budget:
        env = crafter.Env(seed=s)
        player = LearnPlayer(net, np.random.default_rng(s), arm)
        t0 = time.time()
        rec = P.life(env, player)
        rec.update(player.extra())
        rec.update(seed=s, seconds=round(time.time() - t0, 1))
        recs.append(rec)
        total += rec["steps"]
        with open(path, "a") as f:
            f.write(json.dumps(rec) + "\n")
        s += 1
    sc, rates = P.score(recs)
    print(f"{arm}: {len(recs)} lives, {total} steps, mean length {np.mean([r['steps'] for r in recs]):.0f}, "
          f"Crafter score {sc:.2f}%")
    print({k: v for k, v in rates.items() if v > 0})


if __name__ == "__main__":
    main()
