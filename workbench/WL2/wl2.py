"""WL2: why does the leaky memory work? (questions.md, WL2-frozen). WL's world and child; arms L0, L2 (WL's),
W8 (wait, no noise), NS (noisy showing steps, no wait), NP (noise 0.3 on every practice step, none in tests),
Linf (blank memory before each try; copy without the showing in memory).

  python wl2.py arm ARM SIZE OUT_DIR      (seeds 1-48)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "WL"))
import wl  # noqa: E402  (patches ws.run_prefix with wait steps)
import wn  # noqa: E402
import ws  # noqa: E402

ARMS = ("L0", "L2", "W8", "NS", "NP", "Linf")
NP_SIGMA = 0.3


class Noisy:
    """A showing step whose neurons get noise added to their input."""
    def __init__(self, x, eps):
        self.x, self.eps = x, eps


def run_prefix(net, prefix):
    h = np.zeros(net.n)
    xs, hs = [], []
    for item in prefix:
        hp = h if net.rec else np.zeros(net.n)
        if isinstance(item, wl.Wait):
            x = np.zeros(ws.N_IN)
            h = np.tanh(net.p["Wx"] @ x + net.p["Wh"] @ hp + net.p["b"] + item.eps)
        elif isinstance(item, Noisy):
            x = item.x
            h = np.tanh(net.p["Wx"] @ x + net.p["Wh"] @ hp + net.p["b"] + item.eps)
        else:
            x = item
            h, _ = net.step(x, h)
        xs.append(x)
        hs.append(h)
    return xs, hs, h


ws.run_prefix = run_prefix


class Net(wn.Net):
    """WN's network; with noise_on, every step adds N(0, NP_SIGMA^2) to the neurons' input (NP)."""
    def __init__(self, seed, n, recurrent, np_noise=False):
        super().__init__(seed, n, recurrent)
        self.np_rng = np.random.default_rng([seed, 15]) if np_noise else None
        self.noise_on = False

    def step(self, x, hprev):
        if not (self.np_rng is not None and self.noise_on):
            return super().step(x, hprev)
        hp = hprev if self.rec else np.zeros(self.n)
        h = np.tanh(self.p["Wx"] @ x + self.p["Wh"] @ hp + self.p["b"] + self.np_rng.normal(0, NP_SIGMA, self.n))
        return h, self.p["M"] @ h + self.p["c"]


def episode(arm, look, pairs, n, rng):
    show = ws.show_steps(look, pairs)
    if arm == "L2":
        return show + [wl.Wait(rng.normal(0, 0.6, n)) for _ in range(8)]
    if arm == "W8":
        return show + [wl.Wait(np.zeros(n)) for _ in range(8)]
    if arm == "NS":
        return [Noisy(x, rng.normal(0, 0.6, n)) for x in show]
    if arm == "Linf":
        return []
    return show                                     # L0, NP


def test(arm, home, net, seed, d, showing=False):
    r = np.random.default_rng([seed, 6, d, int(showing)])
    nr = np.random.default_rng([seed, 14, d])
    full = []
    for k in range(ws.KINDS):
        look = home.looks[k] + r.normal(0, 0.2, ws.LOOK)
        prefix = episode(arm, look, home.pairs[k], net.n, nr) if showing else []
        full.append(1.0 if ws.try_box(net, look, home.pairs[k], prefix, None, False)[0] == ws.LIDS else 0.0)
    return float(np.mean(full))


def run_child(arm, n, seed):
    home = ws.Home(seed)
    net = Net(seed, n, True, np_noise=(arm == "NP"))
    rng = np.random.default_rng([seed, 3, ws.BRAINS.index("Bm")])
    nrng = np.random.default_rng([seed, 13])
    tests, food, show30 = {}, 0, None
    for d in range(1, ws.DAYS + 1):
        net.noise_on = True
        for k, look, rnd in home.day(d):
            prefix = []
            if d <= ws.DEMO_DAYS:
                prefix = episode(arm, look, home.pairs[k], n, nrng)
                ws.copy_step(net, look, home.pairs[k], prefix, wn.COPY_RATE)
            food += ws.try_box(net, look, home.pairs[k], prefix, rng, True)[0]
        net.noise_on = False
        if d in wl.TEST_DAYS:
            tests[d] = test(arm, home, net, seed, d)
        if d == 30:
            show30 = test(arm, home, net, seed, d, showing=True)
    return {"arm": arm, "n": n, "seed": seed, "tests": tests, "food": food, "show30": show30}


if __name__ == "__main__":
    if sys.argv[1] == "arm":
        arm, n, out = sys.argv[2], int(sys.argv[3]), Path(sys.argv[4])
        out.mkdir(parents=True, exist_ok=True)
        for s in range(1, 49):
            (out / f"{arm}_{n}_seed_{s}.json").write_text(json.dumps(run_child(arm, n, s)), encoding="utf-8")
        print("done", arm, n, flush=True)
