"""WS code checks (questions.md, Validity) -> checks.log.

  python checks_ws.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import ws  # noqa: E402

LINES = []


def say(name, ok, extra=""):
    LINES.append(f"{name}: {'PASS' if ok else 'FAIL'} {extra}".rstrip())
    print(LINES[-1], flush=True)
    return ok


def main():
    ok = True
    homes = [ws.Home(s) for s in range(1, 49)]
    ok &= say("each box's 2 lid pairs differ", all(len(set(h.pairs[k])) == 2 for h in homes for k in range(6)))
    # what each brain's network sees, and how it learns
    seen, applies = {}, {}
    orig_step, orig_apply = ws.Net.step, ws.Net.apply

    def spy_step(self, x, hprev):
        seen.setdefault(spy_step.brain, []).append(x.copy())
        return orig_step(self, x, hprev)

    def spy_apply(self, g, lr):
        applies.setdefault(spy_step.brain, []).append(lr)
        return orig_apply(self, g, lr)
    ws.Net.step, ws.Net.apply = spy_step, spy_apply
    runs = {}
    try:
        for b in ws.BRAINS:
            spy_step.brain = b
            runs[b] = ws.run(b, 3)
    finally:
        ws.Net.step, ws.Net.apply = orig_step, orig_apply
    show_idx = slice(ws.LOOK + ws.MAXL + ws.ACTS + 1, ws.N_IN)
    ff_ok = all(not np.any(x[show_idx]) for b in ("B0", "Bc", "Bu", "Br", "Bp", "Bx") for x in seen[b])
    ok &= say("non-memory brains never see a showing in their input", ff_ok)
    rec_ok = any(x[-1] == 1.0 for x in seen["Bm"]) and all(
        (x[-1] == 0.0) == (not np.any(x[ws.LOOK + ws.MAXL + ws.ACTS + 1:-1])) for x in seen["Bm"])
    ok &= say("Bm sees showings only as showing steps (flag set exactly when a shown act is fed)", rec_ok)
    ok &= say("Br and Brm replay 4 showings each night of days 1-30, the others none",
              runs["Br"]["replays"] == 120 and runs["Brm"]["replays"] == 120 and
              all(runs[b]["replays"] == 0 for b in ("B0", "Bc", "Bu", "Bm", "Bp", "Bx")))
    amount = {b: runs[b]["copies"] * ws.COPY[b] + runs[b]["replays"] * ws.REPLAY_RATE for b in ("Bu", "Br")}
    ok &= say("Bu's total copy amount equals Br's", abs(amount["Bu"] - amount["Br"]) < 1e-9,
              f"({amount['Bu']:.3f} vs {amount['Br']:.3f})")
    ok &= say("Bp never learns from reward (only copy-rate updates)",
              all(abs(lr - ws.LR * ws.COPY["Bp"]) < 1e-12 for lr in applies["Bp"]) and len(applies["Bp"]) == 540)
    h3 = ws.Home(3)
    diff = sum(1 for d in range(1, 31) for k, look, rnd in h3.day(d) if rnd != h3.pairs[k])
    ok &= say("Bx's showings are random (mostly not the right pairs)", diff > 400, f"({diff} of 540 differ)")
    # gradient check through time (a recurrent net with large weights)
    rng = np.random.default_rng(1)
    net = ws.Net(9, True)
    for k in net.p:
        net.p[k] = net.p[k] * 4
    xs = [rng.normal(0, 1, ws.N_IN) for _ in range(7)]
    targets = {2: (1, 0.7), 4: (3, -0.4), 6: (0, 1.0)}

    def loss():
        h, total = np.zeros(ws.HID), 0.0
        for t, x in enumerate(xs):
            h, z = net.step(x, h)
            if t in targets:
                a, sc = targets[t]
                total += -sc * np.log(ws.softmax(z)[a])
        return total
    hs, h = [], np.zeros(ws.HID)
    for x in xs:
        h, _ = net.step(x, h)
        hs.append(h)
    g = net.grads(xs, hs, targets)
    worst = 0.0
    for name, P in net.p.items():
        f, gf = P.reshape(-1), g[name].reshape(-1)
        for i in rng.choice(f.size, min(25, f.size), replace=False):
            o = f[i]
            f[i] = o + 1e-6
            lp = loss()
            f[i] = o - 1e-6
            lm = loss()
            f[i] = o
            num = (lp - lm) / 2e-6
            worst = max(worst, abs(num - gf[i]) / max(1e-3, abs(num) + abs(gf[i])))
    ok &= say("gradients through time equal finite differences", worst < 1e-5, f"(worst rel. {worst:.1e})")
    ok &= say("the same seed gives the same result twice", ws.run("Brm", 4) == ws.run("Brm", 4))
    LINES.append(f"All: {'PASS' if ok else 'FAIL'}")
    (HERE / "checks.log").write_text("\n".join(LINES) + "\n", encoding="utf-8")
    print(LINES[-1])


if __name__ == "__main__":
    main()
