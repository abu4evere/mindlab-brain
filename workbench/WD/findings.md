# WD findings: the doubting test — the recipe brain is not fooled by a wrong teacher (exploratory; `analyse_wd.py`)

Plan: `questions.md` (WD-frozen). Checks All: PASS before data. Run 15 November 2026, 14:13–14:17, locally at Idle;
48 children per cell. Full table: `analysis.md`. Mind Lab: exploratory, no council, no blind recompute.

## Results (own skill, no showing; bad kinds = the teacher shows a wrong code)
| arm | size | bad kinds d15 / d30 / d60 | good kinds d15 / d30 / d60 | believes the wrong code (d15, d30, d60) | food |
|---|---|---|---|---|---|
| Naive (copies everything) | 32 | 0.63 / 0.99 / 1.00 | 0.85 / 1.00 / 1.00 | 0.00, 0.00, 0.00 | 1737 |
| Doubt (trust from checked results) | 32 | 0.62 / 0.99 / 1.00 | 0.85 / 1.00 / 1.00 | 0.00, 0.00, 0.00 | 1746 |
| Alone (never copies) | 32 | 0.58 / 0.98 / 1.00 | **0.56** / 0.98 / 1.00 | 0.00, 0.00, 0.00 | 1690 |
| Naive | 128 | 0.82 / 1.00 / 1.00 | 0.99 / 1.00 / 1.00 | 0.00, 0.00, 0.00 | 1880 |
| Doubt | 128 | 0.84 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 | 0.00, 0.00, 0.00 | 1891 |
| Alone | 128 | 0.83 / 1.00 / 1.00 | **0.76** / 1.00 / 1.00 | 0.00, 0.00, 0.00 | 1838 |

- **Doubt's trust at day 30:** bad kinds 0.000 [0.000, 0.000], good kinds 1.000 [1.000, 1.000] at both sizes. Doubt
  identified the wrong teacher perfectly.
- **Doubt − Naive:** every difference is between −0.007 and 0.000 (bad kinds at days 30 and 60; good kinds; believing).
- **The priors:**
  - "Naive is misled" (about 60%): **no**;
  - "Doubt beats Naive on bad kinds" (about 65%): **no**;
  - "Doubt costs at most 0.05 on good kinds" (about 70%): **yes**;
  - "trust below 0.3 on bad kinds and above 0.7 on good ones" (about 55%): **yes**.

## What it means (the assistant's reading)
- **The recipe brain is already a critical learner,** without any trust mechanism.
  - It copies the teacher, tries, and when the copied move fails, "don't repeat a failure" blocks it. The search finds
    the right move, "that worked!" writes it in, and the night replay keeps it.
  - The wrong teacher never wins: no child at any size believed the wrong code on any test day.
  - This is close to Enquist et al.'s "critical social learning" (copy, and learn alone when the copy fails).
- **A good teacher still helps:** on good kinds at day 15, the copier is far ahead of the child who learns alone
  (0.85 against 0.56 at size 32; 0.99 against 0.76 at size 128).
  - So the recipe takes the help of a right teacher and shrugs off a wrong one.
- **The test was easy for doubt:** a wrong code fails at once and visibly.
  - Harder cases are untested: a teacher who is right on one lid but wrong on the next; one who is right only
    sometimes; or a mistake whose cost comes late.
  - Those are where explicit trust might matter.

## Limits
One task; the error is visible at once; one fixed wrong code per bad kind; codes never change.
