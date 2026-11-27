# BV1 findings (Body v1, step 1): the interface gate PASSES

Frozen plan: `questions.md` (tag BV1-frozen; the creator's sign-off 26 Nov 2026). Run 26 Nov 2026 (evening, EST) on
the second computer (Windows 10, AMD Ryzen 5 5600, Python 3.12.10, numpy 2.5.3), Idle priority. Every number below is
from `output/gate.json` (written by `bv1.py`) and `checks_bv1.log` (written by `checks_bv1.py`).

## What was tested
Whether Body v1 (standard senses, verbs, two-part feedback, a per-world adapter) connects W3r's RM brain to Mind
Lab's world without changing anything it sees, learns or does. An interface gate only: no hands, use or operate(k)
are exercised (this world has none), and nothing here is a claim about the body's generality (step 2).

## Results
1. **Adapter audit (before any brain): All: PASS** on 4 fresh lands, each unrenamed and under 3 renamings, with a
   scripted random body (500 steps): every verb always legal and the list unchanged; every non-eye output identical
   under every renaming; eyes and touch a pure relabelling; feedback keys body-only; the meaning table, renamed back,
   identical under every renaming.
2. **Exact parity: BODY and BODY-SHUF reproduce NATIVE bit for bit on all 8 seeds** (RMS seeds 1-8, fresh land
   910001), compared at every step on the action, position, energy, fatigue, the brain's input layers and the table's
   counts. NATIVE lifespans: 3000 on seeds 1-3 and 5-8, 1628 on seed 4 (identical in all arms).
3. **Coverage met with the 8 lives** (so no seeds were added): wall hits 579, meals below the energy cap 865, **meals
   at the cap 105**, rests at the shelter 3090, steps at map edges 2618. The meals at the cap are the case GPT flagged
   in the round-table (a meal hidden in the net energy change); the two-part feedback (the body's drift, then the
   world's response) recovers every one.
4. **Determinism:** BODY on seed 1 twice: identical.

**Gate: PASS** (by the frozen rule: all of 1-4).

## Build decisions recorded (all consistent with the frozen plan; listed in `body_v1.py`)
- The feedback's signed parts are computed from the body's own quantities (energy, fatigue), not from the 0-1
  feelings, because the tiredness feeling saturates at F_CAP while fatigue does not.
- The body's drift is its own metabolism (world3.py's rule: -2 energy for a move taken while tired, else -1; fatigue
  +1). "use" passes time like rest (the frozen brain never chooses it).
- The brains (RM_CS_1-11.npz) were copied from Oracle into `brains/` (checksums equal; not committed: they are W3r's
  outputs).

## Limits
- An interface check on one world; it says nothing about learning through the body or about hands and operations.
- W3r's official reading is not final yet (preliminary only); this gate stands either way as an interface check.
- **Independent re-run still to do** (the project's recompute rule): a fresh session re-runs `checks_bv1.py` and
  `bv1.py` from the repository and confirms "All: PASS" and the same `gate.json`, before these findings are final.

## What it means for Bob
Today's brain can live through the standard body with nothing lost. The body is ready for step 2 (a small crafting
world where things held in the hands combine: the creator's "start with things in hands then add station"), which
needs its own plan, council and sign-off.

## Appended 26 Nov 2026 (about 20:35 EST): independent re-run, PASS confirmed
A fresh Claude session (not the one that built and ran BV1) re-ran both scripts from the repository, unchanged, on the
second computer (Windows 10, AMD Ryzen 5 5600, Python 3.12.10, numpy 2.5.3), Idle priority. The brains in `brains/`
were first checked against W3r's outputs on Oracle (`~/mindlab/workbench/W3r/output/RM_CS_1-8.npz`): SHA-256 equal
for all 8.
- `checks_bv1.py`: **All: PASS**; its log is identical, line for line, to the committed `checks_bv1.log` (kept as
  `checks_bv1_rerun_2026-11-26.log`).
- `bv1.py`: **Gate: PASS**; the new `gate.json` (kept as `output/gate_rerun_2026-11-26.json`) equals the committed one
  in every field (all 8 seeds' lifespans and coverage, parity BODY and BODY-SHUF vs NATIVE, coverage totals 579 / 865
  / 105 / 3090 / 2618, coverage met, determinism, machine) except the wall-clock `seconds` (234.8 vs 186.1).
Limit: the same machine as the first run (a different machine was not needed: the gate is exact parity, not a
statistic). **These findings are now final.**
