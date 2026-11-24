"""Play Crafter lives with a player and score them the Crafter way (draft, exploratory until the plan is frozen).

  python play.py brain|sated|random5|random5s|random BUDGET [FIRST_SEED] [OUTDIR]
      lives on seeds FIRST_SEED, FIRST_SEED+1, ... until the total steps reach BUDGET (the crossing life is completed)
      -> OUTDIR/<player>.jsonl (one line per life; resumes from the lines already there) and a printed score

Crafter's score (Hafner 2021): each achievement's success rate s_i = the share of lives (episodes) in which it was
unlocked at least once, in percent; score = exp(mean_i ln(1 + s_i)) - 1 over the 22 achievements.
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import crafter

import bridge as BR

HERE = Path(__file__).parent
OUT = HERE / "output"


def first_info(env):
    p = env._player
    return {"semantic": env._sem_view(), "player_pos": p.pos, "inventory": dict(p.inventory)}


def life(env, player):
    env.reset()
    player.reset()
    info, done, steps, reward = first_info(env), False, 0, 0.0
    acts = {"move": 0, "do": 0, "sleep": 0, "other": 0}
    while not done:
        a = player.act(env, info)
        name = BR.ACTIONS[a]
        acts["move" if name.startswith("move_") else name if name in ("do", "sleep") else "other"] += 1
        _, r, done, info = env.step(a)
        player.after(env)
        steps += 1
        reward += r
    got = {k: v for k, v in info["achievements"].items() if v > 0}
    return {"steps": steps, "reward": round(reward, 2), "achievements": got, "actions": acts,
            "cells": len(player.visited),
            "death": "time" if steps >= env._length else "health"}


def score(recs):
    names = crafter.constants.achievements
    rates = np.array([100.0 * np.mean([n in r["achievements"] for r in recs]) for n in names])
    return float(np.exp(np.mean(np.log(1.0 + rates))) - 1.0), dict(zip(names, rates.round(1).tolist()))


def main():
    kind = sys.argv[1]
    budget = int(sys.argv[2])
    first = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    out = Path(sys.argv[4]) if len(sys.argv) > 4 else OUT
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{kind}.jsonl"
    recs = [json.loads(x) for x in open(path)] if path.exists() else []
    total = sum(r["steps"] for r in recs)
    s = first + len(recs)
    net = BR.load(str(HERE / "mbb_seed1.npz")) if kind in ("brain", "sated") else None
    make = {"brain": lambda r: BR.BrainPlayer(net, r), "sated": lambda r: BR.BrainPlayer(net, r, sated=True),
            "random5": lambda r: BR.RandomHandPlayer(r), "random5s": lambda r: BR.RandomHandPlayer(r, sated=True),
            "random": lambda r: BR.RandomPlayer(r)}[kind]
    while total < budget:
        env = crafter.Env(seed=s)
        rng = np.random.default_rng(s)
        player = make(rng)
        t0 = time.time()
        rec = life(env, player)
        rec.update(seed=s, seconds=round(time.time() - t0, 1))
        recs.append(rec)
        total += rec["steps"]
        with open(path, "a") as f:
            f.write(json.dumps(rec) + "\n")
        s += 1
    sc, rates = score(recs)
    print(f"{kind}: {len(recs)} lives, {total} steps, mean length {np.mean([r['steps'] for r in recs]):.0f}, "
          f"Crafter score {sc:.2f}%")
    print({k: v for k, v in rates.items() if v > 0})


if __name__ == "__main__":
    main()
