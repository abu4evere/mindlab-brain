"""The Bob Profile tests W3p's frozen analysis needs, run on the PC as brains arrive (W3p's readout; no new reading).

Fetches each finished kept copy (<ARM>_CS_<SEED>.npz) from the two VMs into W3p/output, and runs bp_mv.py for every
(test, arm, seed) whose result file is missing, WORKERS at a time at Idle priority. Also HR's seed 4 (still training
when the Bob Profile battery ran) and the PLAN measure for HR. Logs to bp_queue.log; stops when all are done.

  python bp_queue.py [WORKERS]
"""
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).parent
BP_OUT = HERE.parent.parent / "scorecard" / "bp" / "output"
WORKERS = int(sys.argv[1]) if len(sys.argv) > 1 else 2
HOSTS = ["ubuntu@129.80.176.86", "mindlab-cloud@35.221.60.73"]
KEY = str(Path.home() / ".ssh" / "mindlab_cloud")
TESTS = ["R2", "R5d", "M2", "M2e", "A2", "G2", "L2", "A5s"]
JOBS = [(t, "HR", 4) for t in TESTS] + [("PLAN", "HR", s) for s in range(1, 9)]
JOBS += [(t, a, s) for a in ("MB", "MBb", "MV") for s in range(1, 9) for t in ["PLAN", "WALLS"] + TESTS]


def log(msg):
    with open(HERE / "bp_queue.log", "a") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M} {msg}\n")


def fetch():
    for h in HOSTS:
        try:
            out = subprocess.run(["ssh", "-i", KEY, "-o", "ConnectTimeout=15", h, "ls ~/mindlab/workbench/W3p/output/"],
                                 capture_output=True, text=True, timeout=60).stdout.split()
        except Exception:
            continue
        names = set(out)
        for name in out:
            arm, _, seed = name[:-4].partition("_CS_") if name.endswith(".npz") else ("", "", "")
            finished = f"test_{arm}S-bare_{seed}.json" in names      # the run's last test: the kept copy is final
            if "_CS_" in name and finished and not (HERE / "output" / name).exists():
                tmp = HERE / "output" / (name + ".part")
                r = subprocess.run(["scp", "-i", KEY, "-q", f"{h}:~/mindlab/workbench/W3p/output/{name}", str(tmp)], timeout=300)
                if r.returncode == 0:
                    tmp.rename(HERE / "output" / name)
                    log(f"fetched {name} from {h.split('@')[1]}")


def done(t, a, s):
    return (BP_OUT / f"{t}_{a}S_{s}.json").exists()


def ready(a, s):
    d = HERE.parent / "W3n" / "output" if a == "HR" else HERE / "output"
    return (d / f"{a}_CS_{s}.npz").exists()


(HERE / "output").mkdir(exist_ok=True)
running = []
last_fetch = 0.0
while True:
    if time.time() - last_fetch > 600:
        fetch()
        last_fetch = time.time()
    for p, job in list(running):
        if p.poll() is not None:
            log(f"done {' '.join(map(str, job))} (exit {p.returncode})")
            running.remove((p, job))
    busy = {j for _, j in running}
    todo = [j for j in JOBS if not done(*j) and j not in busy]
    if not todo and not running:
        log("all done")
        break
    for j in [j for j in todo if ready(j[1], j[2])][:max(0, WORKERS - len(running))]:
        p = subprocess.Popen([sys.executable, str(HERE / "bp_mv.py"), j[0], j[1], str(j[2])], cwd=str(HERE),
                             stdout=subprocess.DEVNULL, stderr=open(HERE / "output" / f"bp_{j[0]}_{j[1]}_{j[2]}.err", "w"),
                             creationflags=0x00000040)
        running.append((p, j))
        log(f"start {' '.join(map(str, j))}")
    time.sleep(30)
