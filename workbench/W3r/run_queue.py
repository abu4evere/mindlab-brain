"""W3r's queue on one machine: keeps at most SLOTS heavy runs alive (W3r's own, plus W3q's and BX1's runs started by
anything else), and starts W3r jobs from JOBFILE (lines "ARM SEED") at the lowest priority. Logs to
queue_progress.log.

  python run_queue.py SLOTS JOBFILE
"""
import os
import subprocess
import sys
import time
from datetime import datetime

SLOTS = int(sys.argv[1])
JOBS = [l.split() for l in open(sys.argv[2], encoding="utf-8") if l.strip()]
HEAVY = ("w3r.py run", "w3q.py run", "w3n.py run", "w3o.py run", "run_school.py")


def running():
    out = subprocess.run(["ps", "-eo", "args"], capture_output=True, text=True).stdout
    return [l for l in out.splitlines() if "python" in l and any(h in l for h in HEAVY) and "run_queue" not in l]


def log(msg):
    with open("queue_progress.log", "a") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M} {msg}\n")


mine = []
while JOBS or any(p.poll() is None for p, _ in mine):
    for p, job in list(mine):
        if p.poll() is not None:
            log(f"done {job[0]} {job[1]} (exit {p.returncode})")
            mine.remove((p, job))
    while JOBS and len(running()) < SLOTS:
        a, s = JOBS.pop(0)
        out = open(f"run_{a}_{s}.out", "w")
        p = subprocess.Popen([sys.executable, "w3r.py", "run", a, s, "999"], stdout=out, stderr=subprocess.STDOUT,
                             preexec_fn=lambda: os.nice(19))
        mine.append((p, (a, s)))
        log(f"start {a} {s}")
        time.sleep(5)
    time.sleep(60)
log("queue finished")
