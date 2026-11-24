#!/bin/bash
# CX1 lane: run the given arms one after another, each at Idle priority, 1M steps, seeds 1+ (questions.md).
# Optional: WAIT_PID=<pid> waits for that process to end first (one of the PC's 2 slots).
cd /d/mindlab/exam_crafter
if [ -n "$WAIT_PID" ]; then while tasklist //FI "PID eq $WAIT_PID" | grep -q python; do sleep 60; done; fi
for k in "$@"; do
  echo "$(date '+%F %T') start $k" >> CX1/lane.log
  cmd //c "start /low /b /wait .venv\Scripts\python.exe play.py $k 1000000 1 CX1\output" > CX1/run_$k.out 2>&1
  echo "$(date '+%F %T') end $k ($(tail -2 CX1/run_$k.out | head -1))" >> CX1/lane.log
done
