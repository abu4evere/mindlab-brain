"""W3l checks, before any data. Prints All: PASS or the failures. Imports w3l first (which imports w3k), so the
numerical settings are in place before numpy loads."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import w3l  # noqa: E402
import os  # noqa: E402
import shutil  # noqa: E402
from collections import deque  # noqa: E402

import numpy as np  # noqa: E402
from w3k import w3d, W, R3  # noqa: E402

w3k = w3l.w3k
fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


R = R3.regrowth()
tmp = HERE / "tmp_checks"


def fresh():
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()
    w3k.OUT = tmp


def short(run, fade, steps, seed):
    w3k.RUNS[run] = {"steps": steps, "fade": fade}
    w3l.configure(run, seed)
    w3k.w3b.OUT = w3k.w3i.OUT = tmp


# 0. the numerical settings (W3k's), set before numpy loaded
from numpy._core._multiarray_umath import __cpu_targets_info__  # noqa: E402
in_use = sorted({v["current"] for fn in __cpu_targets_info__.values() for v in fn.values()})
check(f"determinism settings in place before numpy loads (verified machine: {w3k.GOOD_MACHINE}; paths {in_use})",
      os.environ.get("OPENBLAS_CORETYPE") == ("Zen" if w3k.GOOD_MACHINE else None)
      and os.environ.get("NPY_DISABLE_CPU_FEATURES") == "AVX512_SPR AVX512_ICL X86_V4"
      and not any(t.startswith(("X86_V4", "AVX512")) for t in in_use) and os.environ.get("OPENBLAS_NUM_THREADS") == "1")

# 1. the schedules: C3 fades over 3.6M of 5.2M (W3k's), C5 over 4.8M of 6.4M; CY's steps drawn with the new seed
ok = True
for run, fade, steps in (("C3", 3_600_000, 5_200_000), ("C5", 4_800_000, 6_400_000)):
    w3l.configure(run, 3)
    cw, pp = w3d._ns["copy_weight"], w3d._ns["parent_present"]
    ok &= w3k.RUNS[run] == {"steps": steps, "fade": fade}
    ok &= cw(0) == 0.5 and abs(cw(fade // 2) - 0.25) < 1e-12 and cw(fade) == 0.0 and pp(fade - 1) and not pp(fade)
    ok &= w3k.CFG["cy_step"] == int(np.random.default_rng(20261191 + 3).integers(fade + 200_000, steps))
    ok &= all(fade + 200_000 <= w3k.cy_step_for(s, run) < steps for s in range(1, 17))
ok &= w3k.snaps("C3") == (3_600_000, 4_000_000, 4_400_000, 4_800_000)
ok &= w3k.snaps("C5") == (4_800_000, 5_200_000, 5_600_000, 6_000_000)
check("schedules: C3 3.6M of 5.2M; C5 4.8M of 6.4M; snapshots; CY's steps drawn in advance (seed 20261191 + run seed)",
      bool(ok))

# 2. the hooks do not change training (short C3: fade 1,500, steps 3,000), with CY now drawn
w3k.CS_WINDOW, w3k.CS_START = 400, 200
fresh()
short("C3", 1500, 3000, 4)
w3k.CFG["cy_step"] = 2200
net_h, st_h, _ = w3k.train_net_w3k("C3", 4, 3000, R, hours=1.0)
w3k.configure("C3", 4)
w3d.CFG.update(child=1500)
net_p, _, _ = w3d.train_net_parent("C3", 4, 3000, R, hours=1.0)
check("the hooks do not change training (C3 with hooks equals W3d's training without them)",
      all(np.array_equal(net_h.p[k], net_p.p[k]) for k in net_h.p))

ends, best, cs_step, total = deque(), -1.0, None, 0
for rec in st_h["lives_log"]:
    total += rec["t"]
    ends.append((total, rec["t"]))
    while ends and ends[0][0] <= total - 400:
        ends.popleft()
    if total >= 1500 + 200:
        mean = sum(x[1] for x in ends) / len(ends)
        if mean > best:
            best, cs_step = mean, total
check(f"CS keeps the copy its rule names (recomputed {cs_step}; kept {st_h.get('cs_step')})",
      cs_step is not None and st_h.get("cs_step") == cs_step)
boundaries = np.cumsum([r["t"] for r in st_h["lives_log"]])
first_after = int(boundaries[np.argmax(boundaries >= 2200)])
check(f"CY is the brain at the first life boundary after its step (2200 -> {st_h.get('cy_at')})",
      st_h.get("cy_at") == first_after)

# 3. a run other than R now saves both copies (the one change from W3k), and its end equals the unstaged run
fresh()
short("C3", 1500, 3000, 4)
w3k.CFG["cy_step"] = 2200
w3l.train_staged("C3", 4, hours=1.0, snapshot_at=(1500,))
names = {p.name for p in tmp.iterdir()}
check("run C3 gives its end, CS and CY copies and the fade snapshot (C3_4, C3_CS_4, C3_CY_4, C3_4_1k)",
      {"C3_4.npz", "C3_CS_4.npz", "C3_CY_4.npz", "C3_4_1k.npz", "C3_4_meta.json"} <= names)
end = dict(np.load(tmp / "C3_4.npz"))
cs = dict(np.load(tmp / "C3_CS_4.npz"))
check("the end equals the unstaged run; the CS copy equals the copy kept in the unstaged run",
      all(np.array_equal(end[k], net_h.p[k]) for k in end) and all(np.array_equal(cs[k], st_h["cs_p"][k]) for k in cs))

# 4. split = unsplit (with the copies' state); the same seed twice is the same
fresh()
short("C5", 1500, 3000, 6)
a1, s1, _ = w3k.train_net_w3k("C5", 6, 3000, R, hours=1.0)
_, qa, _ = w3k.train_net_w3k("C5", 6, 3000, R, hours=1.0, pause_after=1900)
b1, sb, _ = w3k.train_net_w3k("C5", 6, 3000, R, hours=1.0, state=qa)
a2, _, _ = w3k.train_net_w3k("C5", 6, 3000, R, hours=1.0)
same = all(np.array_equal(a1.p[k], b1.p[k]) and np.array_equal(a1.p[k], a2.p[k]) for k in a1.p)
same &= s1.get("cs_step") == sb.get("cs_step") and s1.get("cy_at") == sb.get("cy_at")
if s1.get("cs_p") is not None:
    same &= all(np.array_equal(s1["cs_p"][k], sb["cs_p"][k]) for k in s1["cs_p"])
check("C5: a split run equals an unsplit run (with the copies' state); the same seed twice is the same", bool(same))

# 5. outputs go to W3l's folder; an unverified processor hands the job back
w3k.OUT = w3l.OUT
check("outputs go to W3l/output", w3l.OUT == HERE / "output" and w3k.OUT == HERE / "output")
w3k.OUT = tmp
ok_flag = w3k.right_machine() == w3k.GOOD_MACHINE and (tmp / "wrong_machine.flag").exists() != w3k.GOOD_MACHINE
check(f"an unverified processor hands the job back with a flag (this machine verified: {w3k.GOOD_MACHINE})", ok_flag)
shutil.rmtree(tmp)
print("All: PASS" if not fails else f"FAILED: {fails}")
