#!/bin/bash
# W3r on this machine: the checks first (they must print All: PASS), then the queue. Usage: start_after_checks.sh NAME SLOTS JOBFILE
cd "$(dirname "$0")"
PY=/home/ubuntu/venv/bin/python; [ -x "$PY" ] || PY=$HOME/venv/bin/python
$PY checks_w3r.py > checks_$1.log 2>&1
if grep -q "All: PASS" checks_$1.log; then
  nohup $PY run_queue.py $2 $3 > queue_$1.out 2>&1 &
  echo "$(date '+%F %H:%M') checks passed; queue started ($2 slots, $3)" >> queue_progress.log
else
  echo "$(date '+%F %H:%M') checks FAILED; queue not started" >> queue_progress.log
fi
