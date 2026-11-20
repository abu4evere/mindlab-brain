# W3m findings: the body's own mind (20 November 2026)

**Plan:** `questions.md` (W3m-frozen; council `../W3m_council_2026-11-19.md`; the creator's idea, 19 Nov: "the brain has two
minds, one ours and one the brain's own … if we do not want to sleep we eventually sleep"). Checks All: PASS before
data and in all 80 cloud check logs. 48 cloud jobs (SL, SR, UR × 16 seeds); the manager froze for about 6 hours on the
evening of 19 November and was restarted (no data lost; its GitHub calls now time out and retry). All closed 05:25.
- The frozen `analyse_w3m.py` gives `analysis.md`. n = 16 seeds × 50 test lives (and 50 fresh lands).
- **Recompute:** the assistant recomputed both primary readings with a separate short script and another bootstrap seed:
  the same means, interval ends within 5 steps.
- The control is W3k (R2, CS, CY): with both parts off, `w3m.py` trains W3k's run R bit for bit (checked before data).

## The frozen readings
| arm | what | lifespan | survived | fresh lands: survived | steps exhausted |
|---|---|---|---|---|---|
| CS (W3k) | no inborn part, kept copy | 1,835 | 0.478 | 0.445 | 0.163 |
| **SLS** | **the sleep reflex**, kept copy | **2,223** | **0.614** | **0.646** | **0.061** |
| SLS-off | the same brain, reflex switched off at test | 1,594 | 0.353 | 0.359 | 0.174 |
| SRS | rest only (held at the shelter once there) | 1,852 | 0.444 | 0.425 | 0.141 |
| URS | the tiredness urge (reward only) | 1,841 | 0.473 | 0.464 | 0.163 |

1. **Primary readings (97.5% intervals):**
   - **"The sleep reflex helps" (SLS − CS): +388 [+101, +689]. Yes.** 12 of 16 seeds; every leave-one-seed-out mean
     +308 to +454.
   - **"The tiredness urge helps" (URS − CS): +6 [−265, +304]. No.**
2. **Secondary (95%):** SL − R2 +586 [+263, +909], yes (the end brains agree); SLS − SRS +371 [+186, +522], yes (the
   way-finding matters: holding the brain at the shelter is not enough); SRS − CS +17, no; UR − R2 +33, no;
   SLS-off − CS −241 [−458, +21], no (the brain did not learn to rest by itself; without its reflex it is slightly worse);
   steps exhausted SLS − CS −0.102 [−0.129, −0.076], lower.
3. **Toward the bar:** SLS's fresh-land survival **0.646 [0.569, 0.708], the best yet** (W3l's C5S 0.559). The bar is 0.80.

**The priors** (frozen): SLS − CS above 0, about 75% (GPT 75%): yes. URS − CS, about 35%: no. SRS − CS, about 45%: no.
SLS-off − CS, about 25%: no. SLS exhausted less than CS, about 90%: yes. Any arm at 0.80 on fresh lands, about 15%: no.

## The deaths (share of deaths with each label; labels overlap)
| | deaths per 50 | no food known | food known within 30 steps, not reached | exhaustion |
|---|---|---|---|---|
| CS | 26.1 | 0.47 | 0.66 | 0.66 |
| SLS | **19.3** | 0.35 | **0.83** | **0.25** |
The reflex takes over 4% of test steps. Exhaustion is no longer the main killer; **hunger near known food is**.

## What it means (the assistant's reading)
1. **The creator's "two minds" idea works.** A body that makes the brain rest, the way a body makes a person sleep,
   raises survival on unseen lands from 0.45 to 0.65 and cuts deaths by a quarter.
2. **The body's way-finding is the active part** (SLS − SRS +371): forcing rest only when the brain already stands at
   the shelter does nothing measurable.
3. **A reward alone does not do it** (URS: a tiredness urge adds nothing), as the council expected.
4. **The brain leans on its reflex** (SLS-off below CS): like sleep in animals, it is the body's job, not learned.
5. **Next: W3n** (prepared, council-reviewed): the same move for hunger (a hunger reflex), cheaper rest (the creator's
   idea), and both.
