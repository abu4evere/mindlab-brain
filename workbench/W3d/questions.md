# W3d: learning to live from a parent (plan, frozen before any code or data)

**Frozen** as git tag `W3d-frozen`, before any code or data.
- **Sign-off:** the assistant, under the creator's sleep-mode autonomy. The creator: "alr bro keep it pushing i will
  sleep", 15 November 2026, about 23:0x.
- **Council:** `../W3d_council_2026-11-15.md` (Gemini, ChatGPT, DeepSeek). All three call it a fair, useful rung; the
  teaching fades (their shared change).
- **Exploratory,** in the W3 series.

## Why
- **W3–W3c:** brains taught only by their own feelings never learned to live. The best was one seed with 5 of 50 full
  lives (W3c, GYFR).
- Every box test that worked had a teacher plus copying, with the showing not held in mind (WS, WL2, WR).
- W3's Script reads only the child's own senses (the map memory, its body and position) and survives 0.96, so it is a
  fair parent.

## The world, body, drives, brain and test
W3's, unchanged (W3b's training loop and test, `../W3b/w3b.py`). The brain is W3's D3 class, ungated.

## The parent's teaching (the only new part)
- **On every training step while the parent is present:** the parent (a W3 Script, one per life, kept in step with the
  child's own life) is shown the child's map view and says what it would do.
- **Every 4th step,** the child takes one supervised copy step toward that act, in its own situation, using W3b's
  `imitate` (the planner and head learn; the critic does not), with weight w.
- **Nothing of the parent's choice enters the child's senses or memory;** the child acts by itself and learns from its
  feelings as in W3.
- **Weights:**
  - **P:** w = 0.5 × (1 − t / 400,000) for t < 400,000 (fading to zero over childhood); none after.
  - **PA:** w = 0.5 on every 4th step for all 2,000,000 steps (the parent who never leaves).

## Arms (8 seeds, 2,000,000 steps, GitHub's machines)
| arm | what |
|---|---|
| **P** | parent childhood (fading) |
| **PYFR** | parent childhood + W3b's "that worked!" (Y) and rest replay (FR), unchanged |
| **PA** | the parent all life (weight 0.5, every 4th step) |
| cited | W3's D3; W3b's Y+FR (the same seeds, lands and tests) |

## Readings (95% bootstrap intervals over the 8 seeds, paired; numpy seed 20261130)
1. **"A child taught by a parent lives":** P or PYFR survives with mean ≥ 0.50 and lower bound ≥ 0.30.
2. **"The parent helps":** P − D3 on survival (or lifespan if every survival is 0) has a lower bound above 0.
3. **"The recipe adds":** PYFR − P (the same rule), reported with its interval.
4. **"A parent who never leaves":** PA − P, reported. Is the child weaker on its own?
- **Interpretation rule (council):** survival here shows that a parent's teaching can bootstrap a policy, not that
  feelings alone teach it.

## Validity (hard stops)
- **Checks All: PASS before data:**
  - with no parent (childhood 0, no PA), the loop reproduces W3b's D3 training exactly;
  - copy steps happen only on every 4th step, only while the parent is present, with the planned weights;
  - the parent sees only the map view;
  - a split run equals an unsplit run;
  - the same seed twice is the same.
- Every run finishes, or is reported.

## The assistant's prior
- Reading 1: about 40% (the council: 65%, 35%, 15–20%).
- Reading 2: about 80%.
- Reading 3 (PYFR above P): about 40%.
- PA worse than P: about 35%.
