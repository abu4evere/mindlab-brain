#!/bin/bash
# Status line every 30 minutes, shown as a Claude background task on the second computer (the creator asked to see
# the check inside Claude, 25 Nov 2026). Read-only: W3r queue and Bob Profile counts on both cloud machines.
K=~/.ssh/mindlab_cloud
Q='W=~/mindlab/workbench/W3r; L=$W/queue_progress.log; echo "W3r done $(grep -c " done " $L), fails $(grep " done " $L | grep -vc "exit 0"), $(grep -q "queue finished" $L && echo FINISHED || echo running); Bob Profile $(ls $W/bp_output 2>/dev/null | wc -l)"'
while true; do
  t=$(TZ='EST5EDT,M3.2.0,M11.1.0' date '+%a %b %d %H:%M EST')
  o=$(timeout 40 ssh -i $K -o BatchMode=yes -o ConnectTimeout=15 ubuntu@129.80.176.86 "$Q" 2>/dev/null || echo "unreachable")
  g=$(timeout 40 ssh -i $K -o BatchMode=yes -o ConnectTimeout=15 mindlab-cloud@35.221.60.73 "$Q" 2>/dev/null || echo "unreachable")
  echo "[$t] Oracle (55 runs, 352 BP tests): $o | Google (25 runs, 160 BP tests): $g"
  sleep 1800
done
