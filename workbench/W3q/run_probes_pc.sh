#!/bin/bash
# W3q probes on the PC (one at a time, low priority): every arm and seed that is downloaded.
cd "$(dirname "$0")"
for arm in "$@"; do for s in 1 2 3 4 5 6 7 8; do
  echo "$(date '+%F %H:%M') probe $arm $s" >> probes_pc.log
  python probe_w3q.py $arm $s >> probes_pc.log 2>&1
done; done
echo "$(date '+%F %H:%M') probes finished: $*" >> probes_pc.log
