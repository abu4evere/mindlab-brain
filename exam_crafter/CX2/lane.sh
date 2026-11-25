#!/bin/bash
# CX2 lane: arms one after another, each at low priority, 1M steps, seeds 1+ (CX2/questions.md).
cd /d/mindlab/exam_crafter
for k in "$@"; do
  echo "$(date '+%F %T') start $k" >> CX2/lane.log
  cmd //c "start /low /b /wait .venv\Scripts\python.exe cx2.py $k 1000000 1 CX2\output" > CX2/run_$k.out 2>&1
  echo "$(date '+%F %T') end $k ($(tail -2 CX2/run_$k.out | head -1))" >> CX2/lane.log
done
