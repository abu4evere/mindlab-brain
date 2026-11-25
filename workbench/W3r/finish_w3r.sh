#!/bin/bash
# W3r's finish, run on the PC when both VMs' queues have finished: download, merge (no clashes), probe, frozen analysis.
# The Bob Profile battery (bp_w3r.py) runs on a VM afterwards (bp_battery.sh). Usage: bash finish_w3r.sh
set -e
cd "$(dirname "$0")"
K=~/.ssh/mindlab_cloud
for M in oci:ubuntu@129.80.176.86 gcp:mindlab-cloud@35.221.60.73; do
  name=${M%%:*}; host=${M#*:}
  ssh -o ConnectTimeout=20 -i $K $host 'grep -q "queue finished" ~/mindlab/workbench/W3r/queue_progress.log' || { echo "$name not finished"; exit 1; }
  ssh -o ConnectTimeout=20 -i $K $host "cd ~/mindlab/workbench/W3r && tar czf ~/w3r_$name.tgz output queue_progress.log checks_$name.log"
  scp -q -o ConnectTimeout=20 -i $K $host:~/w3r_$name.tgz /tmp/
  mkdir -p dl/$name && tar xzf /tmp/w3r_$name.tgz -C dl/$name
done
python - <<'PY'
from pathlib import Path
import shutil, filecmp
dst = Path("output"); dst.mkdir(exist_ok=True)
for m in ("oci", "gcp"):
    for p in (Path("dl") / m / "output").iterdir():
        q = dst / p.name
        if q.exists():
            assert p.is_file() and filecmp.cmp(p, q, shallow=False), f"clash {p.name}"
        else:
            (shutil.copytree if p.is_dir() else shutil.copy2)(p, q)
print("merged")
PY
python probe_w3r.py
python analyse_w3r.py
