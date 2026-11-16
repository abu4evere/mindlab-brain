# WQ findings: the silent room (exploratory; numbers from `analyse_wq.py`)

**Plan:** `questions.md` (WQ-frozen; the creator's question). Checks All: PASS before data.
- Run 15–16 November 2026 on GitHub's machines (10 jobs, all succeeded; 73 files).
- n = 8 seeds × 3 rooms × 10,000 steps per cell; Script is one deterministic run per room.
- Mind Lab: exploratory, no council, no blind recompute. "w1" is the first 1,000 steps, "w10" the last.

## 1. No brain answered silence with silence
- **Every brain kept moving to the end:** activity in the last window ran from 0.60 (D2, still) to 0.93 (Dc, living).
- **The ones with nothing to feel (D2: hunger and tiredness, both always 0) slowly settled:**
  - activity fell 0.682 → 0.602 (w10 − w1 −0.080 [−0.119, −0.045]);
  - they kept to a smaller part of the room than a random mover (reach 69 cells against 121; D2 − Rand −52
    [−65, −39]).
- **Curiosity alone (Dc) did the opposite:** it became more restless.
  - Activity rose 0.81 → 0.92 (+0.106 [+0.059, +0.161]), and it ranged as widely as a random mover (reach 122 against
    121).
  - Dc − D2 at w10: activity +0.318 [+0.229, +0.399]; reach +53 [+38, +67].
- **D3** (all three feelings, curiosity diluted) behaved like D2 when still: reach −0.8 against D2, interval about 0.

## 2. The recipe brain paced in a tight loop
- **GYFR** (W3c: all three feelings plus "that worked!" and rest replay), weights fixed:
  - **visited only about 9 cells per 1,000 steps** (reach 9.3; GYFR − D2 −60 [−75, −44]);
  - **with the most repetitive movement of any learned brain** (pattern 0.124 against Rand's 0.397; GYFR − D2 −0.241
    [−0.305, −0.159]).
- **It kept moving** (activity 0.65), round and round a small circuit.
- **Allowed to keep learning (living),** the loop loosened: activity +0.203 [+0.064, +0.355], reach +19 [+3, +39],
  less repetitive (+0.096).
- **The hand-written Script patrols by rule:** pattern 0.066, the most repetitive of all, and reach 73.

## 3. Living (learning continues) made the curiosity-trained brains roam more
- D3 living − still: activity +0.114 [+0.034, +0.207]; reach +43 [+25, +62]. Its activity no longer fell (w10 − w1
  +0.043).
- Dc changed little (it was already restless).
- D2 (reward always 0) moved slightly toward random (pattern +0.020 [+0.007, +0.036]).

## The priors
- "D2 keeps moving at its noise level, with no clear fall" (about 60%): **partly.** It kept moving, but it did slow
  and narrow.
- "D3 and Dc reach more than D2" (about 70%): **Dc yes, D3 no.**
- "The curiosity brains are more patterned than random" (about 60%): **yes,** strongly for GYFR, slightly for D3 and
  Dc (−0.047 and −0.015 against Rand).
- "Living makes D2 more random" (about 50%): **yes, slightly.**

## What it means (the assistant's reading)
- **These brains never fall silent,** but for different reasons:
  - **D2 and D3:** they act by sampling, so they keep drifting. With nothing to want, they drift less and keep to a
    smaller corner.
  - **Curiosity:** it turns silence into restlessness. The emptier the room, the more the brain roams to re-check what
    has gone stale. That is how W3 defined curiosity (staleness), so part of it is built in.
  - **The recipe brain, which learned to repeat what worked, settled into a tight, repeated circuit.** In animals,
    repetitive pacing in a bare enclosure is called a stereotypy.
  - Whether anything like boredom or distress lies behind it cannot be said: **this is behaviour, not feeling.**
- **The creator's question ("will it answer silence with silence?"):** no. But nothing here invents new activity
  either (no talking to itself, no games). They roam, drift or pace. Inventing needs an inner source of input
  (imagination) and a drive to learn something new, which these brains lack.
- **Next (the creator's choice):**
  - an imagination part (replaying and recombining memories in idle time);
  - a "learning progress" curiosity (wanting to get better at something, not only to see what is stale);
  - then the silent room again.

## Limits
- One room type; 10,000 steps; W3's curiosity definition; no imagination; no inner speech is possible here.
