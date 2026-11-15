"""Mind Lab cloud helper: dispatch study jobs to GitHub's machines (run.yml), wait for them, fetch their artifacts.

  python tools/cloud.py dispatch JOBS_FILE RUN_IDS_FILE
      JOBS_FILE: one job per line, "name<TAB>dir<TAB>checks<TAB>command<TAB>save" (checks may be empty).
      Writes the new run ids (one per line, "id<TAB>name") to RUN_IDS_FILE.
  python tools/cloud.py wait RUN_IDS_FILE [SECONDS_BETWEEN_POLLS]
      Polls until every run has completed; prints each conclusion; exit code 1 if any is not "success".
  python tools/cloud.py fetch RUN_IDS_FILE DEST_DIR
      Downloads each run's artifact into DEST_DIR/<name>/ (gh run download).

gh is at C:/Users/User/gh/bin/gh.exe; the repo is abu4evere/mindlab. Nothing here changes the repo or any study code.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

GH = "C:/Users/User/gh/bin/gh.exe"
REPO = "abu4evere/mindlab"


def gh(*args, capture=True):
    r = subprocess.run([GH, *args], capture_output=capture, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise SystemExit(f"gh {' '.join(args)} failed: {r.stderr}")
    return r.stdout


def run_list(limit=60):
    out = gh("run", "list", "-R", REPO, "--workflow", "run.yml", "--limit", str(limit),
             "--json", "databaseId,status,conclusion,createdAt")
    return json.loads(out)


def dispatch(jobs_file, ids_file):
    jobs = [ln.rstrip("\n").split("\t") for ln in Path(jobs_file).read_text(encoding="utf-8").splitlines() if ln.strip()]
    before = {r["databaseId"] for r in run_list()}
    for name, d, checks, command, save in jobs:
        gh("workflow", "run", "run.yml", "-R", REPO, "-f", f"name={name}", "-f", f"dir={d}", "-f", f"checks={checks}",
           "-f", f"command={command}", "-f", f"save={save}")
        print("dispatched", name, flush=True)
        time.sleep(2)
    new = []
    for _ in range(30):
        time.sleep(10)
        new = sorted(r["databaseId"] for r in run_list() if r["databaseId"] not in before)
        if len(new) >= len(jobs):
            break
    if len(new) != len(jobs):
        print(f"WARNING: {len(new)} new runs seen for {len(jobs)} jobs", flush=True)
    # dispatch order = creation order (ids rise with time); names are paired in that order
    names = {}
    for rid, (name, *_rest) in zip(new, jobs):
        names[rid] = name
    for rid in new:
        nm = names.get(rid, "")
        full = gh("run", "view", str(rid), "-R", REPO, "--json", "jobs")
        # the artifact name carries the study name; confirm from the job's step title when available
        try:
            steps = json.loads(full)["jobs"][0]["steps"]
            titles = " ".join(s["name"] for s in steps)
        except Exception:                                                      # noqa: BLE001
            titles = ""
        names[rid] = nm or titles
    Path(ids_file).write_text("".join(f"{rid}\t{names[rid]}\n" for rid in new), encoding="utf-8")
    print("run ids written to", ids_file, flush=True)


def read_ids(ids_file):
    rows = [ln.split("\t") for ln in Path(ids_file).read_text(encoding="utf-8").splitlines() if ln.strip()]
    return [(int(r[0]), r[1] if len(r) > 1 else str(r[0])) for r in rows]


def wait(ids_file, every=60):
    ids = read_ids(ids_file)
    pending = {rid for rid, _ in ids}
    conclusions = {}
    while pending:
        for rid in sorted(pending):
            info = json.loads(gh("run", "view", str(rid), "-R", REPO, "--json", "status,conclusion"))
            if info["status"] == "completed":
                conclusions[rid] = info["conclusion"]
                pending.discard(rid)
                print(time.strftime("%H:%M:%S"), rid, info["conclusion"], flush=True)
        if pending:
            print(time.strftime("%H:%M:%S"), len(pending), "still running", flush=True)
            time.sleep(every)
    bad = [rid for rid, c in conclusions.items() if c != "success"]
    print("all completed;", "all success" if not bad else f"NOT success: {bad}", flush=True)
    return 1 if bad else 0


def fetch(ids_file, dest):
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    for rid, name in read_ids(ids_file):
        d = dest / (name or str(rid))
        d.mkdir(parents=True, exist_ok=True)
        gh("run", "download", str(rid), "-R", REPO, "-D", str(d), capture=True)
        print("fetched", rid, name, "->", d, flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "dispatch":
        dispatch(sys.argv[2], sys.argv[3])
    elif cmd == "wait":
        raise SystemExit(wait(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 60))
    elif cmd == "fetch":
        fetch(sys.argv[2], sys.argv[3])
    else:
        raise SystemExit(__doc__)
