"""CX2 checks, before any data (CX2/questions.md). Prints All: PASS or the failures."""
import types

import numpy as np
import crafter

import bridge as BR
import play as P
import cx2

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


NET = BR.load("mbb_seed1.npz")
SEM = BR.SEM
K = {n: i for i, n in enumerate(SEM)}

# 1. NAMED's eyes are CX1's: on the same life prefix, the NAMED player's window equals a CX1 BrainPlayer's window
env = crafter.Env(seed=1)
env.reset()
cx1, nm = BR.BrainPlayer(NET, np.random.default_rng(1)), cx2.LearnPlayer(NET, np.random.default_rng(1), "named")
cx1.reset()
nm.reset()
info, same = P.first_info(env), True
for _ in range(40):
    pos = tuple(int(v) for v in info["player_pos"])
    cx1.mem.write(info["semantic"], pos, cx1.t, BR.ripe_plants(env))
    nm.mem.write(info["semantic"], pos, nm.t, BR.ripe_plants(env))
    same &= np.array_equal(cx1.mem.window(pos, cx1.t), nm.mem.window(pos, nm.t))
    a = cx1.act(env, info)
    nm.t += 1
    _, _, done, info = env.step(a)
    cx1.after(env)
    if done:
        break
check(f"NAMED's eyes equal CX1's over a life prefix [{same}]", bool(same))

# 2. a perfect table gives LEARN the told meanings (cells without plants, which CX1 marks by ripeness, not kind)
lp = cx2.LearnPlayer(NET, np.random.default_rng(2), "learn")
lp.reset()
env = crafter.Env(seed=2)
env.reset()
info = P.first_info(env)
for _ in range(30):
    _, _, done, info = env.step(int(np.random.default_rng(_).integers(1, 5)))
pos = tuple(int(v) for v in info["player_pos"])
lp.t = nm.t = 0
lp.write(info["semantic"], pos)
nm.mem = BR.Memory()
nm.mem.write(info["semantic"], pos, 0, BR.ripe_plants(env))
for n, k in K.items():
    food, wall = n in ("water", "cow"), (n not in BR.GROUND) and n not in ("water", "cow")
    (lp.tab.bp if (n not in BR.GROUND) else lp.tab.bn)[k] += 1
    for j, need in ((0, "cow"), (1, "water")):
        (lp.tab.fp if n == need else lp.tab.fn)[k, j] += 1
a_, b_ = lp.window(pos), nm.mem.window(pos, 0)
plant = np.zeros((cx2.N, cx2.N), bool)
for wy in range(cx2.N):
    for wx in range(cx2.N):
        x, y = pos[0] + wx - cx2.H, pos[1] + wy - cx2.H
        if 0 <= x < 64 and 0 <= y < 64 and lp.kind[x, y] == K["plant"]:
            plant[wy, wx] = True
eq = all(np.allclose(a_[c][~plant], b_[c][~plant]) for c in range(5))
check(f"a perfect table gives LEARN's layers = NAMED's (plants aside; {int(plant.sum())} plant cells) [{eq}]", bool(eq))


# 3. labels, with a mock body: a bump into water then pokes until drinking; a 3-hit cow; full drink teaches nothing
class Body:
    def __init__(self, pos, inv):
        self.pos, self.facing, self.inventory, self.sleeping = np.array(pos), (0, 1), dict(inv), False


class Env:
    def __init__(self, body, sem):
        self._player, self.sem = body, sem

    def _sem_view(self):
        return self.sem


def mock(arm="learn"):
    p = cx2.LearnPlayer(NET, np.random.default_rng(0), arm)
    p.reset()
    sem = np.full((64, 64), K["grass"], int)
    return p, sem


inv0 = {"health": 9, "food": 5, "drink": 5, "energy": 9}
p, sem = mock()
sem[10, 11] = K["water"]
body = Body((10, 10), inv0)
env = Env(body, sem)
p.prev = {"kind": "move", "cell": (10, 11), "dir": (0, 1), "from": (10, 10), "k": K["water"], "asleep": False}
p.after(env)                                                     # bumped: blocked + a poke bout opens
ok_bump = p.tab.bp[K["water"]] == 1 and p.bout is not None and p.bout["poke"]
p.prev = {"kind": "do", "cell": (10, 11), "dir": (0, 1), "inv": dict(body.inventory), "asleep": False}
body.inventory["drink"] = 6
p.after(env)                                                     # drank: the bout closes, positive for drink
ok_drink = p.tab.fp[K["water"], 1] == 1 and p.tab.fn[K["water"], 0] == 1 and p.bout is None
p, sem = mock()
sem[10, 11] = K["cow"]
body = Body((10, 10), inv0)
env = Env(body, sem)
p.open_bout((10, 11), (0, 1), K["cow"], poke=True)
for hit in range(3):
    p.prev = {"kind": "do", "cell": (10, 11), "dir": (0, 1), "inv": dict(body.inventory), "asleep": False}
    if hit == 2:
        body.inventory["food"] = 9
        sem[10, 11] = K["grass"]
    p.after(env)
ok_cow = p.tab.fp[K["cow"], 0] == 1 and p.tab.fn[K["cow"], 0] == 0 and p.tab.fn[K["cow"], 1] == 1 and p.bout is None
p, sem = mock()
sem[10, 11] = K["water"]
body = Body((10, 10), {"health": 9, "food": 5, "drink": 9, "energy": 9})
env = Env(body, sem)
p.open_bout((10, 11), (0, 1), K["water"], poke=True)
for _ in range(cx2.MAX_DOS):
    p.prev = {"kind": "do", "cell": (10, 11), "dir": (0, 1), "inv": dict(body.inventory), "asleep": False}
    p.after(env)
ok_full = p.tab.fp[K["water"], 1] == 0 and p.tab.fn[K["water"], 1] == 0 and p.tab.fn[K["water"], 0] == 1
p, sem = mock("learn_np")
env = Env(Body((10, 10), inv0), sem)
p.prev = {"kind": "move", "cell": (10, 11), "dir": (0, 1), "from": (10, 10), "k": K["tree"], "asleep": False}
p.after(env)
ok_np = p.tab.bp[K["tree"]] == 1 and p.bout is None
p, sem = mock()
body = Body((10, 10), inv0)
body.pos = np.array((10, 11))
env = Env(body, sem)
p.prev = {"kind": "move", "cell": (10, 11), "dir": (0, 1), "from": (10, 10), "k": K["grass"], "asleep": True}
p.after(env)
ok_sleep = p.tab.bn.sum() == 0 and p.tab.bp.sum() == 0
check(f"labels: bump into water [{ok_bump}], poke until drinking [{ok_drink}], a 3-hit cow is one bout, one positive "
      f"[{ok_cow}], full drink teaches nothing about drink [{ok_full}], LEARN-NP does not poke [{ok_np}], moves while "
      f"asleep teach nothing [{ok_sleep}]", ok_bump and ok_drink and ok_cow and ok_full and ok_np and ok_sleep)


# 4. a life: the tables reset at each life; the same seed twice gives the same life; BLIND's learned layers are 0
def run(arm, seed, perm=None, steps=None):
    env = crafter.Env(seed=seed)
    pl = cx2.LearnPlayer(NET if arm != "random5p" else None, np.random.default_rng(seed), arm, perm=perm)
    acts = []
    orig = pl.act

    def act(e, i):
        a = orig(e, i)
        acts.append(a)
        return a
    pl.act = act
    rec = P.life(env, pl)
    rec.update(pl.extra())
    return rec, acts, pl


import json
import subprocess
import sys


def fresh(arm, seed, perm_seed=None):
    """One life in a FRESH process (Crafter keeps its creatures in Python sets whose order follows memory addresses,
    so only a fresh process repeats a seed exactly)."""
    out = subprocess.run([sys.executable, "cx2_one.py", arm, str(seed), str(perm_seed).lower() if perm_seed is None else str(perm_seed)],
                         capture_output=True, text=True)
    if not out.stdout.strip():
        print(out.stderr[-2000:])
    return json.loads(out.stdout.strip().splitlines()[-1])


r1, r2 = fresh("learn", 3), fresh("learn", 3)
r1b, a1b, pl1 = run("learn", 3)
pl1.reset()
reset_ok = not (pl1.tab.bp.any() or pl1.tab.fp.any() or pl1.tab.fn.any())
rb, ab, plb = run("blind", 4)
wb = plb.window(tuple(int(v) for v in plb.visited.pop()))
blind_ok = not wb[cx2.CH_FOOD].any() and wb[cx2.CH_WALL].sum() == np.sum(wb[cx2.CH_WALL] == 1.0)
check(f"the same seed in two fresh processes, the same life [{r1 == r2}] ({r1['steps']} steps, {r1['bouts']} bouts); "
      f"tables empty after reset [{reset_ok}]; BLIND shows no food and only edge walls [{blind_ok}]",
      r1 == r2 and reset_ok and blind_ok)

# 5. no hidden kinds: relabelling every kind id (a fixed permutation) leaves the lives unchanged (fresh processes)
ok = True
for arm, seed in (("learn", 5), ("random5p", 6), ("learn_np", 8)):
    ra, rp = fresh(arm, seed), fresh(arm, seed, perm_seed=7)
    ok &= ra["acts"] == rp["acts"] and ra["steps"] == rp["steps"] and ra["achievements"] == rp["achievements"]         and ra["first_drink"] == rp["first_drink"] and ra["first_food"] == rp["first_food"]
check(f"relabelled kinds change nothing (LEARN, RANDOM-5P, LEARN-NP: the same actions, lives and measures) [{ok}]",
      bool(ok))

# 6. every arm runs a whole life
ok, lens = True, {}
for arm in cx2.ARMS:
    r, _, _ = run(arm, 11)
    lens[arm] = (r["steps"], r["bouts"], r["first_drink"])
    ok &= r["steps"] > 0
check(f"every arm lives a whole life (steps, bouts, first drink ranked): {lens}", bool(ok))
print("All: PASS" if not fails else f"FAILED: {fails}")
