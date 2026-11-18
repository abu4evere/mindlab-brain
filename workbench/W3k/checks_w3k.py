"""W3k checks, before any data. Prints All: PASS or the failures. Imports w3k first, so the numerical settings are in
place before numpy loads."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import w3k  # noqa: E402  (sets the numerical environment, then loads numpy)
import os  # noqa: E402
import shutil  # noqa: E402
from collections import deque  # noqa: E402

import numpy as np  # noqa: E402
from w3k import w3d, B, W, R3  # noqa: E402

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
    w3k.configure(run, seed)
    w3k.w3b.OUT = w3k.w3i.OUT = tmp


# 0. the numerical settings, set before numpy loaded
from numpy._core._multiarray_umath import __cpu_targets_info__  # noqa: E402
in_use = sorted({v["current"] for fn in __cpu_targets_info__.values() for v in fn.values()})
check(f"determinism settings in place before numpy loads (OpenBLAS Haswell; numpy's paths in use {in_use}, none "
      f"AVX-512; 1 thread)",
      os.environ.get("OPENBLAS_CORETYPE") == "Haswell"
      and os.environ.get("NPY_DISABLE_CPU_FEATURES") == "AVX512_SPR AVX512_ICL X86_V4"
      and not any(t.startswith(("X86_V4", "AVX512")) for t in in_use) and os.environ.get("OPENBLAS_NUM_THREADS") == "1")

# 1. the schedules: R and CR fade over 2.4M of 4.0M; C3 over 3.6M of 5.2M; CY's step drawn as stated
ok = True
for run, fade, steps in (("R", 2_400_000, 4_000_000), ("CR", 2_400_000, 4_000_000), ("C3", 3_600_000, 5_200_000)):
    w3k.configure(run, 3)
    cw, pp = w3d._ns["copy_weight"], w3d._ns["parent_present"]
    ok &= w3k.RUNS[run] == {"steps": steps, "fade": fade}
    ok &= cw(0) == 0.5 and abs(cw(fade // 2) - 0.25) < 1e-12 and cw(fade) == 0.0 and pp(fade - 1) and not pp(fade)
ok &= w3k.snaps("C3") == (3_600_000, 4_000_000, 4_400_000, 4_800_000) and w3k.snaps("R")[0] == 2_400_000
cys = [w3k.cy_step_for(s) for s in range(1, 17)]
ok &= all(2_600_000 <= c < 4_000_000 for c in cys) and cys[0] == int(np.random.default_rng(20261181 + 1).integers(2_600_000, 4_000_000))
check(f"schedules: fades 0.5 to 0 (R, CR over 2.4M; C3 over 3.6M of 5.2M); snapshots; CY's step drawn in advance "
      f"(seed 1: {cys[0]})", bool(ok))

# 2. maps pack exactly
w = W.World(W.make_land(1), R)
m = w.obs_map()
pk = w3k._pack(m)
check(f"a stored map is exact ({pk.dtype}, {pk.nbytes} bytes)", np.array_equal(pk.astype(np.float64), m))

# 3. R, CS and CY come from one run, and the hooks never change training (short: fade 1,500, steps 3,000)
w3k.CS_WINDOW, w3k.CS_START = 400, 200
fresh()
short("R", 1500, 3000, 4)
net_h, st_h, _ = w3k.train_net_w3k("R", 4, 3000, R, hours=1.0)
w3k.configure("R", 4)
w3d.CFG.update(child=1500)
net_p, _, _ = w3d.train_net_parent("R", 4, 3000, R, hours=1.0)
check("the hooks do not change training (R with hooks equals W3d's training without them)",
      all(np.array_equal(net_h.p[k], net_p.p[k]) for k in net_h.p))

# CS's rule, recomputed from the run's own lives
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
check(f"CS keeps the copy its rule names (recomputed step {cs_step}; kept {st_h.get('cs_step')})",
      cs_step is not None and st_h.get("cs_step") == cs_step)
cy = w3k.CFG["cy_step"]
boundaries = np.cumsum([r["t"] for r in st_h["lives_log"]])
first_after = int(boundaries[np.argmax(boundaries >= cy)])
check(f"CY is the brain at the first life boundary after its drawn step ({cy} -> {st_h.get('cy_at')})",
      st_h.get("cy_at") == first_after)

fresh()
short("R", 1500, 3000, 4)
w3k.train_staged("R", 4, hours=1.0, snapshot_at=(1500,))
names = {p.name for p in tmp.iterdir()}
check("one run gives R2, CS and CY (R_4, R_CS_4, R_CY_4) and the fade snapshot",
      {"R_4.npz", "R_CS_4.npz", "R_CY_4.npz", "R_4_1k.npz", "R_4_meta.json"} <= names)
r2 = dict(np.load(tmp / "R_4.npz"))
check("R2 equals the unstaged run's end", all(np.array_equal(r2[k], net_h.p[k]) for k in r2))

# 4. CR: stores only second-half-of-fade examples, at most the cap; replays after the fade every 4th step at 0.05
fresh()
short("CR", 1500, 3000, 6)
w3k.PSTORE_CAP = 50
seen_w = []
orig_imitate = w3k.w3b.imitate


def spy(net, recs, weights):
    seen_w.append(weights[0])
    return orig_imitate(net, recs, weights)


w3k.w3b.imitate = spy
net_r, st_r, _ = w3k.train_net_w3k("CR", 6, 3000, R, hours=1.0)
w3k.w3b.imitate = orig_imitate
up = st_r["updates"]
check(f"CR keeps second-half-of-fade examples only (seen {st_r.get('pseen')}, expected 187), at most the cap "
      f"({len(st_r['pstore'])} of 50)", st_r.get("pseen") == 187 and len(st_r["pstore"]) == 50)
check(f"CR replays after the fade every 4th step ({up.get('replay_parent')}, expected 375) at weight 0.05 "
      f"(childhood copies {up.get('copy')}, expected 375)",
      up.get("replay_parent") == 375 and up.get("copy") == 375 and seen_w.count(0.05) == 375)

# 5. split = unsplit, with the hooks' state (R: CS and CY; CR: the store and its generator)
for run, seed in (("R", 4), ("CR", 6)):
    fresh()
    short(run, 1500, 3000, seed)
    a1, s1, _ = w3k.train_net_w3k(run, seed, 3000, R, hours=1.0)
    _, qa, _ = w3k.train_net_w3k(run, seed, 3000, R, hours=1.0, pause_after=1900)
    b1, sb, _ = w3k.train_net_w3k(run, seed, 3000, R, hours=1.0, state=qa)
    same = all(np.array_equal(a1.p[k], b1.p[k]) for k in a1.p)
    same &= s1.get("cs_step") == sb.get("cs_step") and s1.get("cy_at") == sb.get("cy_at")
    same &= len(s1.get("pstore", [])) == len(sb.get("pstore", []))
    if s1.get("cs_p") is not None:
        same &= all(np.array_equal(s1["cs_p"][k], sb["cs_p"][k]) for k in s1["cs_p"])
    a2, _, _ = w3k.train_net_w3k(run, seed, 3000, R, hours=1.0)
    check(f"{run}: a split run equals an unsplit run (with the hooks' state); the same seed twice is the same",
          bool(same) and all(np.array_equal(a1.p[k], a2.p[k]) for k in a1.p))

# 6. drift and parent agreement: a brain against itself drifts 0
same = w3k.drift_and_parent(net_h, net_h, list(W.TEST_SEEDS)[:2], R)
other = w3k.drift_and_parent(net_h, B.DriveVIN(9, fixed_map=False), list(W.TEST_SEEDS)[:2], R)
check("drift: a brain against itself 0; against another brain > 0; parent agreement in [0, 1]",
      all(d["drift"] == 0 for d in same) and any(d["drift"] > 0 for d in other)
      and all(0 <= d["parent_agree"] <= 1 for d in same + other))

# 7. the machine record
w3k.machine("check", 0)
rec = __import__("json").loads((tmp / "machine_check_0.json").read_text())[-1]
check(f"the machine record ({rec['cpu'][:40]}; numpy {rec['numpy']}; {rec['env']})",
      rec["env"]["OPENBLAS_CORETYPE"] == "Haswell" and rec["numpy"])
shutil.rmtree(tmp)
print("All: PASS" if not fails else f"FAILED: {fails}")
