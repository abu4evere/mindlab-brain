"""MoveVIN's hand-written gradients against finite differences (random maps, levels, cells; a random linear loss on
the hand's logits and the critic's value). Prints the worst relative error per parameter."""
import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "W3"))
import numpy as np  # noqa: E402
import brain_mv as M  # noqa: E402

rng = np.random.default_rng(3)
net = M.MoveVIN(5)
for k in net.p:                                     # move away from the start so every part is active
    net.p[k] = net.p[k] + rng.normal(0, 0.2, net.p[k].shape)
T = 3
maps = (rng.random((T, M.C, M.N, M.N)) < 0.3).astype(float)
maps[:, 4] = rng.random((T, M.N, M.N))
levels = rng.random((T, 3))
rows = np.array([t * M.N * M.N + int(rng.integers(M.N * M.N)) for t in range(T)])
A, Bv = rng.normal(size=(T, 5)), rng.normal(size=T)


def loss():
    z, v = net.head(net.plan(maps, levels), rows)
    return float((A * z).sum() + (Bv * v).sum())


g = net.backprop(net.plan(maps, levels), rows, A, Bv)
worst = {}
for k, x in net.p.items():
    errs = []
    for i in range(min(x.size, 12)):
        idx = np.unravel_index(i, x.shape)
        old = x[idx]
        x[idx] = old + 1e-6; lp = loss()
        x[idx] = old - 1e-6; lm = loss()
        x[idx] = old
        num = (lp - lm) / 2e-6
        errs.append(abs(num - g[k][idx]) / max(1e-6, abs(num) + abs(g[k][idx])))
    worst[k] = max(errs)
print({k: f"{v:.1e}" for k, v in worst.items()})
print("All: PASS" if max(worst.values()) < 1e-4 else "FAIL")
