"""W3m calibration (before any study data): W3k's CS brains with the sleep reflex added at test, on W3's calibration
lands (800001-800050; never the test or fresh lands), for hunger lines 40, 60, 90, 120. Picks the line by lifespan."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import w3m  # noqa: E402
import numpy as np  # noqa: E402
from w3m import w3k, W, R3  # noqa: E402

seed, line = int(sys.argv[1]), float(sys.argv[2])
w3m.OUT = w3k.OUT = HERE / "calib"
w3m.OUT.mkdir(exist_ok=True)
w3k.configure("R", seed)
w3m.PART.update(reflex="walk" if line > 0 else False, urge=False)
w3m.E_HUNGER = line
net = w3k.load_npz(HERE.parent / "W3k" / "output" / f"R_CS_{seed}.npz", seed)
R = R3.regrowth()
w3m.COUNT.update(steps=0, forced=0)
lives = [w3k.w3i.test_life(net, ls, R) for ls in W.CAL_SEEDS]
out = {"seed": seed, "line": line, "lifespan": float(np.mean([l["lifespan"] for l in lives])),
       "survived": float(np.mean([l["survived"] for l in lives])),
       "exhausted": float(np.mean([l["exhausted"] for l in lives])), "forced": w3m.COUNT["forced"] / max(1, w3m.COUNT["steps"])}
(w3m.OUT / f"cal_{seed}_{int(line)}.json").write_text(json.dumps(out))
print(json.dumps(out))
