"""Can MoveVIN solve the R2 detours at all? Hand-set weights (food is worth +1 when hungry, walls cannot be entered,
a small cost per place), then the Bob Profile R2 probe (BP-frozen) with these weights. A capacity check of the design,
not a result."""
import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "scorecard" / "bp"))
import bp_tests as T  # noqa: E402
import numpy as np  # noqa: E402
sys.path.insert(0, str(HERE))
import brain_mv as M  # noqa: E402
from bp_tests import W, R3  # noqa: E402

T.w3n.configure("HR", 1)
R = R3.regrowth()
net = M.MoveVIN(1)
for k in net.p:
    net.p[k][:] = 0
net.p["Ws"][0, W.CH_FOOD, 1, 1] = 3.0
net.p["br"][0] = -0.05
net.p["Wp"][0, W.CH_WALL, 1, 1] = -20.0
net.p["bp"][0] = 10.0
net.p["g"][0] = 3.0
net.p["lb"][0] = np.log(20.0)
T.body(False)
print("R2", T.t_R2(net, R), "R5d", T.t_R5d(net, R), "M2", T.t_M2(net, R))
