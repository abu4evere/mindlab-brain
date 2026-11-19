"""Watch W3m's cloud jobs, resume paused training runs, collect finished outputs into workbench/W3m/output.
State in W3m/chains.json (name -> list of run ids). Logs to W3m/manage.log. Orchestration only; no study code."""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

GH = "C:/Users/User/gh/bin/gh.exe"
REPO = "abu4evere/mindlab"
W = Path("D:/mindlab/workbench/W3m")
DL = W / "dl"
CH = W / "chains.json"
LOG = W / "manage.log"


def gh(*a):
    for attempt in range(10):                      # network blips (13:15 on 16 Nov killed the manager): retry
        r = subprocess.run([GH, *a], capture_output=True, text=True, encoding="utf-8")
        if r.returncode == 0:
            return r.stdout
        time.sleep(60)
    raise RuntimeError(r.stderr)


def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M ") + msg + "\n")


jobs = {}
for line in (W / "jobs.tsv").read_text(encoding="utf-8").splitlines():
    name, d, checks, cmd, save = line.split("\t")
    jobs[name] = (d, checks, cmd, save)
if CH.exists():
    chains = json.loads(CH.read_text())
else:
    chains = {name: [rid] for rid, name in (l.split("\t") for l in (W / "run_ids.txt").read_text().splitlines())}
    chains = {k: {"runs": v, "state": "running"} for k, v in chains.items()}
CH.write_text(json.dumps(chains, indent=1))

while True:
    open_ = [n for n, c in chains.items() if c["state"] == "running"]
    if not open_:
        log("all chains closed")
        break
    for name in open_:
        rid = chains[name]["runs"][-1]
        st = json.loads(gh("run", "view", rid, "-R", REPO, "--json", "status,conclusion"))
        if st["status"] != "completed":
            continue
        dest = DL / name / rid
        if dest.exists():
            shutil.rmtree(dest)
        gh("run", "download", rid, "-R", REPO, "-D", str(dest))
        outs = list(dest.rglob("output"))
        files = [p for o in outs for p in o.iterdir()] if outs else []
        names = {p.name for p in files}
        ckpt = any(n.endswith(".ckpt.pkl") for n in names) or "wrong_machine.flag" in names   # amendment 2: re-queue
        retry = st["conclusion"] == "cancelled" and chains[name].get("retries", 0) < 3   # a lost runner: try again
        if retry:
            chains[name]["retries"] = chains[name].get("retries", 0) + 1
        if st["conclusion"] != "success" and not retry:
            chains[name]["state"] = "failed"
            log(f"{name} run {rid} concluded {st['conclusion']}")
        elif ckpt or retry:
            d, checks, cmd, save = jobs[name]
            before = {r["databaseId"] for r in json.loads(gh("run", "list", "-R", REPO, "-w", "run.yml", "-L", "5",
                                                            "--json", "databaseId"))}
            gh("workflow", "run", "run.yml", "-R", REPO, "-f", f"name={name}", "-f", f"dir={d}", "-f",
               f"checks={checks}", "-f", f"command={cmd}", "-f", f"save={save}", "-f", f"resume_run_id={rid}")
            new = None
            for _ in range(20):
                time.sleep(4)
                now = [r["databaseId"] for r in json.loads(gh("run", "list", "-R", REPO, "-w", "run.yml", "-L", "5",
                                                                  "--json", "databaseId"))]
                fresh = [x for x in now if x not in before]
                if fresh:
                    new = str(max(fresh))
                    break
            chains[name]["runs"].append(new)
            log(f"{name} {'cancelled (retry ' + str(chains[name]['retries']) + ')' if retry else 'paused'} in run {rid}; resumed as {new}")
        else:
            (W / "output").mkdir(exist_ok=True)
            for p in files:
                if p.is_file():
                    shutil.copy2(p, W / "output" / p.name)
            chains[name]["state"] = "finished"
            log(f"{name} finished in run {rid} ({len(files)} files collected)")
        CH.write_text(json.dumps(chains, indent=1))
    time.sleep(300)
