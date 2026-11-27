#!/bin/bash
# V2-3 main runs (amendment A1, world B250): one arm-seed = train 1M steps, then its tests and the Bob Profile.
# usage: run_arm.sh ARM SEED   (ARM FROZEN: only the B test; FROZEN's home test and Bob Profile run once elsewhere)
cd "$(dirname "$0")"; PY=${PY:-python}; W=B250; arm=$1; s=$2
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
mkdir -p output bp_output
[ -f output/skip_${arm}_${s} ] && { echo "skipped $arm $s (runs elsewhere)"; exit 0; }
if [ "$arm" = FROZEN ]; then $PY v23.py test B FROZEN $s $W >> output/test_FROZEN_$s.out 2>&1; echo "done FROZEN $s"; exit; fi
[ -f output/net_${arm}_${s}.npz ] || $PY v23.py train $arm $s 1000000 $W > output/train_${arm}_${s}.out 2>&1 || { echo "FAILED train $arm $s"; exit 1; }
for k in B H; do for t in "" snap250k snap500k; do $PY v23.py test $k $arm $s $W $t >> output/test_${arm}_${s}.out 2>&1 || echo "FAILED test $k $arm $s $t"; done; done
for t in L2 R2 R5d M2 M2e G2 A2 A5s; do [ -f bp_output/${t}_${arm}_${s}.json ] || $PY v23.py bp $t $arm $s >> output/test_${arm}_${s}.out 2>&1 || echo "FAILED bp $t $arm $s"; done
echo "done $arm $s"
