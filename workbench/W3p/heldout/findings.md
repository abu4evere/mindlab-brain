# W3p-H findings: the detour result holds on lands never used before (23 Nov 2026)

Plan: `questions.md`, tag `W3p-heldout-frozen`; run on the PC (Idle); `heldout_analysis.md` from the frozen script (its
console print failed on a character after the files were written; the print was fixed afterwards, no number changed).

| | R2: detour 4+ (152 cases) | R5d: long detour 10+ (40 cases) |
|---|---|---|
| **MBb** (balanced bump lessons) | **1.000, every seed 1.00** | **0.916 [0.850, 0.969]** |
| MB (bump lessons) | 0.751 [0.682, 0.822] | 0.044 |
| HR (W3n, the old brain) | 0.213 [0.163, 0.262] | 0.119 |
| Script / greedy / random | 1.00 / 0.00 / 0.007 | 1.00 / 0.00 / 0.00 |

- **Confirmed:** MB − HR on R2 +0.538 [+0.448, +0.641]; MBb − HR +0.787 [+0.738, +0.837]. MBb's lower bound (1.00) is
  above the Bob Profile's 0.80 on R2, and on R5d (0.850).
- MB fails long detours (0.044, below HR); balanced lessons fix that (the leaky "can I enter here?" filter).
- The numbers match the W3p preview on the original 50 test lands (MB 0.80, MBb 1.00, HR 0.27), so the original lands
  did not flatter the result.
- Against the prior: MB confirmed (90%) yes; MBb confirmed (95%) yes; MBb lower bound ≥ 0.80 (85%) yes.
- Limits: the same Bob Profile tests (memory fully known, hungry, no reflex); 8 seeds; the held-out set confirms the
  probe's result, not W3p's other readings (lifespan, survival), which W3p's frozen analysis gives.
