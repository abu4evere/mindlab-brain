# V2-3 Keep learning for life, with protection (DRAFT, not frozen; for the council)

Drafted 28 Nov 2026 (EST, early) under the creator's sleep-mode autonomy, as the next Brain v2 step after V2-2's
negative result (`brain_v2/V22/findings.md`), which moved this step ahead of another goal attempt.

## Why
V2-2: every walker that kept learning as an adult (1M steps of actor-critic in CW2's world, no parent) lost a little on
the Bob Profile, with or without a goal part (A5s about −0.10, R2 −0.07 to −0.11), while plain survival hardly moved.
People keep learning all life without losing what they knew; Bob's walker cannot yet. The roadmap (V2-3) and the v1
plan's G0 -> G1 ("grow and protect") name this as the next problem.

## The question
Can the walker (RMS, W3n's DriveVIN) keep learning in a new world as an adult, gaining there, while keeping its old
abilities (the Bob Profile and survival in its home world)?

## Worlds
- **Home (A):** W3r's lands (changing colours), where RMS was raised.
- **New (B):** the same lands with food scarcer: regrowth R doubled (food takes twice as long to come back). A world
  change, not a new rule (Mind Lab only; ACL untouched). The frozen walker survives less there (to be measured in the
  pilot on pilot lands, before data); learning should help.

## Arms (16 seeds = RMS 1-16; each fine-tuned for the same steps in B, the V2-2 loop without hands or goal)
| arm | adult learning in B | protection |
|---|---|---|
| **FROZEN** | none | — |
| **FREE** | actor-critic, as V2-2 | none |
| **ANCHOR** | the same | a pull back toward the RMS weights, weighted by how much each weight mattered at home (an EWC-style penalty: importance = squared gradients of the policy on home lives, measured before fine-tuning) |
| **REHEARSE** | the same, but every other life is lived at home (A) with learning on | interleaved home practice (the brain's own experience, no parent) |
| **SLOW** | the same with the learning rate x0.1 | none (controls for "just learn less") |

## Measures (draft)
- **Primary (two parts, both needed):** (a) gain in B: full-life survival in B, arm − FROZEN; (b) no loss at home: the
  Bob Profile vs RMS (V2-2's rule: no test with the lower end below −0.05) and home survival arm − FROZEN above −0.03.
  The question is answered yes for an arm only if both hold. Main comparison: ANCHOR and REHEARSE against FREE.
- Secondary: the size of the B gain per arm; which Bob Profile tests move; weight drift from RMS.

## Checks before data
FREE with learning rate 0 = FROZEN bit for bit; ANCHOR's penalty is zero at the RMS weights; REHEARSE alternates worlds
as stated; B differs from A only in R (code diff); determinism; the V2-2 loop reused unchanged except for these parts.

## Compute
4 fine-tuned arms x 16 seeds x up to 1M steps (V2-2: ~2.5 h per run on Oracle); tests: B and A lives, the Bob Profile.
About 10-12 hours on the three machines.

## Questions for the council
1. Is "food twice as slow" a good new world (it changes a number, not a rule), or should B be something else?
2. ANCHOR (importance-weighted pull to old weights) and REHEARSE (alternating home lives): the right protections to test
   first? Anything missing (e.g. a larger fixed brain, a replay buffer of old states)?
3. Is a two-part primary (gain in B AND no home loss) right, and is SLOW the right control?
4. How long should adult learning run, given V2-2's 1M steps?
5. What would make a positive result misleading?

## Expected (before data)
Some gain in B for FREE: about 50%. ANCHOR or REHEARSE passing both parts: about 40%.
