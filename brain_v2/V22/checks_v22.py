"""V2-2's checks before data (questions.md, "Checks before data"; all must pass).
  1 exact zero check: new weights at 0 -> GOAL, GOAL-NOFLOOR, SHAM-GOAL and FT-NOGOAL walkers live CW2's NO-GUIDE life
    step for step (RMS seeds 1-2, lands 950001-950002; action, position, energy, fatigue)
  2 fine-tuning with learning rate 0 changes no parameter
  3 the reward is the drive reward unchanged (R3.reward, kind D3: the code calls nothing else)
  4 no goal from the untried bonus (a model with nothing experienced gives no target)
  5 the sham place is never a cell of the goal look (instrumented SHAM-GOAL lives)
  6 resuming from a checkpoint is deterministic (two resumes from the same checkpoint give identical parameters)
  7 determinism (the same short fine-tuning twice gives identical parameters)
  python checks_v22.py
"""
from __future__ import annotations

import inspect
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import v22  # noqa: E402
import numpy as np  # noqa: E402
from v22 import cw2, w3k, B  # noqa: E402

OK = []


def check(name, cond, detail=""):
    OK.append(bool(cond))
    print(f"{name}: {'PASS' if cond else 'FAIL'} {detail}", flush=True)


def traj():
    rec = []
    return rec, (lambda w, a, d0, cur: rec.append((int(a), tuple(w.pos), float(w.E), float(w.F))))


def zero_check():
    for s in (1, 2):
        rms = w3k.load_npz(v22.BRAINS / f"RM_CS_{s}.npz", s)
        for ls in (950001, 950002):
            cw2.configure("NO-GUIDE", s)
            ref, f = traj()
            cw2.life(rms, s, ls, "NO-GUIDE", on_step=f)
            for arm in ("GOAL", "GOAL-NOFLOOR", "SHAM-GOAL", "FT-NOGOAL"):
                v22.configure(s)
                got, f = traj()
                _, m = v22.life(v22.goalvin_from_rms(s), s, ls, arm, on_step=f)
                check(f"1 zero check seed {s} land {ls} {arm}", got == ref,
                      f"({len(ref)} steps; goal starts {m['goal_starts']})")


def lr_zero():
    keep = B.LR
    B.LR = 0.0
    try:
        v22.OUT = HERE / "output_checks"
        shutil.rmtree(v22.OUT, ignore_errors=True)
        v22.train("GOAL", 2, 2000, "_lr0")
        start = v22.goalvin_from_rms(2)
        with np.load(v22.OUT / "net_GOAL_2_lr0.npz") as z:
            same = all(np.array_equal(z[k], start.p[k]) for k in start.p)
        check("2 fine-tuning with learning rate 0 changes nothing", same)
    finally:
        B.LR = keep


def reward_unchanged():
    src = inspect.getsource(v22)
    calls = src.count("R3.reward(")
    check("3 the reward is R3.reward('D3', ...) only (one call, kind D3)", calls == 1 and 'R3.reward("D3"' in src)


def no_bonus_goal():
    m = cw2.Model(4, np.random.default_rng(0))
    m.u_seen |= {1, 2, 7}
    for u, c in ((1, (1, 1)), (2, (5, 5)), (7, (9, 9))):
        m.feel(u, c)
    check("4 no goal with nothing experienced", v22.best_target(m, (1, 2), 0) == (None, 0.0))


def sham_rule():
    bad = {"n": 0, "starts": 0}
    orig = v22.Goal.update

    def spy(self, w, model, h, u):
        before = self.cell
        orig(self, w, model, h, u)
        if self.cell is not None and self.cell != before:
            bad["starts"] += 1
            bad["n"] += self.cell in model.places.get(self.look, set())
    v22.Goal.update = spy
    try:
        for ls in (950001, 950002, 950003):
            v22.configure(2)
            v22.life(v22.goalvin_from_rms(2), 2, ls, "SHAM-GOAL")
    finally:
        v22.Goal.update = orig
    check("5 the sham place is never a goal-look cell", bad["n"] == 0 and bad["starts"] > 0,
          f"{bad['starts']} sham goals")


def resume_and_determinism():
    v22.OUT = HERE / "output_checks"
    v22.CKPT_EVERY = 1000
    v22.train("GOAL", 2, 1500, "_ck")                    # writes a checkpoint at the end of its run
    ck = v22.OUT / "ckpt_GOAL_2_ck.pkl"
    saved = ck.read_bytes()
    v22.train("GOAL", 2, 4500, "_ck")
    with np.load(v22.OUT / "net_GOAL_2_ck.npz") as z:
        a = {k: z[k].copy() for k in z.files}
    ck.write_bytes(saved)
    v22.train("GOAL", 2, 4500, "_ck")
    with np.load(v22.OUT / "net_GOAL_2_ck.npz") as z:
        b = {k: z[k].copy() for k in z.files}
    check("6 two resumes from the same checkpoint give identical parameters", all(np.array_equal(a[k], b[k]) for k in a))
    for tag in ("_d1", "_d2"):
        v22.train("GOAL", 2, 2000, tag)
    with np.load(v22.OUT / "net_GOAL_2_d1.npz") as z1, np.load(v22.OUT / "net_GOAL_2_d2.npz") as z2:
        same = all(np.array_equal(z1[k], z2[k]) for k in z1.files)
    moved = not np.array_equal(np.load(v22.OUT / "net_GOAL_2_d1.npz")["Wo"], v22.goalvin_from_rms(2).p["Wo"])
    check("7 the same fine-tuning twice gives identical parameters (and learning moves them)", same and moved)


if __name__ == "__main__":
    reward_unchanged()
    no_bonus_goal()
    zero_check()
    sham_rule()
    lr_zero()
    resume_and_determinism()
    print("All:", "PASS" if all(OK) else "FAIL", f"({sum(OK)}/{len(OK)})")
