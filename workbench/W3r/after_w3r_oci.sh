#!/bin/bash
# Oracle, after W3r's queue finishes here: the handoff's next work (D:\acl\docs\HANDOFF_2026-11-25.md).
#  1. (CX2-C was here; moved to the second computer on 25 Nov 2026, see below)
#  2. the Bob Profile battery (W3r amendments 5-6) on this VM's W3r seeds (1-11), with the other 12 slots.
# Single-threaded numerical libraries so 16 processes share 16 threads (Crafter lives are not paired across
# processes or machines anyway: CX2 amendment 2). Written 25 Nov 2026 (EST) from the second computer.
# Usage (on Oracle): nohup bash after_w3r_oci.sh > /dev/null 2>&1 &     Log: ~/after_w3r_oci.log
LOG=~/after_w3r_oci.log
Q=~/mindlab/workbench/W3r/queue_progress.log
echo "$(date -u '+%F %H:%M') UTC waiting for W3r's queue to finish" >> $LOG
until grep -q "queue finished" $Q; do sleep 300; done
# An early Bob Profile batch (seeds 1-9, 9 slots) was started on 26 Nov 01:45 EST while W3r's last runs used only 7 of
# the 16 threads; wait for it, so no test is started twice (bp_battery.sh skips tests whose result exists).
while pgrep -f "bp_battery.sh" > /dev/null; do sleep 300; done
echo "$(date -u '+%F %H:%M') UTC W3r's queue finished; starting the Bob Profile" >> $LOG
# CX2-C moved to the second computer (25 Nov 2026, 23:50 EST; the creator asked that this PC be used too), so this
# script no longer starts it here: the Bob Profile gets all 16 slots.
cd ~/mindlab/workbench/W3r
nohup bash bp_battery.sh 16 1 2 3 4 5 6 7 8 9 10 11 > bp_battery_runner.out 2>&1 &
echo "$(date -u '+%F %H:%M') UTC started bp_battery.sh (16 slots, seeds 1-11; pid $!)" >> $LOG
