"""WL4: forgetting when things follow a rule (questions.md, WL4-frozen). 30 kinds (24 practised, 6 held out); RULE
world (codes from arg-maxes of the look) and RAND world (random codes); WL2's arms L0, L2, Linf.

  python wl4.py arm WORLD ARM SIZE OUT_DIR      (seeds 1-24)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "WL2"))
import wl2  # noqa: E402  (wait-aware prefix runner, episodes, Net)
import wn  # noqa: E402
import ws  # noqa: E402

N_KINDS, N_PRACTISED = 30, 24
WORLDS, ARMS = ("RULE", "RAND"), ("L0", "L2", "Linf")
TEST_DAYS = (15, 30, 60)


def rule_code(look):
    a = lambda s: int(np.argmax(look[s:s + 4]))
    return [(a(0), a(4)), (a(8), a(12))]


class Home:
    """WS's Home arithmetic over the 24 practised kinds; looks and codes for all 30 kinds."""
    def __init__(self, seed, world):
        r = np.random.default_rng([seed, 31])
        self.looks = r.normal(0, 1, (N_KINDS, ws.LOOK))
        rand = []
        for _ in range(N_KINDS):
            ps = r.permutation(ws.ACTS * ws.ACTS)[:ws.LIDS]
            rand.append([(int(p) // ws.ACTS, int(p) % ws.ACTS) for p in ps])
        self.pairs = [rule_code(l) for l in self.looks] if world == "RULE" else rand
        self.seed = seed

    def day(self, d):
        r = np.random.default_rng([self.seed, 2, d])
        out = []
        for k in np.tile(r.permutation(N_PRACTISED), ws.TRIES):
            k = int(k)
            out.append((k, self.looks[k] + r.normal(0, 0.2, ws.LOOK)))
        return out


def test(home, net, seed, d):
    r = np.random.default_rng([seed, 6, d, 0])
    full = []
    for k in range(N_KINDS):
        look = home.looks[k] + r.normal(0, 0.2, ws.LOOK)
        full.append(1.0 if ws.try_box(net, look, home.pairs[k], [], None, False)[0] == ws.LIDS else 0.0)
    return {"practised": float(np.mean(full[:N_PRACTISED])), "heldout": float(np.mean(full[N_PRACTISED:]))}


def run_child(world, arm, n, seed):
    home = Home(seed, world)
    net = wl2.Net(seed, n, True)
    rng = np.random.default_rng([seed, 3, ws.BRAINS.index("Bm")])
    nrng = np.random.default_rng([seed, 13])
    tests, food = {}, 0
    for d in range(1, ws.DAYS + 1):
        for k, look in home.day(d):
            prefix = []
            if d <= ws.DEMO_DAYS:
                prefix = wl2.episode(arm, look, home.pairs[k], n, nrng)
                ws.copy_step(net, look, home.pairs[k], prefix, wn.COPY_RATE)
            food += ws.try_box(net, look, home.pairs[k], prefix, rng, True)[0]
        if d in TEST_DAYS:
            tests[d] = test(home, net, seed, d)
    return {"world": world, "arm": arm, "n": n, "seed": seed, "tests": tests, "food": food}


if __name__ == "__main__":
    if sys.argv[1] == "arm":
        world, arm, n, out = sys.argv[2], sys.argv[3], int(sys.argv[4]), Path(sys.argv[5])
        out.mkdir(parents=True, exist_ok=True)
        for s in range(1, 25):
            (out / f"{world}_{arm}_{n}_seed_{s}.json").write_text(json.dumps(run_child(world, arm, n, s)), encoding="utf-8")
        print("done", world, arm, n, flush=True)
