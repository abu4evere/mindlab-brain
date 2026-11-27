# V2-3 Keep learning for life, with protection: FROZEN PLAN (Brain v2, step 3)

Frozen 28 Nov 2026 (EST, early) by the assistant under the creator's sleep-mode autonomy (council: GPT, Gemini,
DeepSeek, `roundtable_v23_2026-11-28.md`); this is `questions_draft.md` revised by it.

## Question
Can the walker (RMS, W3n's DriveVIN) keep learning in a new world as an adult, gaining there, while keeping its old
abilities?

## Worlds and the pilot rule (fixed now)
- Home A: W3r's lands. New world B1: the same with food regrowth twice as slow (R x2).
- **Pilot (seeds 1-2, pilot lands 999001-999020, 1M steps):** if FREE − FROZEN survival in B1 is at least +0.08 (mean
  over the two seeds), B = B1. Otherwise B = B2: R x2 AND the shelter moved to the farthest open cell from its place
  (a structural change, DeepSeek). The pilot is about B only; pilot brains are never test brains.

## Arms (16 seeds = RMS 1-16; 1M steps of adult learning in B, V2-2's loop without hands or goal)
FROZEN; FREE (plain actor-critic); SLOW (learning rate x0.1); ANCHOR (EWC-style penalty toward the RMS weights,
importance = mean squared policy gradients over 20 home lives measured before learning; one strength, set now: the
penalty's weight equals the inverse of the mean importance); REHEARSE (after each B life, one home life with learning
on; the same number of B steps as every other arm, its home steps extra and reported); REPLAY (a buffer of 20,000 home
transitions with their returns, recorded before learning; each update mixes one home segment for every B segment).

## Measures (fixed now)
- **Primary, per arm, both parts needed:** (a) survival in B (test lands 997001-997050), arm − FROZEN, lower end above 0;
  (b) no home loss: the Bob Profile vs RMS (no test with the 95% lower end below −0.05; V2-2's rule) and home survival
  (W3r's fresh lands 910001-910050) arm − FROZEN, lower end above −0.03. The protections are judged against FREE and
  must beat SLOW on retention at equal or better B gain.
- Secondaries: snapshots at 250k and 500k (B survival, home survival) reported, never chosen as the primary; weight drift
  from RMS; REHEARSE's total steps.

## Checks before data
FREE with learning rate 0 = FROZEN bit for bit; ANCHOR's penalty 0 at the RMS weights; REHEARSE and REPLAY schedules as
stated; B differs from A only as stated (code diff); determinism; resume.

## Limits (written now)
Written hunger and sleep reflexes may mask brain decline (GPT); 1M steps is not a lifetime; one B; no larger brain arm
(deferred, GPT and Gemini).

## Expected (before data)
FREE gains in B: about 50%. At least one protection passes both parts: about 35%.
