"""W3j checks, before any data. Prints All: PASS or the failures."""
import shutil
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import w3j  # noqa: E402
from w3j import w3i, w3d, w3b, B, W, R3  # noqa: E402

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
    w3j.OUT = tmp


def short(arm, fade, steps):
    w3j.ARMS[arm] = {"steps": steps, "fade": fade}
    w3j.configure(arm)
    w3j.w3b.OUT = w3j.w3i.OUT = tmp


# 1. the arms' schedules
okf = True
for arm in ("CK", "CV", "C4", "C2"):
    w3j.configure(arm)
    f = w3j.ARMS[arm]["fade"]
    cw, pp = w3d._ns["copy_weight"], w3d._ns["parent_present"]
    okf &= cw(0) == 0.5 and abs(cw(f // 2) - 0.25) < 1e-12
    okf &= (cw(f) == 0.05 and pp(f) and pp(3_000_000)) if arm == "CV" else (cw(f) == 0.0 and not pp(f))
check("fades: 0.5 to 0 over each arm's fade; CV keeps 0.05 after it (C4 1.2M, C2 2.4M)", okf
      and w3j.ARMS["C2"]["fade"] == 2_400_000 and w3j.ARMS["C4"]["steps"] == 4_000_000)
check("snapshots: the fade end, then every 400,000 steps (CK: 1.2M, 1.6M, 2.0M, 2.4M; C2: 2.4M to 3.6M)",
      w3j.snaps("CK") == (1_200_000, 1_600_000, 2_000_000, 2_400_000) and w3j.snaps("C2")[0] == 2_400_000)

# 2. CK: the learning rate drops only from the fade snapshot on (short run: fade 1,500, steps 3,000)
fresh()
short("CK", 1500, 3000)
seen = []
orig_apply = B.DriveVIN.apply


def spy(self, g):
    seen.append(B.LR)
    return orig_apply(self, g)


B.DriveVIN.apply = spy
w3j.train_staged("CK", 4, hours=1.0, steps=3000, snapshot_at=(1500,))
B.DriveVIN.apply = orig_apply
ok_lr = seen and seen[0] == w3j.LR0 and seen[-1] == w3j.LR0 * 0.1 and sorted(set(seen)) == sorted({w3j.LR0, w3j.LR0 * 0.1})
check(f"CK: the learning rate is {w3j.LR0} before the fade snapshot and x0.1 after ({len(seen)} updates)", bool(ok_lr))
check("the learning rate is restored after a CK run", B.LR == w3j.LR0)

# 3. CK before the fade equals C (its snapshot is CF, shared with C)
fresh()
short("C", 1500, 3000)
w3j.train_staged("C", 4, hours=1.0, steps=3000, snapshot_at=(1500,))
c_snap = dict(np.load(tmp / "C_4_1k.npz"))
fresh()
short("CK", 1500, 3000)
w3j.train_staged("CK", 4, hours=1.0, steps=3000, snapshot_at=(1500,))
ck_snap = dict(np.load(tmp / "CK_4_1k.npz"))
ck_final = dict(np.load(tmp / "CK_4.npz"))
check("CK's end-of-fade snapshot equals C's (CF is C's own brain at the fade end)",
      all(np.array_equal(c_snap[k], ck_snap[k]) for k in c_snap))

# 4. split = unsplit; the same seed twice (CV, short)
fresh()
short("CV", 1500, 3000)
w3d.CFG.update(child=1500)
p1, _, _ = w3d.train_net_parent("CV", 5, 3000, R, hours=1.0)
pa, qa, _ = w3d.train_net_parent("CV", 5, 3000, R, hours=1.0, pause_after=1400)
pb, _, _ = w3d.train_net_parent("CV", 5, 3000, R, hours=1.0, state=qa)
check("a split run equals an unsplit run (CV)", all(np.array_equal(p1.p[k], pb.p[k]) for k in p1.p))
p2, s2, _ = w3d.train_net_parent("CV", 5, 3000, R, hours=1.0)
check("the same seed twice is the same (CV)", all(np.array_equal(p1.p[k], p2.p[k]) for k in p1.p))
check(f"CV copies after the fade ({s2['updates'].get('copy')} copies in 3,000 steps; 750 expected)",
      s2["updates"].get("copy") == 750)

# 5. drift and parent agreement on a hand-made case: a brain against itself drifts 0
net = w3j.load_npz(tmp.parent / "tmp_checks" / "CV_5.npz", 5) if (tmp / "CV_5.npz").exists() else p1
same = w3j.drift_and_parent(net, net, list(W.TEST_SEEDS)[:2], R)
other = w3j.drift_and_parent(net, B.DriveVIN(9, fixed_map=False), list(W.TEST_SEEDS)[:2], R)
check(f"drift: a brain against itself 0 ({[d['drift'] for d in same]}); against another brain > 0 "
      f"({[round(d['drift'], 2) for d in other]}); parent agreement in [0, 1]",
      all(d["drift"] == 0 for d in same) and any(d["drift"] > 0 for d in other)
      and all(0 <= d["parent_agree"] <= 1 for d in same + other))
shutil.rmtree(tmp)
print("All: PASS" if not fails else f"FAILED: {fails}")
