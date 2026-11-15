"""WR checks, before any data (questions.md, Checks). Prints All: PASS or the failures."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import wr  # noqa: E402
import wf  # noqa: E402
import wy  # noqa: E402
import wn  # noqa: E402
import ws  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


WB = Path(__file__).parent.parent


def same_tests(a, b):
    return {str(k): v for k, v in a["tests"].items()} == {str(k): v for k, v in b["tests"].items()}


# 1. the changing world reproduces WY's Base and TBYS (size 32, seed 1001) and WF's RP (sizes 32 and 128, seed 1001)
for arm, src, name in (("Base", "WY", "Base32"), ("TY", "WY", "TBYS32")):
    a = wr.run_child("change", arm, 32, 1001)
    b = json.loads((WB / src / "output" / f"{name}_seed_1001.json").read_text())
    check(f"change {arm}-32 reproduces {src}'s {name} (tests, food)", same_tests(a, b) and a["food"] == b["food"])
for n in (32, 128):
    a = wr.run_child("change", "TYR", n, 1001)
    b = json.loads((WB / "WF" / "output" / f"RP{n}_seed_1001.json").read_text())
    check(f"change TYR-{n} reproduces WF's RP{n} (tests, food, replays)",
          same_tests(a, b) and a["food"] == b["food"] and a["replays"] == b["replays"])

# 2. the stable world reproduces WL2's L0 and Linf (sizes 32 and 128, seed 1): tests, food, after-showing skill
for arm, name in (("L0", "L0"), ("L", "Linf")):
    for n in (32, 128):
        a = wr.run_child("stable", arm, n, 1)
        b = json.loads((WB / "WL2" / "output" / f"{name}_{n}_seed_1.json").read_text())
        check(f"stable {arm}-{n} reproduces WL2's {name} (tests, food, show30)",
              same_tests(a, b) and a["food"] == b["food"] and a["show30"] == b["show30"])

# 3. L: an empty memory before the copy step and the try even when the teacher shows; without L, the showing steps
look = np.random.default_rng(1).normal(0, 1, ws.LOOK)
pairs = [(1, 2), (0, 3)]
check("L gives an empty prefix", wr.prefix_for("LTYR", look, pairs) == [])
p = wr.prefix_for("TYR", look, pairs)
check("without L the prefix is the 4 showing steps", len(p) == 4 and all(np.array_equal(x, y) for x, y in zip(p, ws.show_steps(look, pairs))))

# 4. T: a blocked pair is never chosen in practice (15 of 16 pairs blocked on lid 0 -> the free one is chosen)
net = wn.Net(4, 32, True)
free = (2, 3)
tabu = {0: {(a, b) for a in range(ws.ACTS) for b in range(ws.ACTS)} - {free}, 1: set()}
r = np.random.default_rng(9)
chosen = [wf.try_box(wn.Net(4, 32, True), look, pairs, [], r, True, tabu)[1][0] for _ in range(20)]
check("T: only the unblocked pair is chosen on a blocked lid (20 draws)", all(tuple(c) == free for c in chosen))

# 5. Y: a self-copy raises the copied act (WY's check); R: replays happen; Y fires in the recipe
h, z = net.step(ws.x_try(look, 0, None, 0), np.zeros(32))
p0 = ws.softmax(z)[2]
wy.self_copy(net, look, [[2, 1]], [1.0], [])
_, z2 = net.step(ws.x_try(look, 0, None, 0), np.zeros(32))
check("Y: self-copy raises the copied act", ws.softmax(z2)[2] > p0)
res = {a: wr.run_child("change", a, 32, 1002) for a in wr.ARMS["change"]}
check(f"R: replays happen in LTYR ({res['LTYR']['replays']})", res["LTYR"]["replays"] > 0)
check(f"Y: self-copies happen in LTYR ({res['LTYR']['self_copies']})", res["LTYR"]["self_copies"] > 0)
check("no replay without R (LTY)", res["LTY"]["replays"] == 0)
check("no self-copy without Y (LTR)", res["LTR"]["self_copies"] == 0)

# 6. the same child twice is the same; the eight changing-world arms give eight different lives (seed 1002, size 32)
check("same child twice is the same (LTYR)", wr.run_child("change", "LTYR", 32, 1002) == res["LTYR"])
check("eight changing-world arms give eight different lives",
      len({json.dumps(r["tests"]) + str(r["food"]) for r in res.values()}) == 8)
st = {a: wr.run_child("stable", a, 32, 2) for a in wr.ARMS["stable"]}
check("four stable-world arms give four different lives",
      len({json.dumps(r["tests"]) + str(r["food"]) for r in st.values()}) == 4)
print("All: PASS" if not fails else f"FAILED: {fails}")
