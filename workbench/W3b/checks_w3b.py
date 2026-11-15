"""W3b checks, before any data (questions.md, Validity). Prints All: PASS or the failures."""
import ast
import json
import pickle
import sys
from collections import deque
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import w3b  # noqa: E402
import brains3 as B  # noqa: E402
import world3 as W  # noqa: E402
import run_w3 as R3  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


R = R3.regrowth()
W3OUT = w3b.W3 / "output"

# 1. the base brain and loop unchanged: D3 with no parts reproduces W3's log line at life 20 (seed 1), bit for bit
line = [ln for ln in (W3OUT / "D3_1.log").read_text().splitlines() if " lives 20 " in ln][0]
w3_total = int(line.split("step ")[1].split()[0])
w3_norms = ast.literal_eval(line.split("norms ")[1].rsplit(" ", 1)[0])
net, st, _ = w3b.train_net("D3", 1, 10_000_000, R, hours=9, stop_lives=20)
check(f"D3 (no parts) reproduces W3's training at life 20 (step {st['total']} = {w3_total}; norms equal)",
      st["total"] == w3_total and all(abs(net.row_norms()[k] - w3_norms[k]) < 1e-12 for k in w3_norms))

# 2. the test is W3's: testing W3's D3 seed 1 through w3b.test gives W3's test file
mine = w3b.test("D3", 1)
theirs = json.loads((W3OUT / "test_D3_1.json").read_text())
check("w3b.test('D3', 1) equals W3's test_D3_1.json", json.dumps(mine) == json.dumps(theirs))
(w3b.OUT / "test_D3_1.json").unlink()

# 3. a split run equals an unsplit run (YFR, seed 3, 6,000 steps; the split at the first life boundary after 3,000)
net_u, st_u, fin_u = w3b.train_net("YFR", 3, 6_000, R, hours=9)
net_1, st_1, fin_1 = w3b.train_net("YFR", 3, 6_000, R, hours=9, pause_after=3_000)   # pauses at the first life boundary after 3,000
st_1 = pickle.loads(pickle.dumps(st_1))                                     # through the checkpoint format
net_2, st_2, fin_2 = w3b.train_net("YFR", 3, 6_000, R, hours=9, state=st_1)
same = all(np.array_equal(net_u.p[k], net_2.p[k]) for k in net_u.p) and st_u["total"] == st_2["total"] \
    and st_u["updates"] == st_2["updates"] and st_u["lives"] == st_2["lives"]
check(f"split run = unsplit run (YFR seed 3; updates {st_u['updates']})", same and fin_u and fin_2)

# 4. Y's trigger: fires on a hand-built meal when hungry, not on a plain step, not in the warm-up
stats = w3b.Stats()
for _ in range(200):
    for c in w3b.NEEDS:
        stats.add(c, 0.0)
w0, which = w3b.event(stats, (0.5, 0.1), w3b.relief((0.5, 0.1), (0.3, 0.1)), 5_000)
check(f"Y fires on a meal when hungry (weight {w0:.2f}, need {which})", which == "s" and w0 == w3b.W_MAX)
check("Y does not fire on a plain step", w3b.event(stats, (0.5, 0.1), w3b.relief((0.5, 0.1), (0.507, 0.105)), 5_000)[1] is None)
check("Y does not fire when the need is low", w3b.event(stats, (0.1, 0.1), w3b.relief((0.1, 0.1), (0.0, 0.1)), 5_000)[1] is None)
check("Y does not fire in the warm-up", w3b.event(stats, (0.5, 0.1), w3b.relief((0.5, 0.1), (0.3, 0.1)), 500)[1] is None)

# 5. the window stops at the previous event and at 15; the weights decay 0.9 per step back from w0
recs = deque([(None, None, None, i) for i in range(40)], maxlen=w3b.WIN)
r5, w5 = w3b.window(recs, 5, 2.0)
r15, w15 = w3b.window(recs, 30, 2.0)
check("window: 5 since the previous event -> 5 records; 30 since -> 15", len(r5) == 5 and len(r15) == 15)
check("window weights: w0 at the latest step, x0.9 per step back",
      abs(w15[-1] - 2.0) < 1e-12 and abs(w15[0] - 2.0 * 0.9 ** 14) < 1e-12 and r15[-1][3] == 39)

# 6. FR replays only on shelter steps, at most 64 per life; RR's windows cover the life contiguously with weight 1.0
orig = w3b.imitate
calls = []
w3b.imitate = lambda net, recs, weights: calls.append((len(recs), float(np.mean(weights)))) or orig(net, recs, weights)
net_f, st_f, _ = w3b.train_net("FR", 4, 20_000, R, hours=9)
replays_per_life = [x["replays"] for x in st_f["lives_log"]]
check(f"FR: at most 64 replays per life (max {max(replays_per_life)}); replays {st_f['updates']['replay']}",
      max(replays_per_life) <= w3b.REPLAY_CAP)
calls.clear()
net_r, st_r, _ = w3b.train_net("RR", 4, 20_000, R, hours=9)
pushes_expected = sum(x["t"] // w3b.WIN for x in st_r["lives_log"])
check(f"RR: windows pushed contiguously (one per 15 steps: {pushes_expected} expected) and all weights 1.0; replays {st_r['updates']['replay']}",
      len(st_r["store"]) == min(w3b.STORE_CAP, pushes_expected) and all(w == 1.0 for _, ws in st_r["store"] for w in ws)
      and all(abs(mw - 1.0) < 1e-12 for n, mw in calls))
w3b.imitate = orig


# 6b. the replay condition in the code is 'on the shelter cell, under the cap'
wsh = W.World(W.make_land(W.train_seed(4, 1)), R)
wsh.pos = wsh.shelter
store_1 = [([(wsh.obs_map(), (0.0, 0.0, 0.0), wsh.pos, 4)], [1.0])]
woff = W.World(W.make_land(W.train_seed(4, 1)), R)
check("replay only on the shelter cell, under the cap, with a non-empty store",
      w3b.should_replay(wsh, 0, store_1) and not w3b.should_replay(wsh, w3b.REPLAY_CAP, store_1)
      and not w3b.should_replay(wsh, 0, []) and (woff.pos == woff.shelter or not w3b.should_replay(woff, 0, store_1)))

# 7. F walks to the stored place only when the need is high (s >= 0.2, i.e. E < 120), else the learned brain acts
land = W.make_land(W.TEST_SEEDS[0])
w = W.World(land, R)
netD = R3.load("D3", 1)
pol = w3b.FPolicy(netD, np.random.default_rng(0))
a_exp, x_p, y_p = w3b.open_neighbours(w)[0]
pol.place["s"] = (x_p, y_p)
w.E = 100.0
a_f = pol.act(w)
w.E = 140.0
rng_a, rng_b = np.random.default_rng(7), np.random.default_rng(7)
pol.rng = rng_a
a_net = pol.act(w)
a_ref = netD.act(w.obs_map(), R3.levels(w, "D3"), w.pos, rng_b)[0]
check(f"F walks when hungry (E 100 -> action {a_f}, a move toward the place) and lets the brain act when not (E 140)",
      a_f == a_exp and a_net == a_ref and pol.walks == 1)

# 8. step 0's walks on a hand-built value map; test lands identical across calls; same seed twice is the same
v = np.zeros((B.N, B.N))
w = W.World(W.make_land(W.TEST_SEEDS[1]), R)
nb = w3b.open_neighbours(w)
a0, x0, y0 = nb[0]
v[y0, x0] = 1.0
check("greedy walk picks the highest-value open neighbour", w3b.greedy_action(v, w) == a0)
check("greedy walk stays on a flat map", w3b.greedy_action(np.zeros((B.N, B.N)), w) == 4)
check("look-ahead walk picks the neighbour that sees the best cell", w3b.lookahead_action(v, w) == a0)
l1, l2 = W.make_land(W.TEST_SEEDS[5]), W.make_land(W.TEST_SEEDS[5])
check("test lands identical across calls", np.array_equal(l1["walls"], l2["walls"]) and l1["patches"] == l2["patches"]
      and l1["sched"] == l2["sched"] and l1["start"] == l2["start"])
import time
t_0 = time.time()
n1, s1, _ = w3b.train_net("Y", 2, 2_000, R, hours=9)
speed_ms = (time.time() - t_0) / 2_000 * 1000
n2, s2, _ = w3b.train_net("Y", 2, 2_000, R, hours=9)
check(f"same seed twice is the same (Y seed 2, 2,000 steps; Y updates {s1['updates']['y']}; {speed_ms:.1f} ms/step at Idle)",
      all(np.array_equal(n1.p[k], n2.p[k]) for k in n1.p) and s1["updates"] == s2["updates"])

# 9. weights unchanged by testing is asserted inside w3b.test (check 2 passed through it)
check("weights-unchanged assertion present in test", "weights changed in testing" in Path(w3b.__file__).read_text())
print("All: PASS" if not fails else f"FAILED: {fails}")
