# W3n findings: the body's own mind, part 2 (22 November 2026)

**Plan:** `questions.md` (W3n-frozen; councils `../W3n_council_hunger_2026-11-19.md`, `../W3n_council_2026-11-20.md`;
cheaper rest is the creator's idea).
- **Checks:** All: PASS before data (`checks.log`, copied from a cloud run's passing log).
- **Runs:** 48 (CR, HR, HC × 16 seeds), split across machines after GitHub disabled the repository on 20 Nov
  (`MOVED_TO_LOCAL.md`):
  - 33 run parts on GitHub's machines (Intel Xeon 6975P);
  - 8 on the Google Cloud VM (Intel Xeon 2.80 GHz);
  - 7 on the creator's PC (Windows).
- **Machines:** the Linux machines train bit-identically to one another (W3k's determinism job; W3o's machine_check);
  the PC differs in the last digits. Every run is a valid sample of its arm; the machine of each run part is recorded
  in `output/machine_*.json`.
- The frozen `analyse_w3n.py` gives `analysis.md`. n = 16 seeds × 50 test lives (and 50 fresh lands).
- **Recompute:** `recompute_w3n.py` is a separate script (another bootstrap seed, and a t interval beside it). It gives
  the same means and interval ends within 5 steps; the t intervals agree on every verdict.

## The frozen readings
| arm | what | lifespan | fresh lands: survived | steps hungry | deaths per 50 |
|---|---|---|---|---|---|
| SLS (W3m) | sleep reflex only, kept copy | 2,223 | 0.646 | 0.041 | 19.3 |
| **HRS** | **+ hunger reflex** | **2,749** | **0.884 [0.861, 0.905]** | 0.013 | 6.1 |
| CRS | + cheaper rest | 1,612 | 0.269 | 0.073 | 35.8 |
| **HCS** | **both** | **2,789** | **0.902 [0.873, 0.929]** | 0.011 | 4.7 |
| HRS-bare | HRS's brain, both reflexes off | 1,662 | 0.390 | 0.061 | 31.8 |
| SLS-off (W3m) | SLS's brain, reflex off | 1,594 | 0.359 | 0.069 | 32.4 |

1. **Primary readings (97.5% intervals, Bonferroni):**
   - **"The hunger reflex helps" (HRS − SLS): +527 [+346, +742]. Yes.** 15 of 16 seeds; every leave-one-seed-out mean
     +461 to +563. Recompute: +526.5 [+341.7, +743.2]; t [+296, +757].
   - **"Cheaper rest helps" (CRS − SLS): −610 [−796, −355]. No, the opposite: it hurts.** 1 of 16 seeds above 0.
     Recompute: −610.2 [−796.2, −351.9].
2. **Secondary (95%):**
   - HR − SL +309 [+37, +620], yes (the end brains agree).
   - HCS − HRS +40 [−50, +149], no: with the hunger reflex, cheaper rest adds nothing.
   - CRS-old − SLS −753, no: CR's brain does worse still when rest costs full price again (it adapted to cheap rest).
   - HRS-off − SLS +106 [−69, +320], no; HCS-off − SLS +176 [−5, +370], no.
   - **The brain alone did not improve:** HRS-bare − SLS-off +68 [−83, +232], no; HCS-bare − SLS-off +108
     [−69, +273], no.
   - Steps hungry, HRS − SLS −0.028 [−0.039, −0.020], lower.
3. **Toward the bar (fresh-land survival 0.80):**
   - **HCS 0.902 [0.873, 0.929] and HRS 0.884 [0.861, 0.905]: both above 0.80, lower bounds included. The first W3
     brains to pass the survival part of the ACL readiness bar.**
   - This is the whole agent, the brain with its body's two reflexes. Without them, the same brains survive 0.38–0.39.

**The priors** (frozen):
- HRS − SLS above 0: about 80% (GPT 85%). Yes.
- CRS − SLS above 0: about 25% (GPT 60%). No, and far below 0.
- HCS − HRS above 0: about 20%. No.
- HRS-bare − SLS-off above 0: about 30%. No.
- Any arm at 0.80 on fresh lands: about 40% (GPT 55%). Yes.

## What it means (the assistant's reading; the creator decides)
- **A narrow hunger reflex works.** It walks the body to the nearest remembered food at energy 80 and lets go after one
  meal; it takes under 1% of test steps. Deaths fall from 19 to 6 per 50 lives. The remaining deaths are almost all
  "no food known" (0.98): the food moved and nothing remembered is left. The next limit is searching, not reaching.
- **Cheaper rest backfired.** With rest costing half, the sleep reflex took 10% of steps (4% in SLS); the brains were
  hungry nearly twice as often (0.073 against 0.041), and deaths doubled. Cheap rest made resting too attractive to a
  brain that learns what pays. A real trade-off, not a bug. With the hunger reflex beside it (HC), the starvation is
  prevented and cheap rest becomes harmless, but not useful.
- **The gains are the body's, not the brain's.** With the reflexes off, every W3n brain is back near W3m's (0.38).
  The Bob Profile says the same: the living brain alone scores 6/100 (`../../scorecard/bp/findings_HRS_2026-11-21.md`).
  W3p (a planner that must plan) works on the brain itself.

## Recorded honestly
- The measure "arrivals at remembered food that had gone" reads 0.00 for every arm. It is probably not counting in
  these arms (W3i's StaleWorld counter under W3n's world). It is not used here and should be checked before reuse.
- The handoff's "about 1 day" for the local runs was wrong. They took about 2 days on the PC and the Google VM.
