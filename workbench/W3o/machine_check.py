"""Does another machine train exactly as this PC? A short RE and a short HR training (the frozen code, 6,000 steps,
1,500 fade) and the SHA-256 of all their weights; run on both machines and compare the printed lines.

  python machine_check.py
"""
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import w3o  # noqa: E402  (the numerical settings before numpy loads)
import numpy as np  # noqa: E402
from w3o import w3k, w3m, w3n  # noqa: E402
from w3k import R3  # noqa: E402

R = R3.regrowth()
w3k.CS_WINDOW, w3k.CS_START = 400, 200
tmp = HERE / "tmp_machine"
tmp.mkdir(exist_ok=True)
w3k.OUT = w3m.OUT = w3n.OUT = w3o.OUT = tmp
for arm in ("RE", "HR"):
    w3k.RUNS[arm] = {"steps": 6000, "fade": 1500}
    (w3o.configure if arm in w3o.ARMS else w3n.configure)(arm, 6)
    w3k.w3b.OUT = w3k.w3i.OUT = tmp
    net, _, _ = w3m.train_net_w3m(arm, 6, 6000, R, hours=1.0)
    h = hashlib.sha256(b"".join(np.ascontiguousarray(net.p[k]).tobytes() for k in sorted(net.p))).hexdigest()
    print(arm, h, w3k.CPU, flush=True)
