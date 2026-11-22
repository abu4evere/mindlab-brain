"""W3p's queue on one machine: keeps at most SLOTS Mind Lab runs ('w3n.py run' or 'w3o.py run') alive, counting runs
started by anything else, and starts W3p jobs from JOBFILE (lines "ARM SEED") at the lowest priority. Logs to
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
WIN = os.name == "nt"


def running():
    if WIN:
        cmd = ["powershell", "-NoProfile", "-Command",
               "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | ForEach-Object { $_.CommandLine }"]
    else:
        cmd = ["ps", "-eo", "args"]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    return [l for l in out.splitlines() if ("w3n.py run" in l or "w3o.py run" in l or "w3p.py run" in l) and "run_queue" not in l]


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
        kw = {"creationflags": 0x00000040} if WIN else {"preexec_fn": lambda: os.nice(19)}   # IDLE_PRIORITY_CLASS / nice 19
        p = subprocess.Popen([sys.executable, "w3p.py", "run", a, s, "999"], stdout=out, stderr=subprocess.STDOUT, **kw)
        mine.append((p, (a, s)))
        log(f"start {a} {s}")
        time.sleep(5)
    time.sleep(60)
log("queue finished")
