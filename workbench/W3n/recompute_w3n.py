"""W3n's two primary readings, recomputed from the raw test files by a separate script (not analyse_w3n.py):
mean test-land lifespan per seed (50 lives each), the paired difference HRS - SLS and CRS - SLS over seeds 1-16, with a
percentile bootstrap (another numpy seed, 20261201, 20,000 resamples, 97.5%) and, beside it, a t interval.
Also each arm's fresh-land survival. Writes nothing; prints."""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
SRC = {"HRS": HERE / "output", "CRS": HERE / "output", "HCS": HERE / "output", "SLS": HERE.parent / "W3m" / "output"}
SEEDS = range(1, 17)


def per_seed(arm, prefix="test_"):
    out = []
    for s in SEEDS:
        L = json.loads((SRC[arm] / f"{prefix}{arm}_{s}.json").read_text())
        assert len(L) == 50, (arm, s, len(L))
        out.append(np.mean([l["lifespan" if prefix == "test_" else "survived"] for l in L]))
    return np.array(out)


def boot(d, level=97.5):
    rng = np.random.default_rng(20261201)
    m = d[rng.integers(0, len(d), (20_000, len(d)))].mean(1)
    a = (100 - level) / 2
    return np.percentile(m, a), np.percentile(m, 100 - a)


def tint(d, level=97.5):
    from math import sqrt
    t = {97.5: 2.490, 95: 2.131}[level]                 # t(15) quantiles 0.9875 and 0.975 (two-sided 97.5% and 95%)
    se = d.std(ddof=1) / sqrt(len(d))
    return d.mean() - t * se, d.mean() + t * se


life = {a: per_seed(a) for a in SRC}
for a, v in life.items():
    print(f"{a}: mean lifespan {v.mean():.1f}; fresh-land survival {per_seed(a, 'test_fresh_').mean():.3f}")
for a in ("HRS", "CRS"):
    d = life[a] - life["SLS"]
    lo, hi = boot(d)
    tl, th = tint(d)
    print(f"{a} - SLS: {d.mean():+.1f} bootstrap 97.5% [{lo:+.1f}, {hi:+.1f}]; t 97.5% [{tl:+.1f}, {th:+.1f}]; "
          f"{int((d > 0).sum())} of 16 seeds above 0")
