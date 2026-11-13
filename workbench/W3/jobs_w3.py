"""W3's job queue: the reference brains, then 32 training runs (D3, D2, Dc, D3i x seeds 1-8, 2,000,000 steps each;
IMPLEMENTATION.md: the frozen 2,000,000 steps, restored by the creator), each followed by its test (and the D3- lesion test for D3). At most 4 at
once, at Idle priority. Resumable: a run whose test file exists is skipped.

  python jobs_w3.py
"""
from __future__ import annotations

import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "output"
STEPS = 2_000_000
WORKERS = 4
IDLE = 0x00000040                                     # IDLE_PRIORITY_CLASS (Windows)
LOG = HERE / "jobs.log"


def sh(args):
    return subprocess.call([sys.executable, str(HERE / "run_w3.py"), *args], creationflags=IDLE)


def note(msg):
    with open(LOG, "a") as fh:
        fh.write(time.strftime("%Y-%m-%d %H:%M ") + msg + "\n")


def job(kind, seed):
    if (OUT / f"test_{kind}_{seed}.json").exists() and (kind != "D3" or (OUT / f"test_D3-_{seed}.json").exists()):
        return 0
    note(f"start {kind} {seed}")
    if not (OUT / f"{kind}_{seed}.npz").exists():
        if sh(["train", kind, str(seed), str(STEPS)]) != 0:
            note(f"FAILED train {kind} {seed}")
            return 1
    rc = sh(["test", kind, str(seed)])
    if kind == "D3":
        rc |= sh(["test", "D3-", str(seed)])
    note(f"done {kind} {seed} rc {rc}")
    return rc


def stay_awake():
    """Ask Windows not to sleep while this queue runs (released when the process ends; no setting is changed)."""
    try:
        import ctypes
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)   # ES_CONTINUOUS | ES_SYSTEM_REQUIRED
    except Exception as e:                                                       # noqa: BLE001
        note(f"stay-awake request failed: {e}")


if __name__ == "__main__":
    stay_awake()
    OUT.mkdir(exist_ok=True)
    if not (OUT / "test_Script.json").exists():
        note("refs")
        sh(["refs"])
    jobs = [(k, s) for s in range(1, 9) for k in ("D3", "D2", "Dc", "D3i")]
    with ThreadPoolExecutor(WORKERS) as pool:
        rcs = list(pool.map(lambda j: job(*j), jobs))
    note(f"all done; failures {sum(1 for r in rcs if r)}")
