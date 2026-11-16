"""W3e: generations (questions.md, W3e-frozen). W3d's childhood (copy every 4th step, weight fading 0.5 -> 0 over the
first 400,000 steps) plus the recipe (Y + FR), with a learned parent: W3d's PYFR brain of the same seed (G2), or W3e's
G2 child of the same seed (G3). The parent is fixed and gives its argmax act on the child's own view.

  python w3e.py run GEN SEED [HOURS]     GEN in G2, G3 (train, resumable; then test alone and the fidelity measure)
"""
from __future__ import annotations

import inspect
import json
import os
import sys
import textwrap
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "W3d"))
import w3d  # noqa: E402  (W3b and W3 on the path)
from w3d import w3b, B, W, R3  # noqa: E402

OUT = HERE / "output"
PARENT_FILE = {"G2": lambda s: HERE.parent / "W3d" / "output" / f"PYFR_{s}.npz",
               "G3": lambda s: OUT / f"G2_{s}.npz"}
FID_LANDS, FID_EVERY = range(900001, 900011), 10
_P = {"net": None}


def load_net(path, seed):
    net = B.DriveVIN(seed, fixed_map=False)
    with np.load(path) as z:
        for k in net.p:
            net.p[k] = z[k].copy()
    return net


def parent_act(m, lev, cell):
    return _P["net"].act(m, lev, cell, None, greedy=True)[0]


_src = textwrap.dedent(inspect.getsource(w3b.train_net))
_anchors = [
    ("            a, _, _ = net.act(m, lev, cell, rng)\n",
     "            a, _, _ = net.act(m, lev, cell, rng)\n"
     "            if parent_present(total):\n"
     "                wc_ = copy_weight(total)\n"
     "                if total % EVERY == 0 and wc_ > 0:\n"
     "                    pa = parent_act(m, lev, cell)\n"
     "                    imitate(net, [(m, lev, cell, pa)], [wc_])\n"
     "                    upd['copy'] = upd.get('copy', 0) + 1\n"),
    ("def train_net(", "def train_net_gen("),
]
for a, b in _anchors:
    assert _src.count(a) == 1, a
    _src = _src.replace(a, b)
_ns = dict(w3b.__dict__)
_ns.update(parent_present=w3d.parent_present, copy_weight=w3d.copy_weight, EVERY=w3d.EVERY, parent_act=parent_act,
           parts_of=lambda arm: "YR" if arm in ("G2", "G3") else w3b.parts_of(arm))
exec(compile(_src, "w3e_train_net", "exec"), _ns)
train_net_gen = _ns["train_net_gen"]


def configure(gen, seed):
    w3d.CFG.update(child=w3d.CHILD, always=False)
    _P["net"] = load_net(PARENT_FILE[gen](seed), seed)
    w3b.OUT = OUT
    w3b.train_net = train_net_gen


def fidelity(child, parent, seed):
    """Argmax agreement of child and parent on states from the parent's own lives (test lands 900001-900010)."""
    R = R3.regrowth()
    states = []
    for ls in FID_LANDS:
        land = W.make_land(ls)
        rng = np.random.default_rng(ls)
        k = [0]

        def pol(w):
            m, lev = w.obs_map(), R3.levels(w, "D3")
            if k[0] % FID_EVERY == 0:
                states.append((m, lev, w.pos))
            k[0] += 1
            return parent.act(m, lev, w.pos, rng)[0]
        R3.run_life(pol, land, R, rng)
    agree = [child.act(m, lev, c, None, greedy=True)[0] == parent.act(m, lev, c, None, greedy=True)[0]
             for m, lev, c in states]
    return float(np.mean(agree)), len(states)


if __name__ == "__main__":
    if sys.argv[1] == "run":
        gen, seed = sys.argv[2], int(sys.argv[3])
        configure(gen, seed)
        if w3b.train(gen, seed, float(sys.argv[4]) if len(sys.argv) > 4 else 4.5):
            w3b.test(gen, seed)
            child = load_net(OUT / f"{gen}_{seed}.npz", seed)
            parent = _P["net"]
            d3 = load_net(HERE.parent / "W3" / "output" / f"D3_{seed}.npz", seed)
            fc, n = fidelity(child, parent, seed)
            fd, _ = fidelity(d3, parent, seed)
            (OUT / f"fid_{gen}_{seed}.json").write_text(json.dumps({"child": fc, "d3": fd, "n_states": n}))
            print("done", gen, seed, "fidelity", round(fc, 3), "d3", round(fd, 3), flush=True)
