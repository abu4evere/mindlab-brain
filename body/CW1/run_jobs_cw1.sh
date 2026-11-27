#!/bin/bash
# CW1 runner for a machine: run_jobs_cw1.sh PYTHON SLOTS "ARM:SEED ARM:SEED ..."
# Runs each (arm, seed) as `python cw1.py run ARM SEED` (50 test lives; resumes from its jsonl), SLOTS at a time,
# at low priority, single-threaded BLAS; logs to output/jobs_<host>.log.
cd "$(dirname "$0")"
PY=$1; SLOTS=$2; JOBS=$3
mkdir -p output
LOG=output/jobs_$(hostname).log
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
echo "$(date -u +%FT%TZ) start slots=$SLOTS jobs=$JOBS" >> "$LOG"
for j in $JOBS; do
  while [ "$(jobs -rp | wc -l)" -ge "$SLOTS" ]; do sleep 5; done
  arm=${j%%:*}; seed=${j##*:}
  ( nice -n 19 "$PY" cw1.py run "$arm" "$seed" > "output/run_${arm}_${seed}.out" 2>&1
    echo "$(date -u +%FT%TZ) done $arm $seed (exit $?)" >> "$LOG" ) &
done
wait
echo "$(date -u +%FT%TZ) all finished" >> "$LOG"
