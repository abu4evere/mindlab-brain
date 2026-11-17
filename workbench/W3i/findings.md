# W3i findings: more practice, a longer childhood (17 November 2026, about 07:15)

**Plan:** `questions.md` (W3i-frozen; council `../W3i_council_2026-11-16.md`). Checks All: PASS (8) before data.
- **Runs:** 25 cloud jobs. The 6M runs paused and resumed once or twice. All closed at 06:55.
- The frozen `analyse_w3i.py` gives `analysis.md`. n = 8 seeds × 50 test lives.
- **The reproduction job is exact:** W3d's PYFR seed 1, trained again on GitHub, gives identical weights (max
  difference 0.0).

## The frozen readings
| arm | training | fade | lifespan | survived | to 1,000 | fresh lands: survived | "no food known" (deaths) |
|---|---|---|---|---|---|---|---|
| PYFR (W3d) | 2.0M | 0.4M | 806 | 0.128 | 0.243 | – | 0.80 |
| L | 6.0M | 0.4M | 603 | 0.098 | 0.155 | | 0.73 |
| LC | 6.0M | 1.2M | 980 | 0.188 | 0.315 | | 0.64 |
| **C** | 2.8M | 1.2M | **1,248** | **0.255** | **0.405** | **0.235** | 0.61 |

1. **"More practice helps": no.** L − PYFR −203 [−614, +146].
2. **"A longer childhood helps, with equal practice": yes.** LC − L +377 [+37, +707].
3. **Secondary:** C − PYFR +442 [+43, +889].
4. **Toward the bar:** the best arm is C. On 50 fresh lands it survives 0.235 [0.128, 0.340], against the bar of 0.80.
5. **The failure shifts a little:** "no food known" deaths fall from 0.80 (PYFR) to 0.61–0.64 (C, LC).

**The priors:**
- reading 1 (about 50%): no;
- reading 2 (about 35%): yes;
- the best arm reaches 0.80 (about 2%): no.

## The learning curve (exploratory: snapshots at 2M and 4M)
| | 2M | 4M | 6M |
|---|---|---|---|
| L (fade 0.4M) | 840 / 0.143 | 598 / 0.090 | 603 / 0.098 |
| LC (fade 1.2M) | **1,340 / 0.260** | 915 / 0.153 | 980 / 0.188 |

(lifespan / survival)
- **Both peak early and then fall.** The brain's own learning after childhood slowly wears away what the parent
  taught.
- This matches W3h, where a careful parent's lesson faded once the parent had gone, unless pain held it.
- The best brains are the ones tested soon after a long childhood: C at 2.8M, and LC's 2M snapshot.

## A flaw in a frozen measure (stated, not hidden)
- **"Stale arrivals" is 0 in every arm, and cannot be anything else.** The 3 × 3 view always shows a cell before the
  brain can step onto it, so the memory is corrected one step before arrival.
- The check passed because it set up an impossible case (remembered food next to the brain without the view
  updating). The measure was ill-defined from the start.
- An exploratory replacement, "disappointments" (remembered food found gone when it comes back into view), follows
  below.

## Exploratory (after the data, labelled): disappointments
- **What is counted:** a cell remembered as full food that turns out empty when it comes back into view, not counting
  the cell just eaten.
- **How:** the test lives were replayed exactly. The replayed lifespans equal the frozen ones: 806, 603, 980 and 1,248.

| | PYFR | L | LC | C |
|---|---|---|---|---|
| disappointments per 1,000 steps | 0.04 | 0.04 | 0.17 | 0.19 |

- **Disappointments are rare:** about once in 5,000 to 25,000 steps. They are a little more common in the longer-lived
  brains, which go back to remembered food more often.
- **So the council's worry (stale memory) is not the main failure.** The main failure stays WX's: the brain dies
  knowing of no food at all. Eaten cells look empty in memory until they are seen again, so a brain that has eaten
  its patches knows of nothing, unless it goes back to look.

## What it means (the assistant's reading)
1. **The parent matters more than the practice.** A longer childhood is the strongest lever found so far: lifespan
   806 → 1,248 and survival 0.128 → 0.255. Practice alone, after childhood, makes the brain worse, not better.
2. **Why practice hurts (a hypothesis, to test):** after the parent goes, the only teacher is the brain's own sparse
   feelings, plus "that worked!" and replay. Those slowly overwrite the parent's policy with a worse one: the
   same erosion W3f saw between generations, and W3h within a life.
3. **Next steps this suggests:**
   - keep what the parent taught: a lower learning rate after childhood, or a regulariser that keeps the policy near
     the childhood policy (as in "learning without forgetting");
   - a still longer childhood (the curve has not yet been seen to peak);
   - pain kept on (W3h).
4. **The bar:** 0.235 survival on fresh lands, against 0.80. Real progress (×1.8 in one rung), still far.
