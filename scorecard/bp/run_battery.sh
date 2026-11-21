#!/bin/bash
# The Bob Profile battery (BP-frozen): controls, then W3n's HRS on 8 seeds; quick probes first, full lives after.
cd "$(dirname "$0")"
for t in R2 R5d M2 A2; do for c in script greedy random; do python bp_tests.py $t $c > /dev/null 2>&1; done; done
for s in 1 2 3 5 6 7 8 9; do for t in R2 R5d M2 M2e A2; do python bp_tests.py $t HR $s > /dev/null 2>&1; done; done
for t in L2 G2 A5s; do for c in script random; do python bp_tests.py $t $c > /dev/null 2>&1; done; done
for s in 1 2 3 5 6 7 8 9; do for t in L2 G2 A5s; do python bp_tests.py $t HR $s > /dev/null 2>&1; done; done
python bp_score.py HR 1,2,3,5,6,7,8,9 > battery_done.txt 2>&1
