"""WD: the doubting test (questions.md, WD-frozen). WS's boxes with codes that never change; a teacher present with
p = 0.5 on days 1-30 who is wrong on kinds 0-2 (a fixed wrong code, WC's new-code draw) and right on kinds 3-5. The
brain is WR's recipe (LTYR). Arms: Naive (copies every showing), Doubt (copy rate 0.5 x trust; trust from checked
results), Alone (never copies).

  python wd.py arm ARM SIZE OUT_DIR      (seeds 1-48)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "WR"))
import wr  # noqa: E402  (imports wf, wy, wc, wt, wn, ws)
import wf  # noqa: E402
import wy  # noqa: E402
import wc  # noqa: E402
import wt  # noqa: E402
import wn  # noqa: E402
import ws  # noqa: E402

ARMS = ("Naive", "Doubt", "Alone")
BAD, GOOD = (0, 1, 2), (3, 4, 5)
TEST_DAYS = (15, 30, 45, 60)
TRUST_STEP = 0.3


def test(home, net, seed, d, wrong):
    r = np.random.default_rng([seed, 6, d, 0])
    succ, believe = [], []
    for k in range(ws.KINDS):
        look = home.looks[k] + r.normal(0, 0.2, ws.LOOK)
        opened, chosen = wf.try_box(net, look, home.pairs[k], [], None, False)
        succ.append(1.0 if opened == ws.LIDS else 0.0)
        believe.append((1.0 if tuple(chosen[0]) == tuple(wrong[k][0]) else 0.0) if k in BAD else None)
    return {"success": succ, "believe": believe}


def trust_updates(chosen, opened, shown):
    """The outcomes o for the trust update (questions.md): per lid tried."""
    out = []
    for j, (a1, a2) in enumerate(chosen):
        ok = j < opened
        if (a1, a2) == tuple(shown[j]):
            out.append(1.0 if ok else 0.0)
        elif ok:
            out.append(0.0)
    return out


def run_child(arm, n, seed):
    home = ws.Home(seed)
    wrong = wc.new_codes(home, seed)
    net = wn.Net(seed, n, True)
    rng = np.random.default_rng([seed, 3, ws.BRAINS.index("Bm")])
    tabu = {k: {j: set() for j in range(ws.LIDS)} for k in range(ws.KINDS)}
    y = np.zeros((ws.KINDS, ws.LIDS))
    trust = np.ones(ws.KINDS)
    store, food, tests, trust30 = {}, 0, {}, None
    for d in range(1, ws.DAYS + 1):
        here = wt.present(seed, d, wc.P)
        for i, (k, look, rnd) in enumerate(home.day(d)):
            teacher = d <= ws.DEMO_DAYS and here[i]
            shown = [tuple(p) for p in (wrong[k] if k in BAD else home.pairs[k])]
            if teacher and arm != "Alone":
                rate = wn.COPY_RATE * (trust[k] if arm == "Doubt" else 1.0)
                if rate > 0:
                    ws.copy_step(net, look, shown, [], rate)                      # L: no showing in mind
            opened, chosen = wf.try_box(net, look, home.pairs[k], [], rng, True, tabu[k])
            food += opened
            if teacher and arm == "Doubt":
                for o in trust_updates(chosen, opened, shown):
                    trust[k] += TRUST_STEP * (o - trust[k])
            weights = []
            for j, (a1, a2) in enumerate(chosen):
                ok = j < opened
                if ok:
                    weights.append(1.0 - y[k, j])
                    tabu[k][j].clear()
                    store[(k, j)] = ((a1, a2), True)
                else:
                    tabu[k][j].add((a1, a2))
                    if len(tabu[k][j]) == ws.ACTS * ws.ACTS:
                        tabu[k][j].clear()
                    if (k, j) in store and store[(k, j)][0] == (a1, a2):
                        store[(k, j)] = (store[(k, j)][0], False)
                y[k, j] += wy.Y_STEP * ((1.0 if ok else 0.0) - y[k, j])
            if weights and max(weights) > 0:
                wy.self_copy(net, look, chosen, weights, [])
        for k in range(ws.KINDS):                                              # R: nightly replay
            pairs = []
            for j in range(ws.LIDS):
                if (k, j) in store and store[(k, j)][1]:
                    pairs.append(store[(k, j)][0])
                else:
                    break
            if pairs:
                for _ in range(wf.RP_STEPS):
                    ws.copy_step(net, home.looks[k], pairs, [], wf.RP_RATE)
        if d in TEST_DAYS:
            tests[d] = test(home, net, seed, d, wrong)
        if d == 30:
            trust30 = trust.tolist()
    return {"arm": arm, "n": n, "seed": seed, "tests": tests, "food": food, "trust30": trust30}


if __name__ == "__main__":
    if sys.argv[1] == "arm":
        arm, n, out = sys.argv[2], int(sys.argv[3]), Path(sys.argv[4])
        out.mkdir(parents=True, exist_ok=True)
        for s in range(1, 49):
            (out / f"{arm}_{n}_seed_{s}.json").write_text(json.dumps(run_child(arm, n, s)), encoding="utf-8")
        print("done", arm, n, flush=True)
