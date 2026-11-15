"""WF: a fast memory beside the slow habit (questions.md, WF-frozen). WC's changing world; arms Base and TBYS (WY's
code), TBYS+RP (nightly replay from the store), TBYS+FMin (the store as 9 more senses), WSLS (engineered ceiling: a
fresh stored pair is done; otherwise the network with TB's blocking).

  python wf.py arm ARM SIZE OUT_DIR      (ARM: Base | TBYS | RP | FMin | WSLS; seeds 1001-1048)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "WY"))
import wy  # noqa: E402
import wm  # noqa: E402
import wc  # noqa: E402
import wt  # noqa: E402
import wn  # noqa: E402
import ws  # noqa: E402

ARMS = ("Base", "TBYS", "RP", "FMin", "WSLS")
N_FM = 9
RP_STEPS, RP_RATE = 2, 1.0


def oh(i, n):
    v = np.zeros(n)
    v[i] = 1.0
    return v


def fm_sense(store, k, j):
    if (k, j) not in store:
        return np.zeros(N_FM)
    (a1, a2), fresh = store[(k, j)]
    return np.concatenate([oh(a1, ws.ACTS), oh(a2, ws.ACTS), [1.0 if fresh else 0.0]])


def x_try(look, j, a1, step, ext):
    x = ws.x_try(look, j, a1, step)
    return x if ext is None else np.concatenate([x, ext[j]])


def pad(steps, ext):
    return steps if ext is None else [np.concatenate([s, np.zeros(N_FM)]) for s in steps]


def copy_step(net, look, shown, prefix, rate, ext):
    xs, hs, h = ws.run_prefix(net, prefix)
    targets = {}
    for j, (a1, a2) in enumerate(shown):
        for x, a in ((x_try(look, j, None, 0, ext), a1), (x_try(look, j, a1, 1, ext), a2)):
            h, _ = net.step(x, h)
            xs.append(x)
            hs.append(h)
            targets[len(xs) - 1] = (a, 1.0)
    net.apply(net.grads(xs, hs, targets), ws.LR * rate)


def try_box(net, look, code, prefix, rng, learn, tabu=None, ext=None, force=None):
    """wm.try_box with extra senses and forced pairs (force: {lid: pair}). Forced acts are learned like chosen ones."""
    xs, hs, h = ws.run_prefix(net, prefix)
    targets, opened, chosen = {}, 0, []
    for j in range(ws.LIDS):
        f = (force or {}).get(j)
        x1 = x_try(look, j, None, 0, ext)
        h, z1 = net.step(x1, h)
        if f is not None:
            a1 = f[0]
        elif learn:
            bl = {a for a in range(ws.ACTS) if all((a, b) in tabu[j] for b in range(ws.ACTS))} if tabu else set()
            a1 = wm.pick(z1, rng, 1.0, bl)
        else:
            a1 = int(np.argmax(z1))
        t1 = len(xs)
        xs.append(x1)
        hs.append(h)
        x2 = x_try(look, j, a1, 1, ext)
        h, z2 = net.step(x2, h)
        if f is not None:
            a2 = f[1]
        elif learn:
            bl = {b for b in range(ws.ACTS) if (a1, b) in tabu[j]} if tabu else set()
            a2 = wm.pick(z2, rng, 1.0, bl)
        else:
            a2 = int(np.argmax(z2))
        t2 = len(xs)
        xs.append(x2)
        hs.append(h)
        ok = (a1, a2) == tuple(code[j])
        r = (1.0 / ws.LIDS) if ok else 0.0
        chosen.append([a1, a2])
        if learn:
            adv = r - net.base
            net.base += ws.BASE_RATE * (r - net.base)
            targets[t1] = (a1, adv)
            targets[t2] = (a2, adv)
        if not ok:
            break
        opened += 1
    if learn and targets:
        net.apply(net.grads(xs, hs, targets), ws.LR)
    return opened, chosen


def self_copy(net, look, chosen, weights, prefix, ext):
    xs, hs, h = ws.run_prefix(net, prefix)
    targets = {}
    for j, w in enumerate(weights):
        a1, a2 = chosen[j]
        for x, a in ((x_try(look, j, None, 0, ext), a1), (x_try(look, j, a1, 1, ext), a2)):
            h, _ = net.step(x, h)
            xs.append(x)
            hs.append(h)
            targets[len(xs) - 1] = (a, w)
    net.apply(net.grads(xs, hs, targets), ws.LR * wy.YS_RATE)


def forced(store, k):
    return {j: store[(k, j)][0] for j in range(ws.LIDS) if (k, j) in store and store[(k, j)][1]}


def test(home, net, seed, d, old, store, arm):
    r = np.random.default_rng([seed, 6, d, 0])
    succ, stale = [], []
    for k in range(ws.KINDS):
        look = home.looks[k] + r.normal(0, 0.2, ws.LOOK)
        ext = [fm_sense(store, k, j) for j in range(ws.LIDS)] if arm == "FMin" else None
        force = forced(store, k) if arm == "WSLS" else None
        opened, chosen = try_box(net, look, home.pairs[k], [], None, False, ext=ext, force=force)
        succ.append(1.0 if opened == ws.LIDS else 0.0)
        stale.append((1.0 if tuple(chosen[0]) == tuple(old[k][0]) else 0.0) if wc.changed(k, d) else None)
    return {"success": succ, "stale": stale}


def run_child(arm, n, seed):
    if arm in ("Base", "TBYS"):
        return wy.run_child(arm, n, seed)
    fm = arm == "FMin"
    home = ws.Home(seed)
    old = [list(map(tuple, pr)) for pr in home.pairs]
    new = wc.new_codes(home, seed)
    net = wn.Net(seed, n, True)
    if fm:
        net.p["Wx"] = np.hstack([net.p["Wx"], np.random.default_rng([seed, 16]).normal(0, 0.1, (n, N_FM))])
    rng = np.random.default_rng([seed, 3, ws.BRAINS.index("Bm")])
    tabu = {k: {j: set() for j in range(ws.LIDS)} for k in range(ws.KINDS)}
    y = np.zeros((ws.KINDS, ws.LIDS))
    store, food, tests, replays = {}, 0, {}, 0
    for d in range(1, ws.DAYS + 1):
        if d in wc.CHANGE_DAY:
            for k in wc.CHANGE_DAY[d]:
                home.pairs[k] = list(new[k])
        here = wt.present(seed, d, wc.P)
        for i, (k, look, rnd) in enumerate(home.day(d)):
            ext = [fm_sense(store, k, j) for j in range(ws.LIDS)] if fm else None
            prefix = []
            if d <= ws.DEMO_DAYS and here[i]:
                prefix = pad(ws.show_steps(look, home.pairs[k]), ext)
                copy_step(net, look, home.pairs[k], prefix, wn.COPY_RATE, ext)
            force = forced(store, k) if arm == "WSLS" else None
            opened, chosen = try_box(net, look, home.pairs[k], prefix, rng, True, tabu[k], ext, force)
            food += opened
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
                self_copy(net, look, chosen, weights, prefix, ext)
        if arm == "RP":                                         # nightly replay from the store
            for k in range(ws.KINDS):
                pairs = []
                for j in range(ws.LIDS):
                    if (k, j) in store and store[(k, j)][1]:
                        pairs.append(store[(k, j)][0])
                    else:
                        break
                if pairs:
                    for _ in range(RP_STEPS):
                        ws.copy_step(net, home.looks[k], pairs, [], RP_RATE)
                        replays += 1
        if d in wc.TEST_DAYS:
            tests[d] = test(home, net, seed, d, old, store, arm)
    return {"arm": arm, "n": n, "seed": seed, "tests": tests, "food": food, "replays": replays}


if __name__ == "__main__":
    if sys.argv[1] == "arm":
        arm, n, out = sys.argv[2], int(sys.argv[3]), Path(sys.argv[4])
        out.mkdir(parents=True, exist_ok=True)
        for s in range(1001, 1049):
            (out / f"{arm}{n}_seed_{s}.json").write_text(json.dumps(run_child(arm, n, s)), encoding="utf-8")
        print("done", arm, n, flush=True)
