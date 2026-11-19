"""W3l: the longer childhood with the kept copy, and longer still (questions.md, W3l-frozen).

W3k's code, unchanged, with two differences set from here:
  - runs "C3" (W3k's: 5.2M steps, 3.6M fade) and "C5" (6.4M steps, 4.8M fade) both save the copy kept by W3k's
    own-lives rule (CS) and the copy at a step drawn in advance (CY, new draw seed). W3k saved them for run "R" only.
  - outputs go to W3l/output.
Training is W3k's: the copies only read the brain, so C3 here must equal W3k's C3 bit for bit.

  python w3l.py run RUN SEED [HOURS]     RUN in C3, C5 (train in stages, resumable; then the tests)
"""
from __future__ import annotations

import inspect
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "W3k"))
import w3k  # noqa: E402  (sets the numerical environment before numpy loads; amendments 1 and 2 of W3k)

OUT = HERE / "output"
w3k.OUT = OUT
w3k.RUNS["C5"] = {"steps": 6_400_000, "fade": 4_800_000}
w3k.CY_SEED = 20261191                      # a new draw for this study's CY steps
RUNS = ("C3", "C5")

# W3k's train_staged saves the copies for run "R" only; here, for every run (the one change, checked to be present)
_src = inspect.getsource(w3k.train_staged)
_old = '                if run == "R":\n'
assert _src.count(_old) == 1
_src = _src.replace(_old, "                if True:   # W3l: the copies of every run\n")
_src = _src.replace("def train_staged(", "def train_staged_w3l(")
exec(compile(_src, "w3l_train_staged", "exec"), w3k.__dict__)
train_staged = w3k.train_staged_w3l


def configure(run, seed):
    w3k.configure(run, seed)
    w3k.CFG["cy_step"] = w3k.cy_step_for(seed, run)      # W3k drew a CY step for run "R" only


def run(run_name, seed, hours):
    if not w3k.right_machine():
        return
    configure(run_name, seed)
    w3k.machine(run_name, seed)
    if train_staged(run_name, seed, hours):
        snap = w3k.load_npz(OUT / f"{w3k.tag_of(run_name, seed, w3k.RUNS[run_name]['fade'])}.npz", seed)
        w3k.test_brain(f"{run_name}_{seed}", OUT / f"{run_name}_{seed}.npz", seed, snap)
        w3k.test_brain(f"{run_name}S_{seed}", OUT / f"{run_name}_CS_{seed}.npz", seed, snap)
        w3k.test_brain(f"{run_name}Y_{seed}", OUT / f"{run_name}_CY_{seed}.npz", seed, snap)
        print("done", run_name, seed, flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "run":
        assert sys.argv[2] in RUNS, sys.argv[2]
        run(sys.argv[2], int(sys.argv[3]), float(sys.argv[4]) if len(sys.argv) > 4 else 4.5)
