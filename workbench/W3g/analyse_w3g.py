"""W3g's frozen analysis (questions.md), written before any data. Lifespan and survival, FM against W3d's PYFR (paired
by seed; bootstrap numpy seed 20261136); and WX's death labels for FM (the same recorder, on FM's test lives)."""
import json
import sys
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "WX"))
import w3g  # noqa: E402
w3g.configure()
import wx  # noqa: E402  (W3's modules, with W3g's patched World and brain class)
from w3g import B, W, R3  # noqa: E402

SEEDS = range(1, 9)
IDX = np.random.default_rng(20261136).integers(0, 8, (10_000, 8))


def ci(v):
    v = np.asarray(v, float)
    m = v[IDX].mean(axis=1)
    return [round(float(v.mean()), 3), round(float(np.percentile(m, 2.5)), 3), round(float(np.percentile(m, 97.5)), 3)]


def means(path):
    L = json.loads(Path(path).read_text())
    return {"lifespan": float(np.mean([l["lifespan"] for l in L])), "survived": float(np.mean([l["survived"] for l in L]))}


FM = [means(HERE / "output" / f"test_FM_{s}.json") for s in SEEDS]
PY = [means(HERE.parent / "W3d" / "output" / f"test_PYFR_{s}.json") for s in SEEDS]
f3 = lambda t: f"{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]"
out = {"FM": {k: ci([r[k] for r in FM]) for k in ("lifespan", "survived")},
       "PYFR": {k: ci([r[k] for r in PY]) for k in ("lifespan", "survived")},
       "FM-PYFR": {k: ci([a[k] - b[k] for a, b in zip(FM, PY)]) for k in ("lifespan", "survived")}}
# reading 2: WX's death labels on FM's test lives
labels = []
for s in SEEDS:
    net = B.DriveVIN(s)
    with np.load(HERE / "output" / f"FM_{s}.npz") as z:
        for k in net.p:
            net.p[k] = z[k].copy()
    R = R3.regrowth()
    for ls in W.TEST_SEEDS:
        rng = np.random.default_rng(ls)
        lf = wx.life(lambda w: net.act(w.obs_map(), R3.levels(w, "D3"), w.pos, rng)[0], W.make_land(ls), R, rng)
        if lf["dead"]:
            labels.append(lf["labels"])
out["FM death labels"] = {k: round(float(np.mean([d[k] for d in labels])), 3) for k in ("no_food_known", "food_known_not_reached", "exhaustion")}
out["FM deaths"] = len(labels)
L = ["# W3g analysis (the frozen analysis, analyse_w3g.py)", "",
     f"- FM: lifespan {f3(out['FM']['lifespan'])}; survival {f3(out['FM']['survived'])}",
     f"- PYFR (W3d): lifespan {f3(out['PYFR']['lifespan'])}; survival {f3(out['PYFR']['survived'])}",
     f"- **Reading 1, FM − PYFR:** lifespan {f3(out['FM-PYFR']['lifespan'])}; survival {f3(out['FM-PYFR']['survived'])}",
     f"- **Reading 2, FM's death labels** ({len(labels)} deaths; W3d: no food known 0.80, exhaustion 0.63): {out['FM death labels']}",
     f"- **Reading 3, toward the bar (0.80):** FM survival {out['FM']['survived'][0]:.3f}"]
(HERE / "analysis.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
(HERE / "analysis.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
