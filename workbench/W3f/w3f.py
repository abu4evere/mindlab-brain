"""W3f: choosing whom to learn from, over generations (questions.md, W3f-frozen). W3d's fading childhood plus the
recipe; in each life of its childhood the child meets 4 adults from a pool and copies one adult's argmax act: CH the
one with the highest visible success (mean lifespan on 5 demonstration lands), RN a random one of the same 4.

  python w3f.py pool ARM GEN             compute visible success for the pool of ARM's generation GEN -> pool_<ARM>_<GEN>.json
  python w3f.py run ARM GEN SEED [HOURS]  ARM in CH, RN; GEN in 1, 2, 3
Pools: generation 1 = W3e's G2 brains; generation k > 1 = the same arm's generation k-1 children.
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
sys.path.insert(0, str(HERE.parent / "W3e"))
import w3e  # noqa: E402
from w3e import w3b, w3d, B, W, R3  # noqa: E402

OUT = HERE / "output"
DEMO_LANDS = range(800001, 800006)
SEEDS = range(1, 9)
_S = {"arm": None, "gen": None, "seed": None, "adults": None, "vis": None}


def pool_paths(arm, gen):
    if gen == 1:
        return [HERE.parent / "W3e" / "output" / f"G2_{s}.npz" for s in SEEDS]
    return [OUT / f"{arm}{gen - 1}_{s}.npz" for s in SEEDS]


def visible_success(net):
    R = R3.regrowth()
    spans = []
    for ls in DEMO_LANDS:
        rng = np.random.default_rng(ls)
        _, m = R3.run_life(lambda w: net.act(w.obs_map(), R3.levels(w, "D3"), w.pos, rng)[0], W.make_land(ls), R, rng)
        spans.append(m["lifespan"])
    return float(np.mean(spans))


def make_pool(arm, gen):
    vis = [visible_success(w3e.load_net(p, i + 1)) for i, p in enumerate(pool_paths(arm, gen))]
    (HERE / f"pool_{arm}_{gen}.json").write_text(json.dumps({"visible": vis}))
    return vis


def choose(life):
    """The adult copied in this life: CH the most visibly successful of 4 met, RN a random one of the same 4."""
    met = np.random.default_rng([_S["seed"], 61, _S["gen"], life]).choice(len(_S["adults"]), 4, replace=False)
    if _S["arm"] == "CH":
        return int(met[int(np.argmax([_S["vis"][i] for i in met]))])
    return int(met[int(np.random.default_rng([_S["seed"], 62, _S["gen"], life]).integers(4))])


def adult_act(k, m, lev, cell):
    return _S["adults"][k].act(m, lev, cell, None, greedy=True)[0]


_src = textwrap.dedent(inspect.getsource(w3b.train_net))
_anchors = [
    ("        records, since_event, replays, events, wsum, off_shelter = deque(maxlen=WIN), 0, 0, 0, 0.0, 0\n",
     "        records, since_event, replays, events, wsum, off_shelter = deque(maxlen=WIN), 0, 0, 0, 0.0, 0\n"
     "        chosen = choose(life) if parent_present(total) else None\n"),
    ("            a, _, _ = net.act(m, lev, cell, rng)\n",
     "            a, _, _ = net.act(m, lev, cell, rng)\n"
     "            if parent_present(total) and chosen is not None:\n"
     "                wc_ = copy_weight(total)\n"
     "                if total % EVERY == 0 and wc_ > 0:\n"
     "                    pa = adult_act(chosen, m, lev, cell)\n"
     "                    imitate(net, [(m, lev, cell, pa)], [wc_])\n"
     "                    upd['copy'] = upd.get('copy', 0) + 1\n"
     "                    upd.setdefault('chosen', {})\n"
     "                    upd['chosen'][str(chosen)] = upd['chosen'].get(str(chosen), 0) + 1\n"),
    ("def train_net(", "def train_net_choose("),
]
for a, b in _anchors:
    assert _src.count(a) == 1, a
    _src = _src.replace(a, b)
_ns = dict(w3b.__dict__)
_ns.update(parent_present=w3d.parent_present, copy_weight=w3d.copy_weight, EVERY=w3d.EVERY, choose=choose,
           adult_act=adult_act, parts_of=lambda arm: "YR" if arm[:2] in ("CH", "RN") else w3b.parts_of(arm))
exec(compile(_src, "w3f_train_net", "exec"), _ns)
train_net_choose = _ns["train_net_choose"]


def configure(arm, gen, seed):
    w3d.CFG.update(child=w3d.CHILD, always=False)
    _S.update(arm=arm, gen=gen, seed=seed,
              adults=[w3e.load_net(p, i + 1) for i, p in enumerate(pool_paths(arm, gen))],
              vis=json.loads((HERE / f"pool_{arm}_{gen}.json").read_text())["visible"])
    w3b.OUT = OUT
    w3b.train_net = train_net_choose


if __name__ == "__main__":
    if sys.argv[1] == "pool":
        print(make_pool(sys.argv[2], int(sys.argv[3])))
    elif sys.argv[1] == "run":
        arm, gen, seed = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
        configure(arm, gen, seed)
        name = f"{arm}{gen}"
        if w3b.train(name, seed, float(sys.argv[5]) if len(sys.argv) > 5 else 4.5):
            w3b.test(name, seed)
            print("done", name, seed, flush=True)
