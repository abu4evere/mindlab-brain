"""V2-3's checks before data (questions.md). python checks_v23.py -> PASS/FAIL lines and All."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import v23  # noqa: E402
import numpy as np  # noqa: E402
from v23 import B, W  # noqa: E402

OK = []


def check(name, cond, detail=""):
    OK.append(bool(cond))
    print(f"{name}: {'PASS' if cond else 'FAIL'} {detail}", flush=True)


def main():
    v23.OUT = HERE / "output_checks"
    v23.OUT.mkdir(exist_ok=True)
    # 1 FROZEN reproduces W3r's saved RMS fresh-land life (W3r's own test lands 910001+)
    ref = json.loads((v23.W3R / "output" / "test_fresh_RMS_1.json").read_text())
    got = [v23.life(v23.load_rms(1), 1, 910001 + i, "A")["lifespan"] for i in range(3)]
    check("1 FROZEN at home reproduces W3r's saved RMS lives (seed 1, 3 lands)", got == [r["lifespan"] for r in ref[:3]],
          f"{got}")
    # 2 learning rate 0 changes nothing
    keep = B.LR
    B.LR = 0.0
    v23.train("FREE", 1, 1500, "B1", "_lr0")
    B.LR = keep
    a, b = v23.load("FREE", 1, "_lr0"), v23.load_rms(1)
    check("2 FREE with learning rate 0 equals FROZEN", all(np.array_equal(a.p[k], b.p[k]) for k in a.p))
    # 3 the anchor's penalty is zero at the RMS weights, and grows away from them
    net = v23.load_rms(2)
    F = {k: np.ones_like(v) for k, v in net.p.items()}
    anc = v23.Anchored(net, F, {k: v.copy() for k, v in net.p.items()})
    z = all(not np.any(v) for v in anc.penalty().values())
    net.p["W0"] = net.p["W0"] + 0.1
    check("3 ANCHOR penalty 0 at the old weights, nonzero away", z and np.any(anc.penalty()["W0"]))
    # 4 worlds: B1 differs only in R; B2 also moves the shelter (not onto food or the start)
    la, ra = v23.world_land(999001, "A")
    l1, r1 = v23.world_land(999001, "B1")
    l2, r2 = v23.world_land(999001, "B2")
    same = all((np.array_equal(la[k], l1[k]) if isinstance(la[k], np.ndarray) else la[k] == l1[k]) for k in la)
    food = set(c for p in l2["patches"] for c in W.block_cells(p))
    check("4 B1 = A with R doubled; B2 also moves the shelter", same and r1 == 2 * ra == r2 and l2["shelter"] != la["shelter"]
          and l2["shelter"] not in food and l2["shelter"] != l2["start"] and not l2["walls"][l2["shelter"][1], l2["shelter"][0]])
    # 5 determinism
    v23.train("FREE", 2, 2000, "B1", "_d1")
    v23.train("FREE", 2, 2000, "B1", "_d2")
    a, b = v23.load("FREE", 2, "_d1"), v23.load("FREE", 2, "_d2")
    moved = not np.array_equal(a.p["Wo"], v23.load_rms(2).p["Wo"])
    check("5 the same training twice is identical (and learning moves the weights)",
          all(np.array_equal(a.p[k], b.p[k]) for k in a.p) and moved)
    # 6 REHEARSE adds home steps; REPLAY's buffer holds 20,000+ home transitions
    v23.train("REHEARSE", 2, 3500, "B1", "_r")
    lg = json.loads((v23.OUT / "trainlog_REHEARSE_2_r.json").read_text())["log"][-1]
    check("6 REHEARSE: home steps counted apart from the B budget", lg["step"] == 3500 and lg["home_steps"] > 0,
          f"{lg}")
    buf = v23.home_buffer(v23.load_rms(2), 2)
    check("6 REPLAY buffer of home segments >= 20,000 steps", sum(len(s["acts"]) for s in buf) >= 20000 and
          all(len(s["rets"]) == len(s["acts"]) for s in buf), f"{len(buf)} segments")
    # 7 ANCHOR and SLOW train
    v23.train("ANCHOR", 2, 1500, "B1", "_a")
    v23.train("SLOW", 2, 1500, "B1", "_s")
    d_slow = float(np.abs(v23.load("SLOW", 2, "_s").p["Wo"] - v23.load_rms(2).p["Wo"]).max())
    d_free = float(np.abs(v23.load("FREE", 2, "_d1").p["Wo"] - v23.load_rms(2).p["Wo"]).max())
    check("7 ANCHOR and SLOW run; SLOW moves less than FREE", d_slow < d_free, f"slow {d_slow:.5f} free {d_free:.5f}")
    print("All:", "PASS" if all(OK) else "FAIL", f"({sum(OK)}/{len(OK)})")


if __name__ == "__main__":
    main()
