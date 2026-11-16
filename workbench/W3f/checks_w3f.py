"""W3f checks, before any data. Prints All: PASS or the failures."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import w3f  # noqa: E402
from w3f import w3b, w3d, B, W, R3  # noqa: E402

fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        fails.append(name)


R = R3.regrowth()
HERE = Path(__file__).parent
# 0. the generation-1 pools exist and hold 8 visible successes (identical for CH and RN: the same G2 adults)
pc = json.loads((HERE / "pool_CH_1.json").read_text())["visible"]
pr = json.loads((HERE / "pool_RN_1.json").read_text())["visible"]
check(f"generation-1 pools: 8 values, the same for CH and RN ({[round(v) for v in pc]})", len(pc) == 8 and pc == pr)

# 1. CH picks the most visible of the 4 met; RN one of the same 4; both arms meet the same 4
w3f.configure("CH", 1, 3)
ok_ch, met_same = True, True
for life in range(1, 60):
    met = np.random.default_rng([3, 61, 1, life]).choice(8, 4, replace=False)
    c = w3f.choose(life)
    ok_ch = ok_ch and c in met and w3f._S["vis"][c] == max(w3f._S["vis"][i] for i in met)
check("CH picks the most visibly successful of the 4 adults met", ok_ch)
w3f.configure("RN", 1, 3)
picks = [w3f.choose(life) for life in range(1, 200)]
ok_rn = all(p in np.random.default_rng([3, 61, 1, life]).choice(8, 4, replace=False) for life, p in zip(range(1, 200), picks))
check(f"RN picks one of the same 4 (distinct adults picked: {len(set(picks))})", ok_rn and len(set(picks)) >= 6)

# 2. the copied act is the chosen adult's argmax; adults never change
w = W.World(W.make_land(W.TEST_SEEDS[0]), R)
m, lev = w.obs_map(), R3.levels(w, "D3")
ad = w3f._S["adults"][2]
fw = ad.plan(m[None], np.asarray(lev, float)[None])
z, _ = ad.head(fw, np.array([w.pos[1] * B.N + w.pos[0]]))
check("adult_act is the adult's argmax", w3f.adult_act(2, m, lev, w.pos) == int(np.argmax(z[0])))
before = [{k: v.copy() for k, v in a.p.items()} for a in w3f._S["adults"]]

# 3. no childhood: reproduces W3b's YFR; with a short childhood copies happen, spread over chosen adults
w3d.CFG.update(child=0, always=False)
a, _, _ = w3f.train_net_choose("CH1", 3, 2500, R, hours=1.0)
b, _, _ = w3b.train_net("YFR", 3, 2500, R, hours=1.0)
check("no childhood reproduces W3b's YFR training exactly", all(np.array_equal(a.p[k], b.p[k]) for k in a.p))
w3d.CFG.update(child=2000, always=False)
w3f.configure("CH", 1, 3)
w3d.CFG.update(child=2000, always=False)
n, s, _ = w3f.train_net_choose("CH1", 3, 3000, R, hours=1.0)
check(f"copies every 4th step during childhood ({s['updates'].get('copy')}; expected 500)", s["updates"].get("copy") == 500)
check("adults never change", all(all(np.array_equal(bf[k], a2.p[k]) for k in bf) for bf, a2 in zip(before, w3f._S["adults"])))

# 4. split = unsplit (RN)
w3f.configure("RN", 1, 4)
w3d.CFG.update(child=2000, always=False)
p1, _, _ = w3f.train_net_choose("RN1", 4, 3000, R, hours=1.0)
pa, qa, _ = w3f.train_net_choose("RN1", 4, 3000, R, hours=1.0, pause_after=1400)
pb, _, _ = w3f.train_net_choose("RN1", 4, 3000, R, hours=1.0, state=qa)
check("a split run equals an unsplit run", all(np.array_equal(p1.p[k], pb.p[k]) for k in p1.p))
print("All: PASS" if not fails else f"FAILED: {fails}")
