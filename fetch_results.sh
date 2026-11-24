#!/bin/bash
# Fetch finished results from the Google VM quickly (for short connections): CX1's random arm, W3q's RP 8, W3r status.
K=~/.ssh/mindlab_cloud; G=mindlab-cloud@35.221.60.73; O=ubuntu@129.80.176.86
set -e
cd /d/mindlab
ssh -o ConnectTimeout=20 -i $K $G 'pgrep -f "play.py random 1000000" >/dev/null && echo "CX1 random still running" || echo "CX1 random done"; cat ~/exam_crafter/CX1/run_random.out | head -2; pgrep -f "w3q.py run" >/dev/null && echo "W3q RP 8 still running" || echo "W3q RP 8 done"'
scp -q -o ConnectTimeout=20 -i $K $G:~/exam_crafter/CX1/output/random.jsonl exam_crafter/CX1/random_from_gcp.jsonl
scp -q -o ConnectTimeout=20 -i $K $G:~/exam_crafter/CX1/run_random.out exam_crafter/CX1/run_random_gcp.out
ssh -o ConnectTimeout=20 -i $K $G 'cd ~/mindlab/workbench/W3q && tar czf ~/w3q_rp8.tgz $(ls -d output/*RP*_8* output/*RP*_8.* 2>/dev/null | sort -u) queue_progress.log'
scp -q -o ConnectTimeout=20 -i $K $G:~/w3q_rp8.tgz /tmp/
mkdir -p workbench/W3q/dl/gcp_rp8 && tar xzf /tmp/w3q_rp8.tgz -C workbench/W3q/dl/gcp_rp8
ssh -o ConnectTimeout=20 -i $K $G 'tail -3 ~/mindlab/workbench/W3r/queue_progress.log'
ssh -o ConnectTimeout=20 -i $K $O 'tail -3 ~/mindlab/workbench/W3r/queue_progress.log' || true
echo FETCHED
