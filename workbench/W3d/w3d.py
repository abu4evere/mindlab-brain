"""W3d: learning to live from a parent (questions.md, W3d-frozen). W3b's training loop with one addition: while the
parent is present, every 4th step the child takes one supervised copy step (W3b's imitate) toward what a W3 Script
would do in the child's own situation (it sees only the child's map view).

  python w3d.py run ARM SEED [HOURS]     ARM in P, PYFR, PA (train, resumable; then test alone)
"""
from __future__ import annotations

import inspect
import sys
import textwrap
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "W3b"))
import w3b  # noqa: E402
from w3b import B, W, R3  # noqa: E402

OUT = HERE / "output"
CHILD, EVERY, W_COPY = 400_000, 4, 0.5
ARMS = {"P": {"parts": "", "always": False}, "PYFR": {"parts": "YR", "always": False},
        "PA": {"parts": "", "always": True}}
CFG = {"child": CHILD, "always": False}


def copy_weight(total):
    """The parent's copy weight at training step `total` (0 when absent)."""
    if CFG["always"]:
        return W_COPY
    if total < CFG["child"]:
        return W_COPY * (1.0 - total / CFG["child"])
    return 0.0


def parent_present(total):
    return CFG["always"] or total < CFG["child"]


# W3b's train_net, with the parent's teaching inserted at three anchors (checked to be present)
_src = textwrap.dedent(inspect.getsource(w3b.train_net))
_anchors = [
    ("        records, since_event, replays, events, wsum, off_shelter = deque(maxlen=WIN), 0, 0, 0, 0.0, 0\n",
     "        records, since_event, replays, events, wsum, off_shelter = deque(maxlen=WIN), 0, 0, 0, 0.0, 0\n"
     "        parent = W.Script()\n"),
    ("            a, _, _ = net.act(m, lev, cell, rng)\n",
     "            a, _, _ = net.act(m, lev, cell, rng)\n"
     "            if parent_present(total):\n"
     "                pa = parent.act(W.MapView(w))\n"
     "                wc_ = copy_weight(total)\n"
     "                if total % EVERY == 0 and wc_ > 0:\n"
     "                    imitate(net, [(m, lev, cell, pa)], [wc_])\n"
     "                    upd['copy'] = upd.get('copy', 0) + 1\n"),
    ("def train_net(", "def train_net_parent("),
]
for a, b in _anchors:
    assert _src.count(a) == 1, a
    _src = _src.replace(a, b)
_ns = dict(w3b.__dict__)
_ns.update(parent_present=parent_present, copy_weight=copy_weight, EVERY=EVERY,
           parts_of=lambda arm: ARMS[arm]["parts"] if arm in ARMS else w3b.parts_of(arm))
exec(compile(_src, "w3d_train_net", "exec"), _ns)
train_net_parent = _ns["train_net_parent"]


def configure(arm):
    CFG.update(child=CHILD, always=ARMS[arm]["always"])
    w3b.OUT = OUT
    parts = {a: v["parts"] for a, v in ARMS.items()}
    orig = w3b.parts_of
    w3b.parts_of = lambda a: parts[a] if a in parts else orig(a)
    w3b.train_net = train_net_parent                       # w3b.train() calls train_net by module global


if __name__ == "__main__":
    if sys.argv[1] == "run":
        arm, seed = sys.argv[2], int(sys.argv[3])
        configure(arm)
        if w3b.train(arm, seed, float(sys.argv[4]) if len(sys.argv) > 4 else 4.5):
            w3b.test(arm, seed)
            print("done", arm, seed, flush=True)
