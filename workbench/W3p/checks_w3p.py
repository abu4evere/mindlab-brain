"""W3p checks, before any data. Prints All: PASS or the failures."""
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import w3p  # noqa: E402  (the numerical settings before numpy loads)
import numpy as np  # noqa: E402
from w3p import w3k, w3m, w3n, W, B  # noqa: E402
import brain_mv as M  # noqa: E402
import brain_mv_ref as REF  # noqa: E402
from w3k import w3d, R3  # noqa: E402

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
    w3k.OUT = w3m.OUT = w3n.OUT = w3p.OUT = tmp


def short(arm, seed, fade=1500, steps=3000):
    w3k.RUNS[arm] = {"steps": steps, "fade": fade}
    (w3p.configure if arm in w3p.ARMS else w3n.configure)(arm, seed)
    if arm not in w3p.ARMS:
        B.DriveVIN = w3p.DRIVE
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

# 1. the arm: W3n's HR body and schedule; the recipe builds a MoveVIN
w3p.configure("MV", 3)
cw = w3d._ns["copy_weight"]
net = B.DriveVIN(3, fixed_map=False)
check("MV: W3n's HR body, 4.0M steps with a 2.4M fade, sleep and hunger reflexes; the recipe builds a MoveVIN "
      f"({type(net).__name__}, {sum(v.size for v in net.p.values())} numbers)",
      w3k.RUNS["MV"] == {"steps": 4_000_000, "fade": 2_400_000} and cw(0) == 0.5 and cw(2_400_000) == 0.0
      and w3m.PART == {"reflex": "walk", "urge": False} and w3n.BODY == {"cheap": False, "hunger": True}
      and isinstance(net, M.MoveVIN) and sum(v.size for v in net.p.values()) == 236)
B.DriveVIN = w3p.DRIVE

# 2. the gradients are exact (finite differences)
out = subprocess.run([sys.executable, str(HERE / "gradcheck_mv.py")], capture_output=True, text=True).stdout
check(f"MoveVIN's gradients match finite differences ({out.strip().splitlines()[0] if out.strip() else 'no output'})",
      "All: PASS" in out)

# 3. the fast code equals the reference code, bit for bit (plan, head, backprop)
rng = np.random.default_rng(9)
ok = True
for trial in range(3):
    a, b = M.MoveVIN(trial), REF.MoveVIN(trial)
    for k in a.p:
        a.p[k] = a.p[k] + rng.normal(0, 0.3, a.p[k].shape)
        b.p[k] = a.p[k].copy()
    T = 32
    maps = (rng.random((T, M.C, M.N, M.N)) < 0.3).astype(float)
    lev = rng.random((T, 3))
    rows = np.arange(T) * M.N * M.N + rng.integers(0, M.N * M.N, T)
    fa, fb = a.plan(maps, lev), b.plan(maps, lev)
    za, va = a.head(fa, rows)
    zb, vb = b.head(fb, rows)
    dl, dv = rng.normal(size=(T, 5)), rng.normal(size=T)
    ga, gb = a.backprop(fa, rows, dl, dv), b.backprop(fb, rows, dl, dv)
    ok &= np.array_equal(za, zb) and np.array_equal(va, vb) and all(np.array_equal(ga[k], gb[k]) for k in ga)
check("the fast MoveVIN equals the reference, bit for bit", bool(ok))

# 4. capacity: hand-set ideal weights solve the R2 detours (the design can do it)
out = subprocess.run([sys.executable, str(HERE / "capacity_mv.py")], capture_output=True, text=True).stdout
check(f"capacity: hand-set weights solve the detours ({out.strip().splitlines()[-1] if out.strip() else 'no output'})",
      "'success': 1.0, 'cases': 36" in out)

# 5. MV trains, differs from HR, split = unsplit, repeatable
w3k.CS_WINDOW, w3k.CS_START = 400, 200
fresh()
short("MV", 6, fade=1500, steps=6000)
m1, _, _ = w3m.train_net_w3m("MV", 6, 6000, R, hours=1.0)
_, q, _ = w3m.train_net_w3m("MV", 6, 6000, R, hours=1.0, pause_after=3500)
m2, _, _ = w3m.train_net_w3m("MV", 6, 6000, R, hours=1.0, state=q)
m3, _, _ = w3m.train_net_w3m("MV", 6, 6000, R, hours=1.0)
init = M.MoveVIN(6)
B.DriveVIN = w3p.DRIVE
short("HR", 6, fade=1500, steps=6000)
h1, _, _ = w3m.train_net_w3m("HR", 6, 6000, R, hours=1.0)
check(f"MV trains a MoveVIN [{type(m1).__name__}], it moves from its start [{not same(m1, init)}], split = unsplit "
      f"[{same(m1, m2)}], repeatable [{same(m1, m3)}]; HR still trains a DriveVIN [{type(h1).__name__}]",
      isinstance(m1, M.MoveVIN) and not same(m1, init) and same(m1, m2) and same(m1, m3)
      and type(h1).__name__ == "DriveVIN")

# 6. a whole staged MV run saves its copies and runs every test; nothing written into W3n's folder
fresh()
short("MV", 7, fade=1500, steps=12000)
w3k.CFG["cy_step"] = 2200
seeds0, fresh0 = W.TEST_SEEDS, w3k.w3i.FRESH_SEEDS
W.TEST_SEEDS, w3k.w3i.FRESH_SEEDS = range(900001, 900003), range(910001, 910003)
w3k.right_machine = lambda: True
w3p.OUT = tmp
w3p.run("MV", 7, 1.0)
names = {p.name for p in tmp.iterdir()}
need = {"MV_7.npz", "MV_CS_7.npz", "MV_CY_7.npz", "test_MV_7.json", "test_MVS_7.json", "test_MVY_7.json",
        "test_MVS-off_7.json", "test_MVS-bare_7.json", "test_fresh_MVS_7.json"}
loaded = w3k.load_npz(tmp / "MV_CS_7.npz", 7)
new3n = {p.name for p in W3N_OUT.iterdir()} - n3n
check(f"a staged MV run saves its copies and runs every test (missing {sorted(need - names)}); the kept copy loads as "
      f"{type(loaded).__name__}; nothing new in W3n's folder from W3p ({sorted(x for x in new3n if 'MV' in x)})",
      need <= names and isinstance(loaded, M.MoveVIN) and not any("MV" in x for x in new3n))
W.TEST_SEEDS, w3k.w3i.FRESH_SEEDS = seeds0, fresh0
B.DriveVIN = w3p.DRIVE
shutil.rmtree(tmp)
print("All: PASS" if not fails else f"FAILED: {fails}")
