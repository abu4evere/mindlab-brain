"""WL: a leaky memory (questions.md, WL-frozen). WN's world (a showing before every try on days 1-30) and memory
child; between the showing and the try there are D wait steps with no input and noise N(0, sigma^2) on each neuron's
input. The copy step and the try share one memory episode (the same showing and noise).

  python wl.py arm LEVEL SIZE OUT_DIR      (LEVEL: L0 | L1 | L2; seeds 1-48)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "WN"))
import wn  # noqa: E402  (patches ws.run_prefix for any size; replaced below by a version that knows wait steps)
import ws  # noqa: E402

LEVELS = {"L0": (0, 0.0), "L1": (4, 0.3), "L2": (8, 0.6)}
TEST_DAYS = (7, 15, 30, 60)


class Wait:
    """One wait step: no input; noise added to every neuron's input before its activation."""
    def __init__(self, eps):
        self.eps = eps


def run_prefix(net, prefix):
    h = np.zeros(net.n)
    xs, hs = [], []
    for item in prefix:
        if isinstance(item, Wait):
            x = np.zeros(ws.N_IN)
            hp = h if net.rec else np.zeros(net.n)
            h = np.tanh(net.p["Wx"] @ x + net.p["Wh"] @ hp + net.p["b"] + item.eps)
        else:
            x = item
            h, _ = net.step(x, h)
        xs.append(x)
        hs.append(h)
    return xs, hs, h


ws.run_prefix = run_prefix          # ws's try_box, copy_step and test now go through wait steps


def episode(look, pairs, n, level, rng):
    D, sigma = LEVELS[level]
    return ws.show_steps(look, pairs) + [Wait(rng.normal(0, sigma, n)) for _ in range(D)]


def test(home, net, seed, d, showing=False):
    r = np.random.default_rng([seed, 6, d, int(showing)])
    nr = np.random.default_rng([seed, 14, d])
    full = []
    for k in range(ws.KINDS):
        look = home.looks[k] + r.normal(0, 0.2, ws.LOOK)
        prefix = episode(look, home.pairs[k], net.n, LEVEL, nr) if showing else []
        full.append(1.0 if ws.try_box(net, look, home.pairs[k], prefix, None, False)[0] == ws.LIDS else 0.0)
    return float(np.mean(full))


LEVEL = "L0"


def run_child(level, n, seed):
    """One child's life; the after-showing test at day 30 is taken on the day-30 network."""
    global LEVEL
    LEVEL = level
    home = ws.Home(seed)
    net = wn.Net(seed, n, True)
    rng = np.random.default_rng([seed, 3, ws.BRAINS.index("Bm")])
    nrng = np.random.default_rng([seed, 13])
    tests, food, show30 = {}, 0, None
    for d in range(1, ws.DAYS + 1):
        for k, look, rnd in home.day(d):
            prefix = []
            if d <= ws.DEMO_DAYS:
                prefix = episode(look, home.pairs[k], n, level, nrng)
                ws.copy_step(net, look, home.pairs[k], prefix, wn.COPY_RATE)
            food += ws.try_box(net, look, home.pairs[k], prefix, rng, True)[0]
        if d in TEST_DAYS:
            tests[d] = test(home, net, seed, d)
        if d == 30:
            show30 = test(home, net, seed, d, showing=True)
    return {"level": level, "n": n, "seed": seed, "tests": tests, "food": food, "show30": show30}


if __name__ == "__main__":
    if sys.argv[1] == "arm":
        level, n, out = sys.argv[2], int(sys.argv[3]), Path(sys.argv[4])
        out.mkdir(parents=True, exist_ok=True)
        for s in range(1, 49):
            (out / f"{level}_{n}_seed_{s}.json").write_text(json.dumps(run_child(level, n, s)), encoding="utf-8")
        print("done", level, n, flush=True)
