# W3k findings: a longer childhood still, and keeping the adult's best (18 November 2026, about 21:30 UTC)

**Plan:** `questions.md` (W3k-frozen, with amendments 1 and 2 made before any data; council
`../W3k_council_2026-11-18.md`). Checks All: PASS (16) before data.
- **Runs:** 50 cloud jobs (16 seeds × run "R", "C3" and "CR", and the two determinism jobs). Long runs paused and
  resumed; one cancelled run was retried. All closed at 16:10 on 18 November (local time).
- The frozen `analyse_w3k.py` gives `analysis.md`. n = 16 seeds × 50 test lives.
- **Recompute:** the assistant recomputed the primary and secondary readings with a separate short script and a different
  bootstrap seed: the same means, and interval ends within 6 steps.
- **The determinism job is exact.** R seed 1 trained three times, on different machines (Intel Xeon 6975P; Intel 6975P then 8370C; AMD EPYC 7763), gives bit-identical weights
  (largest difference 0.0). So, unlike W3j, the pairing by seed is real: R2, CS and CY are the same brain at different
  steps, and C3, CR and R2 are the same brain up to their split.

## The frozen readings
| arm | what | lifespan | median | survived | to 1,000 | fresh lands: survived | drift | agrees with the parent |
|---|---|---|---|---|---|---|---|---|
| W3j's C2 (cited) | 4.0M steps, 2.4M fade | 1,594 | | 0.363 | 0.535 | 0.380 | 0.51 | 0.31 |
| R2 | C2 again, the brain at the end | 1,636 | 1,634 | 0.409 | 0.548 | 0.391 | 0.52 | 0.30 |
| **CS** | the same run; **the copy kept by its own lives** | **1,835** | 1,885 | **0.478** | **0.611** | **0.445** | 0.47 | 0.33 |
| CY | the same run; a copy at a step drawn in advance | 1,792 | 1,841 | 0.450 | 0.604 | 0.448 | 0.46 | 0.33 |
| C3 | 5.2M steps, 3.6M fade | 1,753 | 1,869 | 0.429 | 0.600 | 0.460 | 0.48 | 0.31 |
| CR | R2, plus replay of stored parent examples after the fade | 667 | 662 | 0.039 | 0.176 | 0.034 | 0.34 | 0.54 |

1. **Primary readings** (97.5% intervals):
   - **"A longer childhood still helps" (C3 − R2): +117 [−193, +432]. Not shown.** It points the right way (11 of
     16 seeds; every leave-one-seed-out mean is positive, +31 to +178), but the interval includes 0.
   - **"Choosing its own best copy helps" (CS − R2): +199 [+70, +347]. Yes.** 12 of 16 seeds; leave-one-seed-out
     means +155 to +223.
2. **How to read the CS win (CS − CY): +43 [−21, +109]. Not shown.** A copy taken at a step drawn in advance does
   almost as well (CY − R2 +157 [+33, +285]). So the win comes from **taking an earlier copy instead of the worn-down
   end**; the brain's own lives adding information about *when* it was best is not shown.
3. **Secondary:** "remember the parent" (CR − R2): **−969 [−1,196, −753]. No: it hurts badly.** The brain agrees with
   the parent more (0.54 against 0.30) and lives a third as long.
4. **Toward the bar:** the best arm by lifespan is **CS, the best brain yet**: full lives 0.478, fresh-land survival
   0.445 [0.364, 0.524] (W3j's C2: 0.380). The bar is 0.80.

**The priors** (the assistant's, frozen): C3 − R2 above 0, about 50%: not shown. CS − R2 above 0, about 55%: yes.
CS − CY above 0, about 40%: not shown. CR − R2 above 0, about 25%: no. Any arm at 0.80, about 3%: no. The
determinism job bit-identical, about 60%: yes.

## Exploratory (labelled; not frozen readings)
- **The learning curves** (tested snapshots, mean lifespan):
  - R: 2.4M 1,208 → 2.8M 1,821 → **3.2M 1,868** → 3.6M 1,718 → end (4.0M) 1,636: the peak-then-decline seen in W3i
    and W3j, now on bit-identical runs.
  - C3: 3.6M 1,454 → 4.0M 1,756 → 4.4M 1,769 → 4.8M 1,743 → end (5.2M) 1,753: after the longer childhood the curve
    **stays flat** instead of declining.
  - CR: 888 → 511 → 651 → 683 → 667: the replay pulls it down from the first snapshot.
- **The upper bound:** choosing, per seed, the best tested snapshot of run R (by the test itself, so not a fair
  result) gives 1,931 [1,696, 2,135]. CS (1,835) recovers about two thirds of the gap between the end (1,636) and
  this bound.
- CS's kept copy comes from 2.7M to 3.8M steps (mean 3.2M), close to the curve's peak.

## What it means (the assistant's reading)
1. **Runs are now exactly repeatable.** Amendments 1 and 2 worked: the same seed gives the same brain on Intel and
   AMD machines. Every Mind Lab study from here can trust its pairing.
2. **Keeping an earlier copy is a real, cheap gain** (+157 to +199 steps). The brain is better soon after its
   childhood than at the end of its adult learning, so keep a copy from that window. The simple rule ("keep the copy
   while your recent lives are longest") works, though a copy from a fixed window works about as well.
3. **The longer childhood keeps its lesson.** C3 is not separated from R2 on lifespan, but its curve no longer
   declines after childhood, and its fresh-land survival is the highest (0.460). It is a likely partner for CS.
4. **Copying the parent after childhood hurts, in every form tried:** a quiet live parent (W3j's CV) and now replayed
   examples (CR). Copying fights the brain's own learning. The parent belongs in childhood only.
5. **Where the brain stands:** full lives 48% of tests, fresh lands 45% (bar 80%). From W3d's start (fresh lands 0.13)
   the brain has come about half way.
6. **Next, for the brain plan:** C3's longer childhood together with CS's kept copy, on 16 seeds; and a look at what
   still kills the brain (the death causes), to find the next lever.
