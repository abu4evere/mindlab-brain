"""WG: growing with awake neurons (questions.md, WG-frozen). WN's task and memory child (../WN/wn.py); only the way
new neurons start differs.
  G   silent: new incoming N(0, 0.01^2), new outgoing zero (WN's G, wn.Net.grow).
  GA  awake in, quiet out: new incoming N(0, 0.1^2); new outgoing (to the hands and old neurons) zero.
  GF  fully awake: new incoming and outgoing N(0, 0.1^2).
  GA32  as GA, born 8, growing to 16 and 32.

  python wg.py one BRAIN SEED OUT_DIR
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "WN"))
import wn  # noqa: E402  (also patches ws.run_prefix for any size)
import ws  # noqa: E402

BRAINS = ("M16", "M32", "M128", "G", "GA", "GF", "GA32")
BORN = {"M16": 16, "M32": 32, "M128": 128, "G": 16, "GA": 16, "GF": 16, "GA32": 8}
GROW = {"G": {8: 32, 16: 64, 24: 128}, "GA": {8: 32, 16: 64, 24: 128}, "GF": {8: 32, 16: 64, 24: 128},
        "GA32": {8: 16, 16: 32}}
MODE = {"G": "silent", "GA": "awake_in", "GF": "awake", "GA32": "awake_in"}
SCALE = 0.1                                      # a born neuron's starting scale (ws.Net)


def grow(net, new_n, mode):
    if mode == "silent":
        return net.grow(new_n)
    r, n, k = net.grow_rng, net.n, new_n - net.n
    net.p["Wx"] = np.vstack([net.p["Wx"], r.normal(0, SCALE, (k, ws.N_IN))])
    net.p["b"] = np.concatenate([net.p["b"], np.zeros(k)])
    Wh = np.zeros((new_n, new_n))
    Wh[:n, :n] = net.p["Wh"]
    Wh[n:, :] = r.normal(0, SCALE, (k, new_n))                     # into the new neurons, from all neurons
    if mode == "awake":
        Wh[:n, n:] = r.normal(0, SCALE, (n, k))                    # out of the new neurons into the old ones
        Mnew = r.normal(0, SCALE, (ws.ACTS, k))                    # out of the new neurons to the hands
    else:
        Mnew = np.zeros((ws.ACTS, k))
    net.p["Wh"] = Wh
    net.p["M"] = np.hstack([net.p["M"], Mnew])
    net.n = new_n


def run(brain, seed, out=None):
    t0 = time.process_time()
    home = ws.Home(seed)
    net = wn.Net(seed, BORN[brain], True)
    rng = np.random.default_rng([seed, 3, ws.BRAINS.index("Bm")])
    tests, show_tests, sizes = {}, {}, {}
    for d in range(1, ws.DAYS + 1):
        for k, look, rnd in home.day(d):
            prefix = []
            if d <= ws.DEMO_DAYS:
                prefix = ws.show_steps(look, home.pairs[k])
                ws.copy_step(net, look, home.pairs[k], prefix, wn.COPY_RATE)
            ws.try_box(net, look, home.pairs[k], prefix, rng, True)
        if d in wn.TEST_DAYS:
            tests[d] = ws.test(home, net, seed, d)
            sizes[d] = net.n
        if d in wn.SHOW_TEST_DAYS:
            show_tests[d] = ws.test(home, net, seed, d, showing=True)
        if d in GROW.get(brain, {}):
            grow(net, GROW[brain][d], MODE[brain])
    a = np.abs(net.p["M"])
    use = {"born": float(a[:, :BORN[brain]].mean()),
           "added": float(a[:, BORN[brain]:].mean()) if net.n > BORN[brain] else None}
    res = {"brain": brain, "seed": seed, "tests": tests, "show_tests": show_tests, "sizes": sizes,
           "out_weight_day60": use, "cpu_secs": round(time.process_time() - t0, 2)}
    if out is not None:
        out = Path(out)
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{brain}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    return res


if __name__ == "__main__":
    if sys.argv[1] == "one":
        r = run(sys.argv[2], int(sys.argv[3]), sys.argv[4])
        print(sys.argv[2], sys.argv[3], {d: round(v["success"], 2) for d, v in r["tests"].items()}, r["cpu_secs"])
