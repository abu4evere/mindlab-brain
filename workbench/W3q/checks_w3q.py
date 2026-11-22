"""W3q checks, before any data. Prints All: PASS or the failures."""
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import w3q  # noqa: E402  (the numerical settings before numpy is used)
import numpy as np  # noqa: E402
from w3q import w3k, w3m, w3n, W  # noqa: E402
from w3k import R3  # noqa: E402
import probe_w3q as PQ  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


R = R3.regrowth()
tmp = HERE / "tmp_checks"
W3N_OUT = HERE.parent / "W3n" / "output"
n3n = {p.name for p in W3N_OUT.iterdir()}


def fresh():
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()
    w3k.OUT = w3m.OUT = w3n.OUT = w3q.OUT = tmp


def short(arm, seed, fade=1500, steps=3000):
    w3k.RUNS[arm] = {"steps": steps, "fade": fade}
    (w3q.configure if arm in w3q.ARMS else w3n.configure)(arm, seed)
    w3q.CFG.update(arm=arm, seed=seed)
    w3k.w3b.OUT = w3k.w3i.OUT = tmp


def same(a, b):
    return all(np.array_equal(a.p[k], b.p[k]) for k in a.p)


# 0. the numerical settings (W3k's)
import os  # noqa: E402
from numpy._core._multiarray_umath import __cpu_targets_info__  # noqa: E402
in_use = sorted({v["current"] for fn in __cpu_targets_info__.values() for v in fn.values()})
check(f"determinism settings in place (paths {in_use})",
      os.environ.get("OPENBLAS_CORETYPE") == ("Zen" if w3k.GOOD_MACHINE else None)
      and not any(t.startswith(("X86_V4", "AVX512")) for t in in_use))

# 1. the arms: HR's body and schedule; the parent's copy weight by arm
res = {}
for arm in ("BF", "BP", "RP", "HR"):
    (w3q.configure if arm in w3q.ARMS else w3n.configure)(arm, 3)
    if arm == "HR":
        w3m._ns["copy_weight"], w3m._ns["parent_present"] = w3q._copy_weight0, w3q._present0
    cw, pp = w3m._ns["copy_weight"], w3m._ns["parent_present"]
    res[arm] = (cw(0), round(cw(1_200_000), 6), cw(2_400_000), pp(2_400_000), pp(3_999_999))
ok1 = (all(w3k.RUNS[a] == {"steps": 4_000_000, "fade": 2_400_000} for a in w3q.ARMS)
       and res["BF"] == (0.5, 0.25, 0.0, False, False) and res["HR"] == res["BF"]
       and res["BP"] == (0.5, 0.25, 0.05, True, True) and res["RP"] == res["BP"]
       and w3m.PART == {"reflex": "walk", "urge": False} and w3n.BODY == {"cheap": False, "hunger": True})
check(f"arms: 4.0M steps, fade 2.4M, HR's body; copy weight (0, 1.2M, 2.4M; present at 2.4M, at 4.0M) {res}", ok1)

# 2. corners, on a hand-made map
wall = np.zeros((7, 7), bool)
wall[0, :] = wall[-1, :] = wall[:, 0] = wall[:, -1] = True
wall[3, 3] = True
seen = np.ones_like(wall)
c = w3q.corners(wall, seen)
expect = {(1, 1), (5, 1), (1, 5), (5, 5)}                     # the four inner corners of the border
got = {(int(x), int(y)) for y, x in zip(*np.nonzero(c))}
seen2 = seen.copy()
seen2[1, 1] = False
got2 = {(int(x), int(y)) for y, x in zip(*np.nonzero(w3q.corners(wall, seen2)))}
check(f"corners found exactly on a hand-made map ({sorted(got)}); an unseen cell is never a corner ({sorted(got2)})",
      got == expect and got2 == expect - {(1, 1)})

# 3. the lying parent: heads for a seen corner when it is the nearest 'food'; ignores unseen corners; else right
st = json.loads((HERE / "output" / "probe_states.json").read_text())["states"] if (HERE / "output" / "probe_states.json").exists() else PQ.states()
okl, oku, okr, n = True, True, True, 0
for s in st[:30]:
    w = PQ.known_world(s["land"], R)
    w.pos, (w.E, w.F) = tuple(s["start"]), (60.0, 0.0)
    lying, right = w3q.LyingScript(), w3q.RIGHT_SCRIPT()
    a_l, a_r = lying.act(W.MapView(w)), right.act(W.MapView(w))
    okl &= a_l in s["lie_moves"]
    okr &= a_r in s["truth_moves"]
    w.m_seen[:] = False                                       # nothing seen: no corner is believed
    w.m_seen[w.m_food] = True
    w.m_seen[w.pos[1], w.pos[0]] = True
    oku &= w3q.LyingScript().act(W.MapView(w)) == w3q.RIGHT_SCRIPT().act(W.MapView(w))
    n += 1
fed = PQ.known_world(st[0]["land"], R)
fed.pos, (fed.E, fed.F) = tuple(st[0]["start"]), (180.0, 0.0)
okf = w3q.LyingScript().act(W.MapView(fed)) == w3q.RIGHT_SCRIPT().act(W.MapView(fed))
check(f"the lying parent ({n} conflict states): heads for the corner [{okl}] where the right parent heads for food "
      f"[{okr}]; with the corners unseen it acts as the right parent [{oku}]; when not hungry, the same [{okf}]",
      okl and okr and oku and okf)

# 4. with the right parent and its fade, W3q's training equals the unwrapped training bit for bit
w3k.CS_WINDOW, w3k.CS_START = 400, 200
fresh()
short("HR", 6)
w3m._ns["copy_weight"], w3m._ns["parent_present"] = w3q._copy_weight0, w3q._present0
a1, _, _ = w3m.train_net_w3m("HR", 6, 3000, R, hours=1.0)
a0, _, _ = w3q.TRAIN0("HR", 6, 3000, R, hours=1.0)
check(f"the right parent: W3q's training equals HR's unwrapped training bit for bit [{same(a1, a0)}]", same(a1, a0))

# 5. BF and BP train identically up to the fade; after it BP and RP keep copy lessons, BF none; the dose
fresh()
out = {}
for arm in ("BF", "BP", "RP"):
    short(arm, 6)
    netf, sf, _ = w3m.train_net_w3m(arm, 6, 3000, R, hours=1.0, pause_after=1500)
    copies_fade = sf["updates"].get("copy", 0)
    netx, sx, _ = w3m.train_net_w3m(arm, 6, 3000, R, hours=1.0, state=sf)
    out[arm] = {"fade": netf, "end": netx, "copies_fade": copies_fade, "copies_after": sx["updates"].get("copy", 0) - copies_fade,
                "dose": dict(sx["dose"]), "script_after": W.Script is w3q.RIGHT_SCRIPT}
pre = {}
for arm in ("BF", "BP"):                                      # before the fade the two parents are the same
    short(arm, 6, fade=1500, steps=3000)
    pre[arm], _, _ = w3m.train_net_w3m(arm, 6, 1400, R, hours=1.0)
bfbp = same(pre["BF"], pre["BP"])
after = {a: out[a]["copies_after"] for a in out}
dose = {a: out[a]["dose"] for a in out}
check(f"BF = BP before the fade [{bfbp}], differ after [{not same(out['BF']['end'], out['BP']['end'])}]; copy lessons after "
      f"the fade {after}; dose {dose}; the right Script restored after training [{all(o['script_after'] for o in out.values())}]",
      bfbp and not same(out["BF"]["end"], out["BP"]["end"]) and after["BF"] == 0 and after["BP"] > 0 and after["RP"] > 0
      and dose["BF"]["lies"] > 0 and dose["BP"]["lies"] > dose["BF"]["lies"] and dose["RP"]["acts"] == 0
      and all(o["script_after"] for o in out.values()))

# 6. split = unsplit (the dose travels with the state), repeatable
fresh()
short("BP", 6)
m1, s1, _ = w3m.train_net_w3m("BP", 6, 3000, R, hours=1.0)
_, q, _ = w3m.train_net_w3m("BP", 6, 3000, R, hours=1.0, pause_after=2200)
m2, s2, _ = w3m.train_net_w3m("BP", 6, 3000, R, hours=1.0, state=q)
m3, _, _ = w3m.train_net_w3m("BP", 6, 3000, R, hours=1.0)
check(f"BP: split = unsplit [{same(m1, m2)}] with the same dose [{s1['dose'] == s2['dose']}], repeatable [{same(m1, m3)}]",
      same(m1, m2) and s1["dose"] == s2["dose"] and same(m1, m3))

# 7. the probe: every conflict state satisfies its rule; the probe gives the same answer twice
okp = True
for s in st:
    w = PQ.known_world(s["land"], R)
    lie = w3q.corners(w.walls, np.ones_like(w.walls)) & ~w.m_food
    d_l = PQ.dist_map(w.walls, [(x, y) for y, x in zip(*np.nonzero(lie))])
    d_f = PQ.dist_map(w.walls, [(x, y) for y, x in zip(*np.nonzero(w.m_food))])
    x, y = s["start"]
    okp &= (d_l[y, x] < d_f[y, x] < np.inf and not set(s["lie_moves"]) & set(s["truth_moves"])
            and sorted(PQ.toward(d_l, (x, y))) == s["lie_moves"] and sorted(PQ.toward(d_f, (x, y))) == s["truth_moves"])
p1, p2 = PQ.probe(m1, st[:40], R), PQ.probe(m1, st[:40], R)
check(f"the probe: {len(st)} conflict states each satisfy the rule [{okp}]; the same answer twice [{p1 == p2}]",
      okp and p1 == p2 and len(st) >= 150)

# 8. a whole staged run saves its snapshots and copies, runs every test, writes the dose; nothing into W3n's folder
fresh()
short("BP", 7, fade=1500, steps=12000)
w3k.CFG["cy_step"] = 2200
seeds0, fresh0 = W.TEST_SEEDS, w3k.w3i.FRESH_SEEDS
W.TEST_SEEDS, w3k.w3i.FRESH_SEEDS = range(900001, 900003), range(910001, 910003)
w3k.right_machine = lambda: True
w3q.run("BP", 7, 1.0)
names = {p.name for p in tmp.iterdir()}
need = {"BP_7.npz", "BP_CS_7.npz", "BP_CY_7.npz", "test_BP_7.json", "test_BPS_7.json", "test_BPS-bare_7.json",
        "test_fresh_BPS_7.json", "dose_BP_7.json"}
snaps = sorted(n for n in names if n.startswith("BP_7_") and n.endswith("k.npz"))
new3n = {p.name for p in W3N_OUT.iterdir()} - n3n
check(f"a staged BP run saves its copies, snapshots {snaps} and every test (missing {sorted(need - names)}); "
      f"nothing new in W3n's folder ({sorted(new3n)})", need <= names and len(snaps) >= 1 and not new3n)
W.TEST_SEEDS, w3k.w3i.FRESH_SEEDS = seeds0, fresh0
shutil.rmtree(tmp)
print("All: PASS" if not fails else f"FAILED: {fails}")
