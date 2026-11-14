"""WN: how many neurons? A size sweep of WS's memory child, and a growing brain (questions.md, WN-frozen).

WS's task, learning rule and tests (../WS/ws.py), with the number of neurons n as a parameter.
  M-n: the memory child (learned recurrent ring), n in 8..256.   F-n: no ring (WS's B0).
  G:   the memory child born with 16 neurons, doubling at the end of days 8, 16 and 24 (to 128). Old connections are
       kept; the new neurons' incoming connections start N(0, 0.01^2); their outgoing connections (to the hands and to
       old neurons) start at zero, so growing does not change what the child does at that moment.

The starting weights use WS's draw [seed, 4] and every brain uses WS Bm's act draws [seed, 3, 4], so M-32 is WS's Bm
exactly (a check).

  python wn.py one BRAIN SEED OUT_DIR
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "WS"))
import ws  # noqa: E402

BRAINS = ("M8", "M16", "M32", "M64", "M128", "M256", "F8", "F32", "F128", "G")
GROW_AFTER = {8: 32, 16: 64, 24: 128}            # end of day d -> neurons
TEST_DAYS, SHOW_TEST_DAYS = (7, 15, 30, 60), (30,)
COPY_RATE = 0.5


class Net:
    def __init__(self, seed, n, recurrent):
        r = np.random.default_rng([seed, 4])
        self.n, self.rec = n, recurrent
        self.p = {"Wx": r.normal(0, 0.1, (n, ws.N_IN)), "b": np.zeros(n),
                  "Wh": r.normal(0, 0.1, (n, n)) if recurrent else np.zeros((n, n)),
                  "M": r.normal(0, 0.1, (ws.ACTS, n)), "c": np.zeros(ws.ACTS)}
        self.base = 0.0
        self.grow_rng = np.random.default_rng([seed, 9])

    def step(self, x, hprev):
        hp = hprev if self.rec else np.zeros(self.n)
        h = np.tanh(self.p["Wx"] @ x + self.p["Wh"] @ hp + self.p["b"])
        return h, self.p["M"] @ h + self.p["c"]

    def grads(self, xs, hs, targets):
        g = {k: np.zeros_like(v) for k, v in self.p.items()}
        dh_next = np.zeros(self.n)
        for t in reversed(range(len(xs))):
            h = hs[t]
            dh = dh_next.copy() if self.rec else np.zeros(self.n)
            if t in targets:
                a, scale = targets[t]
                dz = ws.softmax(self.p["M"] @ h + self.p["c"])
                dz[a] -= 1.0
                dz *= scale
                g["M"] += np.outer(dz, h)
                g["c"] += dz
                dh += self.p["M"].T @ dz
            dpre = dh * (1.0 - h ** 2)
            g["Wx"] += np.outer(dpre, xs[t])
            g["b"] += dpre
            if self.rec:
                hp = hs[t - 1] if t > 0 else np.zeros(self.n)
                g["Wh"] += np.outer(dpre, hp)
                dh_next = self.p["Wh"].T @ dpre
        return g

    apply = ws.Net.apply

    def grow(self, new_n):
        r, n, k = self.grow_rng, self.n, new_n - self.n
        self.p["Wx"] = np.vstack([self.p["Wx"], r.normal(0, 0.01, (k, ws.N_IN))])
        self.p["b"] = np.concatenate([self.p["b"], np.zeros(k)])
        Wh = np.zeros((new_n, new_n))
        Wh[:n, :n] = self.p["Wh"]
        Wh[n:, :] = r.normal(0, 0.01, (k, new_n))         # into the new neurons, from all neurons
        self.p["Wh"] = Wh                                  # out of the new neurons into the old ones: zero
        self.p["M"] = np.hstack([self.p["M"], np.zeros((ws.ACTS, k))])
        self.n = new_n


def run_prefix(net, prefix):
    h = np.zeros(net.n)
    xs, hs = [], []
    for x in prefix:
        h, _ = net.step(x, h)
        xs.append(x)
        hs.append(h)
    return xs, hs, h


ws.run_prefix = run_prefix                        # ws's try_box, copy_step and test then work at any size


def run(brain, seed, out=None):
    t0 = time.process_time()
    home = ws.Home(seed)
    rec = brain[0] in "MG"
    net = Net(seed, 16 if brain == "G" else int(brain[1:]), rec)
    rng = np.random.default_rng([seed, 3, ws.BRAINS.index("Bm")])
    tests, show_tests, sizes = {}, {}, {}
    for d in range(1, ws.DAYS + 1):
        for k, look, rnd in home.day(d):
            prefix = []
            if d <= ws.DEMO_DAYS:
                prefix = ws.show_steps(look, home.pairs[k]) if rec else []
                ws.copy_step(net, look, home.pairs[k], prefix, COPY_RATE)
            ws.try_box(net, look, home.pairs[k], prefix, rng, True)
        if d in TEST_DAYS:
            tests[d] = ws.test(home, net, seed, d)
            sizes[d] = net.n
        if d in SHOW_TEST_DAYS:
            show_tests[d] = ws.test(home, net, seed, d, showing=True)
        if brain == "G" and d in GROW_AFTER:
            net.grow(GROW_AFTER[d])
    res = {"brain": brain, "seed": seed, "tests": tests, "show_tests": show_tests, "sizes": sizes,
           "cpu_secs": round(time.process_time() - t0, 2)}
    if out is not None:
        out = Path(out)
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{brain}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    return res


if __name__ == "__main__":
    if sys.argv[1] == "one":
        r = run(sys.argv[2], int(sys.argv[3]), sys.argv[4])
        print(sys.argv[2], sys.argv[3], {d: round(v["success"], 2) for d, v in r["tests"].items()}, r["cpu_secs"])
