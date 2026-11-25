#!/bin/bash
# The Bob Profile on W3r's kept copies (amendments 5, 6), on a VM, at most SLOTS at once. Usage: bp_battery.sh SLOTS SEEDS...
cd "$(dirname "$0")"
PY=$HOME/venv/bin/python; SLOTS=$1; shift
for arm in RM HRr RMX RE5; do for s in "$@"; do for t in L2 R2 R5d M2 M2e G2 A2 A5s; do
  [ -f bp_output/${t}_${arm}S_${s}.json ] && continue
  while [ "$(pgrep -fc 'bp_w3r.py')" -ge "$SLOTS" ]; do sleep 30; done
  nice -n 10 $PY bp_w3r.py $t $arm $s >> bp_battery.log 2>&1 &
  sleep 2
done; done; done
wait; echo "$(date '+%F %H:%M') battery finished" >> bp_battery.log
