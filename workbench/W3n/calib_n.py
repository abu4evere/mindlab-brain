"""W3n calibration (before any study data): W3m's SL kept copies, with the hunger reflex added at test (the sleep
reflex on, as in their training), on W3's calibration lands (800001-800050; never the test or fresh lands), for hunger
lines 50, 60, 70, 80 (0 = no hunger reflex). Picks the line by lifespan."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import w3n  # noqa: E402
import numpy as np  # noqa: E402
from w3n import w3k, w3m, W  # noqa: E402
from w3k import R3  # noqa: E402

seed, line = int(sys.argv[1]), float(sys.argv[2])
w3n.OUT = w3k.OUT = w3m.OUT = HERE / "calib"
w3n.OUT.mkdir(exist_ok=True)
w3n.configure("HR", seed)
w3n.BODY.update(cheap=False, hunger=line > 0)
w3n.H_LINE = line
net = w3k.load_npz(HERE.parent / "W3m" / "output" / f"SL_CS_{seed}.npz", seed)
R = R3.regrowth()
w3n.HC.update(steps=0, hunger=0, meals=0)
lives = [w3k.w3i.test_life(net, ls, R) for ls in W.CAL_SEEDS]
out = {"seed": seed, "line": line, "lifespan": float(np.mean([l["lifespan"] for l in lives])),
       "survived": float(np.mean([l["survived"] for l in lives])), "hungry": float(np.mean([l["hungry"] for l in lives])),
       "hunger_share": w3n.HC["hunger"] / max(1, w3n.HC["steps"]), "reflex_meals": w3n.HC["meals"]}
(w3n.OUT / f"cal_{seed}_{int(line)}.json").write_text(json.dumps(out))
print(json.dumps(out))
