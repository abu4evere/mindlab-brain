"""W3p pilot readout (exploratory, labelled): the Bob Profile probes (BP-frozen functions, unchanged) on the pilot
brains PMV (MoveVIN) and PHR (DriveVIN), 800k steps, seeds 1-3, plus the value-map uphill measure.

  python pilot_probe.py ARM SEED      ARM in PMV, PHR
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
import bp_mv  # noqa: E402  (BP-frozen tests, MoveVIN loader)
from bp_mv import T, w3p, R3  # noqa: E402

arm, seed = sys.argv[1], int(sys.argv[2])
R = R3.regrowth()
T.w3n.configure("HR", 1)
if arm == "PMV":
    w3p.configure("PMV", seed)
else:
    w3p.B.DriveVIN = w3p.DRIVE
net = w3p.w3k.load_npz(HERE.parent / "output" / f"{arm}_CS_{seed}.npz", seed)
T.body(False)
res = {"arm": arm, "seed": seed, "brain": type(net).__name__,
       "R2": T.t_R2(net, R)["success"], "R5d": T.t_R5d(net, R)["success"], "M2": T.t_M2(net, R)["success"],
       "uphill": bp_mv.plan_uphill(net, R)["uphill"]}
(HERE / f"pilot_{arm}_{seed}.json").write_text(json.dumps(res))
print(json.dumps(res), flush=True)
