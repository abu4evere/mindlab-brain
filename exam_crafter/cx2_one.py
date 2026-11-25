"""One CX2 life in a fresh process (for checks_cx2.py): python cx2_one.py ARM SEED PERM_SEED|none -> JSON on stdout."""
import json
import sys

import numpy as np
import crafter

import bridge as BR
import play as P
import cx2

arm, seed, ps = sys.argv[1], int(sys.argv[2]), sys.argv[3]
perm = None if ps == "none" else np.random.default_rng(int(ps)).permutation(len(BR.SEM))
net = BR.load("mbb_seed1.npz") if arm != "random5p" else None
pl = cx2.LearnPlayer(net, np.random.default_rng(seed), arm, perm=perm)
acts, orig = [], pl.act


def act(e, i):
    a = orig(e, i)
    acts.append(int(a))
    return a


pl.act = act
r = P.life(crafter.Env(seed=seed), pl)
r.update(pl.extra())
r["acts"] = acts
print(json.dumps(r))
