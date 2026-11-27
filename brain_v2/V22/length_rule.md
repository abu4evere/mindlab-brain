# V2-2 training length (the frozen rule in questions.md, applied to the pilot logs before any test life)

Rule: the first of 300k, 600k, 1M at which BOTH ||Wg|| and the critic loss changed by less than 10% over the last
100k steps; 1M if neither settles. Pilot runs: GOAL seeds 1 and 2 (Oracle; `output/pilot_trainlogs.txt`).

| pilot | at 300k: dWg, dloss | at 600k: dWg, dloss | at 1M: dWg, dloss |
|---|---|---|---|
| seed 1 | 0.352, 0.141 | 0.111, 0.103 | 0.018, 0.399 |
| seed 2 | 0.283, 0.059 | 0.121, 0.243 | 0.092, 0.509 |

Neither settles at 300k or 600k -> **length = 1M steps** for every arm and seed (the main runs were already run to 1M;
the 300k/600k snapshots are not used). Decided 27 Nov 2026 (EST, morning), blind to chains: no test life had been run.
