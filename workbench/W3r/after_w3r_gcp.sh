#!/bin/bash
# Google, after W3r's queue finishes here: the Bob Profile battery (W3r amendments 5-6) on this VM's W3r seeds
# (12-16), all 8 slots. CX2-C runs on Oracle (after_w3r_oci.sh), not here. Written 25 Nov 2026 (EST) from the
# second computer. Usage (on Google): setsid nohup bash after_w3r_gcp.sh > /dev/null 2>&1 < /dev/null &
# Log: ~/after_w3r_gcp.log
LOG=~/after_w3r_gcp.log
Q=~/mindlab/workbench/W3r/queue_progress.log
echo "$(date -u '+%F %H:%M') UTC waiting for W3r's queue to finish" >> $LOG
until grep -q "queue finished" $Q; do sleep 300; done
echo "$(date -u '+%F %H:%M') UTC W3r's queue finished; starting the Bob Profile" >> $LOG
cd ~/mindlab/workbench/W3r
nohup bash bp_battery.sh 8 12 13 14 15 16 > bp_battery_runner.out 2>&1 &
echo "$(date -u '+%F %H:%M') UTC started bp_battery.sh (8 slots, seeds 12-16; pid $!)" >> $LOG
