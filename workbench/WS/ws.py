"""WS: learning step-by-step skills fast (questions.md, WS-frozen).

Cradle C2-K's 2-lid boxes (6 kinds; 3 tries per kind per day; 60 days; one reliable demonstrator on days 1-30, shown
before each try and not in view during it). Brains: B0, Bc, Bu, Br (nightly replay of the last 4 showings), Bm (a
learned recurrent state carries the showing through the try), Brm (both), Bp (copy only), Bx (random showings).

One network class: h_t = tanh(Wx x_t + Wh h_(t-1) + b), act scores M h_t + c. Non-recurrent brains use h_(t-1) = 0
(Wh never used or learned), so each step stands alone, as C2's network.

  python ws.py one BRAIN SEED OUT_DIR
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

BRAINS = ("B0", "Bc", "Bu", "Br", "Bm", "Brm", "Bp", "Bx")
KINDS, LIDS, MAXL, ACTS, LOOK, HID = 6, 2, 3, 4, 16, 32
TRIES, DAYS, DEMO_DAYS = 3, 60, 30
N_IN = LOOK + MAXL + ACTS + 1 + ACTS + 1           # look, lid, own first act, step, shown act, showing flag = 29
LR, BASE_RATE, CLIP = 0.05, 0.01, 1.0
COPY = {"B0": 0.5, "Bc": 1.0, "Bu": 0.5 * (1 + 4 / 18), "Br": 0.5, "Bm": 0.5, "Brm": 0.5, "Bp": 0.5, "Bx": 0.5}
REPLAY_N, REPLAY_RATE = 4, 0.5
TEST_DAYS = [1, 2, 3, 5, 7, 10, 15, 30, 45, 60]
SHOW_TEST_DAYS = [30, 60]


def softmax(z):
    e = np.exp(z - z.max())
    return e / e.sum()


def oh(i, n):
    v = np.zeros(n)
    if i is not None:
        v[i] = 1.0
    return v


def x_try(look, lid, own_first, step):
    return np.concatenate([look, oh(lid, MAXL), oh(own_first, ACTS), [float(step)], np.zeros(ACTS), [0.0]])


def x_show(look, lid, shown_act):
    return np.concatenate([look, oh(lid, MAXL), np.zeros(ACTS), [0.0], oh(shown_act, ACTS), [1.0]])


def show_steps(look, pairs):
    """The showing as input steps: 2 per lid (its 2 acts)."""
    return [x_show(look, j, a) for j, pr in enumerate(pairs) for a in pr]


class Home:
    def __init__(self, seed):
        r = np.random.default_rng([seed, 1])
        self.looks = r.normal(0, 1, (KINDS, LOOK))
        self.pairs = []
        for k in range(KINDS):
            ps = r.permutation(ACTS * ACTS)[:LIDS]
            self.pairs.append([(int(p) // ACTS, int(p) % ACTS) for p in ps])
        self.seed = seed

    def day(self, d):
        """18 tries: (kind, look, random showing pairs for Bx); the same draws for every brain."""
        r = np.random.default_rng([self.seed, 2, d])
        out = []
        for k in np.tile(r.permutation(KINDS), TRIES):
            k = int(k)
            look = self.looks[k] + r.normal(0, 0.2, LOOK)
            rnd = [(int(p) // ACTS, int(p) % ACTS) for p in r.integers(0, ACTS * ACTS, LIDS)]
            out.append((k, look, rnd))
        return out


class Net:
    def __init__(self, seed, recurrent):
        r = np.random.default_rng([seed, 4])
        self.rec = recurrent
        self.p = {"Wx": r.normal(0, 0.1, (HID, N_IN)), "b": np.zeros(HID),
                  "Wh": r.normal(0, 0.1, (HID, HID)) if recurrent else np.zeros((HID, HID)),
                  "M": r.normal(0, 0.1, (ACTS, HID)), "c": np.zeros(ACTS)}
        self.base = 0.0

    def step(self, x, hprev):
        hp = hprev if self.rec else np.zeros(HID)
        h = np.tanh(self.p["Wx"] @ x + self.p["Wh"] @ hp + self.p["b"])
        return h, self.p["M"] @ h + self.p["c"]

    def grads(self, xs, hs, targets):
        """Gradient (to subtract) of sum_t scale_t * (-log pi(a_t | h_t)) over a sequence.
        xs, hs: the inputs and states (hs[t] after step t); targets: {t: (a, scale)}."""
        g = {k: np.zeros_like(v) for k, v in self.p.items()}
        dh_next = np.zeros(HID)
        for t in reversed(range(len(xs))):
            h = hs[t]
            dh = dh_next.copy() if self.rec else np.zeros(HID)
            if t in targets:
                a, scale = targets[t]
                dz = softmax(self.p["M"] @ h + self.p["c"])
                dz[a] -= 1.0
                dz *= scale
                g["M"] += np.outer(dz, h)
                g["c"] += dz
                dh += self.p["M"].T @ dz
            dpre = dh * (1.0 - h ** 2)
            g["Wx"] += np.outer(dpre, xs[t])
            g["b"] += dpre
            if self.rec:
                hp = hs[t - 1] if t > 0 else np.zeros(HID)
                g["Wh"] += np.outer(dpre, hp)
                dh_next = self.p["Wh"].T @ dpre
        return g

    def apply(self, g, lr):
        n = float(np.sqrt(sum(float((v * v).sum()) for v in g.values())))
        s = min(1.0, CLIP / n) if n > 0 else 1.0
        for k in self.p:
            if k == "Wh" and not self.rec:
                continue
            self.p[k] -= lr * s * g[k]


def run_prefix(net, prefix):
    h = np.zeros(HID)
    xs, hs = [], []
    for x in prefix:
        h, _ = net.step(x, h)
        xs.append(x)
        hs.append(h)
    return xs, hs, h


def try_box(net, look, pairs, prefix, rng, learn, reinforce=True):
    """Works the lids in order (a wrong lid ends the try). Returns (lids opened, the chosen pairs)."""
    xs, hs, h = run_prefix(net, prefix)
    targets, opened, chosen = {}, 0, []
    for j in range(LIDS):
        x1 = x_try(look, j, None, 0)
        h, z1 = net.step(x1, h)
        xs.append(x1)
        hs.append(h)
        a1 = int(rng.choice(ACTS, p=softmax(z1))) if learn else int(np.argmax(z1))
        t1 = len(xs) - 1
        x2 = x_try(look, j, a1, 1)
        h, z2 = net.step(x2, h)
        xs.append(x2)
        hs.append(h)
        a2 = int(rng.choice(ACTS, p=softmax(z2))) if learn else int(np.argmax(z2))
        t2 = len(xs) - 1
        ok = (a1, a2) == pairs[j]
        r = (1.0 / LIDS) if ok else 0.0
        chosen.append([a1, a2])
        if learn:
            adv = r - net.base
            net.base += BASE_RATE * (r - net.base)
            targets[t1] = (a1, adv)
            targets[t2] = (a2, adv)
        if not ok:
            break
        opened += 1
    if learn and reinforce and targets:
        net.apply(net.grads(xs, hs, targets), LR)
    return opened, chosen


def copy_step(net, look, shown, prefix, rate):
    """Cross-entropy toward the shown acts at the try steps (first act forced to the shown one), through the prefix."""
    xs, hs, h = run_prefix(net, prefix)
    targets = {}
    for j, (a1, a2) in enumerate(shown):
        for x, a in ((x_try(look, j, None, 0), a1), (x_try(look, j, a1, 1), a2)):
            h, _ = net.step(x, h)
            xs.append(x)
            hs.append(h)
            targets[len(xs) - 1] = (a, 1.0)
    net.apply(net.grads(xs, hs, targets), LR * rate)


def test(home, net, seed, d, showing=False):
    r = np.random.default_rng([seed, 6, d, int(showing)])
    full, part = [], []
    for k in range(KINDS):
        look = home.looks[k] + r.normal(0, 0.2, LOOK)
        prefix = show_steps(look, home.pairs[k]) if (showing and net.rec) else []
        op, _ = try_box(net, look, home.pairs[k], prefix, None, False)
        full.append(1.0 if op == LIDS else 0.0)
        part.append(op / LIDS)
    return {"success": float(np.mean(full)), "partial": float(np.mean(part))}


def run(brain, seed, out=None):
    home = Home(seed)
    rec = brain in ("Bm", "Brm")
    net = Net(seed, rec)
    rng = np.random.default_rng([seed, 3, BRAINS.index(brain)])
    store, replays, copies, tests, show_tests = [], 0, 0, {}, {}
    for d in range(1, DAYS + 1):
        for k, look, rnd in home.day(d):
            prefix = []
            if d <= DEMO_DAYS:
                shown = rnd if brain == "Bx" else home.pairs[k]
                prefix = show_steps(look, shown) if rec else []
                copy_step(net, look, shown, prefix, COPY[brain])
                copies += 1
                store = (store + [(look, shown)])[-REPLAY_N:]
            try_box(net, look, home.pairs[k], prefix, rng, True, reinforce=(brain != "Bp"))
        if d <= DEMO_DAYS and brain in ("Br", "Brm"):          # nightly replay of the last 4 showings
            for look_s, shown_s in store:
                copy_step(net, look_s, shown_s, show_steps(look_s, shown_s) if rec else [], REPLAY_RATE)
                replays += 1
        if d in TEST_DAYS:
            tests[d] = test(home, net, seed, d)
        if d in SHOW_TEST_DAYS:
            show_tests[d] = test(home, net, seed, d, showing=True)
    res = {"brain": brain, "seed": seed, "pairs": home.pairs, "tests": tests, "show_tests": show_tests,
           "copies": copies, "replays": replays}
    if out is not None:
        out = Path(out)
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{brain}_seed_{seed}.json").write_text(json.dumps(res), encoding="utf-8")
    return res


if __name__ == "__main__":
    if sys.argv[1] == "one":
        r = run(sys.argv[2], int(sys.argv[3]), sys.argv[4])
        print(sys.argv[2], sys.argv[3], {d: round(v["success"], 2) for d, v in r["tests"].items()}, flush=True)
