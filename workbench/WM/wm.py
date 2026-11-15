"""WM: learning from mistakes (questions.md, WM-frozen). WC's changing world with single children; brain parts:
  SU   surprise: per-kind expectation e and surprise trace u; practice acts from softmax(z / (1 + 3u)); learning step
       x (1 + 4u)
  TB   don't repeat a failure: per kind and lid, the pairs that failed since the lid last opened are blocked in practice
  LSi  learned lose-shift: 10 more senses showing its own last try on this lid (acts and result)
  SUTB both SU and TB

  python wm.py arm ARM SIZE OUT_DIR      (seeds 1001-1048)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "WC"))
import wc  # noqa: E402
import wt  # noqa: E402
import wn  # noqa: E402
import ws  # noqa: E402

ARMS = ("Base", "SU", "TB", "LSi", "SUTB")
N_EXTRA = 10
Z_EXTRA = np.zeros(N_EXTRA)


def oh(i, n):
    v = np.zeros(n)
    if i is not None:
        v[i] = 1.0
    return v


def extra(last, k, j):
    """What the child senses of its own last try on kind k, lid j: acts tried (4 + 4) and result (opened, failed)."""
    if (k, j) not in last:
        return Z_EXTRA.copy()
    a1, a2, ok = last[(k, j)]
    return np.concatenate([oh(a1, ws.ACTS), oh(a2, ws.ACTS), [1.0 if ok else 0.0, 0.0 if ok else 1.0]])


def x_try(look, j, a1, step, ext):
    x = ws.x_try(look, j, a1, step)
    return x if ext is None else np.concatenate([x, ext[j]])


def show_steps(look, pairs, lsi):
    st = ws.show_steps(look, pairs)
    return [np.concatenate([s, Z_EXTRA]) for s in st] if lsi else st


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


def pick(z, rng, T, blocked):
    s = z / T
    if blocked:
        s = s.copy()
        s[list(blocked)] = -np.inf
    return int(rng.choice(ws.ACTS, p=ws.softmax(s)))


def try_box(net, look, pairs, prefix, rng, learn, T=1.0, tabu=None, ext=None, lrm=1.0):
    """ws.try_box with a temperature, blocked pairs (tabu: {lid: set of pairs}) and extra senses. With T = 1, no tabu
    and no extra senses it is ws.try_box exactly."""
    xs, hs, h = ws.run_prefix(net, prefix)
    targets, opened, chosen = {}, 0, []
    for j in range(ws.LIDS):
        x1 = x_try(look, j, None, 0, ext)
        h, z1 = net.step(x1, h)
        if learn:
            bl = {a for a in range(ws.ACTS) if tabu and all((a, b) in tabu[j] for b in range(ws.ACTS))} if tabu else set()
            a1 = pick(z1, rng, T, bl)
        else:
            a1 = int(np.argmax(z1))
        t1 = len(xs)
        xs.append(x1)
        hs.append(h)
        x2 = x_try(look, j, a1, 1, ext)
        h, z2 = net.step(x2, h)
        if learn:
            bl = {b for b in range(ws.ACTS) if (a1, b) in tabu[j]} if tabu else set()
            a2 = pick(z2, rng, T, bl)
        else:
            a2 = int(np.argmax(z2))
        t2 = len(xs)
        xs.append(x2)
        hs.append(h)
        ok = (a1, a2) == tuple(pairs[j])
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
        net.apply(net.grads(xs, hs, targets), ws.LR * lrm)
    return opened, chosen


def test(home, net, seed, d, old, last, lsi):
    r = np.random.default_rng([seed, 6, d, 0])
    succ, stale = [], []
    for k in range(ws.KINDS):
        look = home.looks[k] + r.normal(0, 0.2, ws.LOOK)
        ext = [extra(last, k, j) for j in range(ws.LIDS)] if lsi else None
        opened, chosen = try_box(net, look, home.pairs[k], [], None, False, ext=ext)
        succ.append(1.0 if opened == ws.LIDS else 0.0)
        stale.append((1.0 if tuple(chosen[0]) == tuple(old[k][0]) else 0.0) if wc.changed(k, d) else None)
    return {"success": succ, "stale": stale}


def make_net(seed, n, lsi):
    net = wn.Net(seed, n, True)
    if lsi:
        net.p["Wx"] = np.hstack([net.p["Wx"], np.random.default_rng([seed, 12]).normal(0, 0.1, (n, N_EXTRA))])
    return net


def run_child(arm, n, seed):
    su, tb, lsi = "SU" in arm, "TB" in arm, arm == "LSi"
    home = ws.Home(seed)
    old = [list(map(tuple, pr)) for pr in home.pairs]
    new = wc.new_codes(home, seed)
    net = make_net(seed, n, lsi)
    rng = np.random.default_rng([seed, 3, ws.BRAINS.index("Bm")])
    last, tabu = {}, {k: {j: set() for j in range(ws.LIDS)} for k in range(ws.KINDS)}
    e, u = np.zeros(ws.KINDS), np.zeros(ws.KINDS)
    food, tests, umax = 0, {}, 0.0
    for d in range(1, ws.DAYS + 1):
        if d in wc.CHANGE_DAY:
            for k in wc.CHANGE_DAY[d]:
                home.pairs[k] = list(new[k])
        here = wt.present(seed, d, wc.P)
        for i, (k, look, rnd) in enumerate(home.day(d)):
            ext = [extra(last, k, j) for j in range(ws.LIDS)] if lsi else None
            prefix = []
            if d <= ws.DEMO_DAYS and here[i]:
                prefix = show_steps(look, home.pairs[k], lsi)
                copy_step(net, look, home.pairs[k], prefix, wn.COPY_RATE, ext)
            T, lrm = (1.0 + 3.0 * u[k], 1.0 + 4.0 * u[k]) if su else (1.0, 1.0)
            opened, chosen = try_box(net, look, home.pairs[k], prefix, rng, True, T, tabu[k] if tb else None, ext, lrm)
            food += opened
            for j, (a1, a2) in enumerate(chosen):
                ok = j < opened
                last[(k, j)] = (a1, a2, ok)
                if ok:
                    tabu[k][j].clear()
                else:
                    tabu[k][j].add((a1, a2))
                    if len(tabu[k][j]) == ws.ACTS * ws.ACTS:      # correction 1: every pair failed -> search again
                        tabu[k][j].clear()
            if su:
                r = opened / ws.LIDS
                u[k] = 0.7 * u[k] + 0.3 * max(0.0, e[k] - r)
                e[k] += 0.2 * (r - e[k])
                umax = max(umax, float(u[k]))
        if d in wc.TEST_DAYS:
            tests[d] = test(home, net, seed, d, old, last, lsi)
    return {"arm": arm, "n": n, "seed": seed, "tests": tests, "food": food, "u_max": umax}


if __name__ == "__main__":
    if sys.argv[1] == "arm":
        arm, n, out = sys.argv[2], int(sys.argv[3]), Path(sys.argv[4])
        out.mkdir(parents=True, exist_ok=True)
        for s in range(1001, 1049):
            (out / f"{arm}{n}_seed_{s}.json").write_text(json.dumps(run_child(arm, n, s)), encoding="utf-8")
        print("done", arm, n, flush=True)
