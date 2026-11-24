"""CX1 checks before the run (questions.md). All must pass.

  python checks_cx1.py
"""
import hashlib
import json
import tempfile
from pathlib import Path

import numpy as np
import crafter
from crafter import objects

import bridge as BR
import play
import analyse_cx1 as AN

HERE = Path(__file__).parent
W3P_KEPT = Path(r"D:\acl\experiments\BX1_brain_exam\mbb_seed1.npz")
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name + (f"  ({detail})" if detail else ""))


# 1. semantic ids
env = crafter.Env(seed=1)
env.reset()
mat = env._world._mat_ids
ok = all(mat[n if n != "none" else None] == i for i, n in enumerate(BR.MAT))
obj = env._sem_view._obj_ids
order = [objects.Player, objects.Cow, objects.Zombie, objects.Skeleton, objects.Arrow, objects.Plant]
ok = ok and all(obj[c] == len(BR.MAT) + i for i, c in enumerate(order)) and [n for n in BR.OBJ] == \
    ["player", "cow", "zombie", "skeleton", "arrow", "plant"]
check("1 semantic ids match Crafter", ok)

# 2. window orientation: a fake world with one tree 2 east and 1 north of the player
sem = np.full((64, 64), BR.MAT.index("grass"))
sem[32 + 2, 30 - 1] = BR.MAT.index("tree")
sem[32 - 3, 30] = BR.MAT.index("water")
mem = BR.Memory()
mem.write(sem, (32, 30), 0, set())
m = mem.window((32, 30), 0)
ok = (m[BR.CH_WALL, BR.H - 1, BR.H + 2] == 1 and m[BR.CH_WALL].sum() == 0 + 1 + 0
      and m[BR.CH_FOOD, BR.H, BR.H - 3] == 1 and m[BR.CH_UNSEEN, BR.H, BR.H + 5] == 1
      and m[BR.CH_UNSEEN, BR.H, BR.H + 4] == 0 and m[BR.CH_UNSEEN, BR.H + 4, BR.H] == 1
      and m[BR.CH_SHELTER, BR.H, BR.H] == 1)
check("2 window orientation, view 9 x 7, wall/food/unseen/shelter", bool(ok))

# 3. the hand: food to the east -> move_right, then do once facing east
class Fixed:
    def __init__(self, a):
        self.a = a
    def plan(self, m, lev):
        return None
    def head(self, fw, rows):
        z = np.full((1, 5), -50.0)
        z[0, self.a] = 50.0
        return z, None

env = crafter.Env(seed=3)
env.reset()
p = BR.BrainPlayer(Fixed(2), np.random.default_rng(0))
p.reset()
info = play.first_info(env)
x, y = (int(v) for v in info["player_pos"])
info["semantic"] = info["semantic"].copy()
info["semantic"][x + 1, y] = BR.MAT.index("water")
p.ripe = set()
a1 = p.act(env, info)
p.facing = (1, 0)
a2 = p.act(env, info)
p.facing = (0, 1)
p.net = Fixed(4)
a3 = p.act(env, info)
check("3 hand: into food = face then do; stay = sleep",
      BR.ACTIONS[a1] == "move_right" and BR.ACTIONS[a2] == "do" and BR.ACTIONS[a3] == "sleep",
      f"{BR.ACTIONS[a1]}, {BR.ACTIONS[a2]}, {BR.ACTIONS[a3]}")

# 4. the score formula
recs = [{"achievements": {"collect_wood": 1}}, {"achievements": {}}]
s, _ = play.score(recs)
want = float(np.exp((np.log(51.0) + 21 * np.log(1.0)) / 22) - 1)
s0, _ = play.score([{"achievements": {}}])
s100, _ = play.score([{"achievements": {a: 1 for a in crafter.constants.achievements}}])
g = AN.got(recs)
check("4 score formula (play and analysis agree)", abs(s - want) < 1e-9 and s0 == 0 and abs(s100 - 100) < 1e-9
      and abs(AN.score_of(g) - want) < 1e-9 and sorted(AN.ACH) == sorted(crafter.constants.achievements),
      f"{s:.4f} vs {want:.4f}")

# 5. determinism: the same seed gives the same life, both arms
net = BR.load(str(HERE / "mbb_seed1.npz"))
same = True
for kind in ("brain", "random"):
    lives = []
    for _ in range(2):
        env = crafter.Env(seed=7)
        rng = np.random.default_rng(7)
        pl = BR.BrainPlayer(net, rng) if kind == "brain" else BR.RandomPlayer(rng)
        lives.append(json.dumps(play.life(env, pl), sort_keys=True))
    same = same and lives[0] == lives[1]
check("5 determinism (seed 7, both arms)", same)

# 6. the brain is W3p's MBb, unchanged
h = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
d = np.load(HERE / "mbb_seed1.npz")
n = sum(d[k].size for k in d.files)
check("6 MBb unchanged (hash equals the kept copy; 236 numbers)", h(HERE / "mbb_seed1.npz") == h(W3P_KEPT) and n == 236,
      f"{n} numbers, {h(W3P_KEPT)[:12]}")

# 7. RANDOM-5 uses the same hand: with food to the east and facing east, an east draw gives "do"
env = crafter.Env(seed=3)
env.reset()
r5 = BR.RandomHandPlayer(np.random.default_rng(0))
r5.reset()
r5.choose = lambda m, info: 2
info = play.first_info(env)
x, y = (int(v) for v in info["player_pos"])
info["semantic"] = info["semantic"].copy()
info["semantic"][x + 1, y] = BR.MAT.index("water")
r5.facing = (1, 0)
b1 = r5.act(env, info)
r5.choose = lambda m, info: 4
b2 = r5.act(env, info)
check("7 RANDOM-5 shares the hand", BR.ACTIONS[b1] == "do" and BR.ACTIONS[b2] == "sleep")

# 8. SATED: water hidden (and a wall) while drink = 9, shown while drink < 9; cows follow food
sem = np.full((64, 64), BR.MAT.index("grass"))
sem[33, 30] = BR.MAT.index("water")
sem[31, 30] = len(BR.MAT) + BR.OBJ.index("cow")
mem = BR.Memory()
mem.write(sem, (32, 30), 0, set())
full = mem.window((32, 30), 0, {"drink": 9, "food": 5})
thirsty = mem.window((32, 30), 0, {"drink": 8, "food": 9})
plain = mem.window((32, 30), 0)
ok = (full[BR.CH_FOOD, BR.H, BR.H + 1] == 0 and full[BR.CH_WALL, BR.H, BR.H + 1] == 1
      and full[BR.CH_FOOD, BR.H, BR.H - 1] == 1
      and thirsty[BR.CH_FOOD, BR.H, BR.H + 1] == 1 and thirsty[BR.CH_WALL, BR.H, BR.H - 1] == 1
      and plain[BR.CH_FOOD, BR.H, BR.H + 1] == 1 and plain[BR.CH_FOOD, BR.H, BR.H - 1] == 1)
check("8 SATED gating (and the primary bridge unchanged)", bool(ok))

print("All: PASS" if all(results) else "All: FAIL")
