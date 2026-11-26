#!/bin/bash
# Oracle, after W3r's queue finishes here: the handoff's next work (D:\acl\docs\HANDOFF_2026-11-25.md).
#  1. CX2-C resumes from its own files, the frozen command (exam_crafter/CX2/questions.md, "CX2-C"), 4 arms;
#  2. the Bob Profile battery (W3r amendments 5-6) on this VM's W3r seeds (1-11), with the other 12 slots.
# Single-threaded numerical libraries so 16 processes share 16 threads (Crafter lives are not paired across
# processes or machines anyway: CX2 amendment 2). Written 25 Nov 2026 (EST) from the second computer.
# Usage (on Oracle): nohup bash after_w3r_oci.sh > /dev/null 2>&1 &     Log: ~/after_w3r_oci.log
LOG=~/after_w3r_oci.log
Q=~/mindlab/workbench/W3r/queue_progress.log
echo "$(date -u '+%F %H:%M') UTC waiting for W3r's queue to finish" >> $LOG
until grep -q "queue finished" $Q; do sleep 300; done
echo "$(date -u '+%F %H:%M') UTC W3r's queue finished; starting CX2-C and the Bob Profile" >> $LOG
cd ~/exam_crafter
for arm in learn named blind random5p; do
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nohup nice -n 10 .venv/bin/python cx2.py $arm 3000000 100001 CX2/output_confirm > CX2/run_confirm_$arm.out 2>&1 &
  echo "$(date -u '+%F %H:%M') UTC started CX2-C $arm (pid $!)" >> $LOG
  sleep 2
done
cd ~/mindlab/workbench/W3r
nohup bash bp_battery.sh 12 1 2 3 4 5 6 7 8 9 10 11 > bp_battery_runner.out 2>&1 &
echo "$(date -u '+%F %H:%M') UTC started bp_battery.sh (12 slots, seeds 1-11; pid $!)" >> $LOG
