#!/bin/bash
# Wait until no W3p run is left on this machine, then W3q's checks; start the queue only on All: PASS.
cd "$(dirname "$0")"
SLOTS=$1; JOBS=$2; LOG=$3
while pgrep -f "w3p.py run" > /dev/null || pgrep -f "W3p/run_queue.py\|run_queue.py 16 jobs_oci\|run_queue.py 8 jobs_pc" > /dev/null; do sleep 300; done
echo "$(date '+%F %T') W3p finished here; W3q checks" >> queue_progress.log
~/venv/bin/python checks_w3q.py > "$LOG" 2>&1; echo "exit $?" >> "$LOG"
if grep -q "All: PASS" "$LOG"; then ~/venv/bin/python run_queue.py "$SLOTS" "$JOBS"; else echo "$(date '+%F %T') checks FAILED; not started" >> queue_progress.log; fi
