# WR: independent blind recompute (15 November 2026)

Two fresh assistant sessions (sub-agents of the main session, started after the data were in) each wrote their own
script from the raw files in `output/` and the plan's "Measures" and "Readings" sections. Neither opened
`analyse_wr.py`, `analysis.md`, `analysis.json` or `findings.md` (each listed every file it read). Both found 24 cells
of 48 children. Numbers below are copied from their replies; the analysis column is from `analysis.json`.

| item | recomputer 1 | recomputer 2 | analyse_wr.py | match |
|---|---|---|---|---|
| change 128, LTYR − TYR, A45 | −0.062 [−0.118, −0.007] | −0.062 [−0.118, −0.007] | −0.062 [−0.118, −0.007] | yes |
| change 128, LTYR − TYR, B60 | −0.007 [−0.056, +0.042] | −0.007 [−0.056, +0.042] | −0.007 [−0.056, +0.042] | yes |
| change 128, LTYR − TYR, A30 / B45 | 0 [0, 0] / 0 [0, 0] | 0 [0, 0] / 0 [0, 0] | 0 [0, 0] / 0 [0, 0] | yes |
| change 128, LTYR − TYR, food | +25.5 [+17.3, +33.4] | +25.5 [+17.3, +33.4] | +25.458 [+17.333, +33.438] | yes |
| change 128, LTYR − LTR, B60 | +0.160 [+0.097, +0.222] | +0.160 [+0.097, +0.222] | +0.160 [+0.097, +0.222] | yes |
| change 128, LTYR − LTY, A45 | +0.368 [+0.285, +0.451] | +0.368 [+0.285, +0.451] | +0.368 [+0.285, +0.451] | yes |
| change 128, LTYR − LYR, A45 | +0.431 [+0.340, +0.521] | +0.431 [+0.340, +0.521] | +0.431 [+0.340, +0.521] | yes |
| stable 128, LTYR − L, day 30 | 0 [0, 0] | 0 [0, 0] | 0 [0, 0] | yes |
| stable 128, LTYR − L, day 7 | +0.062 [+0.021, +0.104] | +0.062 [+0.021, +0.104] | +0.062 [+0.021, +0.104] | yes |
| stable 128, TYR day-30 mean | 1.000 | 1.000 | 1.000 | yes |
| change 32, LTYR − TYR, A45 / B60 | −0.007 [−0.049, +0.035] / +0.028 [−0.021, +0.076] | the same | the same | yes |
| change 128 means: LTYR A45, B60, food | 0.444, 0.444, 1512.9 | 0.444, 0.444, 1512.9 | 0.444, 0.444, 1513 | yes |
| change 128 means: TYR A45, B60, food | 0.507, 0.451, 1487.4 | 0.507, 0.451, 1487.4 | 0.507, 0.451, 1487 | yes |

- Both recomputers read the readings the same way as the script: 1 NO, 2 NO, 3 (the parts asked) yes, 4 YES, 5 YES.
- Recomputer 2 noted that reading 1 fails on B60 as well (lower bound −0.056), which the findings' first draft had
  called a tie; the findings were corrected before they were committed.
- The exact zeros are genuine: every child of both arms scores 1.0 on those readings.
