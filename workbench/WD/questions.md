# WD: the doubting test (can the brain learn not to believe a wrong teacher?) (plan, frozen before any code or data)

**Frozen** as git tag `WD-frozen`, before any code or data.
- **The creator** (14 November 2026), on critical thinking: "can our agent develop that skill too? … if you give them
  those type of questions like something that makes something think what its gonna do?". On 15 November: "go ahead
  … we gotta work like yesterday find something useful".
- **Background** (abstracts only, `D:\acl\docs\research\mindlab_sources_2026-11-15.md`):
  - Enquist, Eriksson and Ghirlanda (2007): "critical social learning" (copy, and learn alone when the copy fails)
    beats pure copying;
  - Koenig and Harris (2005): children learn to mistrust inaccurate speakers.
- **Exploratory:** no council.

## The world
- **WS's boxes, with codes that never change:** 6 kinds, 2 lids, 3 tries per kind per day, 60 days.
- **The teacher:** present on each try of days 1–30 with probability 0.5 (WT's draws `[seed, 5, day]`); none after
  day 30.
- **The teacher is wrong on kinds 0–2 ("bad kinds")** and always shows the same wrong code there. The wrong code is
  WC's new-code draw (`[seed, 8]`): each lid's pair differs from the true pair. On kinds 3–5 ("good kinds") the
  teacher is right.

## The brain: the recipe (WR's LTYR)
- **L:** learn without the showing in mind.
- **T:** don't repeat a failure.
- **Y:** "that worked!".
- **R:** a fast memory replayed at night.

Sizes 32 and 128; 48 children each (seeds 1–48).

## Arms
- **Naive:** copies every showing (copy rate 0.5), as WR.
- **Doubt (critical copying):**
  - each kind has a trust t, starting at 1.0 (children start by trusting adults);
  - the copy step's rate is 0.5 × t;
  - **after each practice try on a teacher-present try, for each lid the child tried:**
    - its pair equals the teacher's shown pair: o = 1 if the lid opened, 0 if not;
    - its pair differs and the lid opened: o = 0 (its own success contradicts the teacher);
    - its pair differs and the lid failed: no update.
  - Then t += 0.3 × (o − t) for each update.
  - A general mechanism (trust from checked results, as in Cradle C2-S), not a rule about boxes.
- **Alone:** never copies (the teacher is ignored); the recipe learns from its own tries only.

## Measures (descriptive; 95% bootstrap intervals over seeds, paired; numpy seed 20261127)
- Own skill (full boxes, no showing; WS's test) on bad kinds and good kinds at days 15, 30, 45 and 60.
- **Believing the teacher:** the share of bad kinds whose first lid gets the teacher's wrong pair, at days 15, 30 and
  60.
- Doubt's trust at day 30 (mean over bad kinds and over good kinds). Lifetime food.
- **Paired differences** (Doubt − Naive, Doubt − Alone, Naive − Alone) on bad kinds and good kinds at days 30 and 60.

## The assistant's prior
- Naive is misled: on bad kinds at day 30, below Alone (interval below 0): about 60%.
- **Doubt beats Naive on bad kinds at day 30** (interval above 0): about 65%.
- Doubt loses at most 0.05 to Naive on good kinds at day 30: about 70%.
- Doubt's trust at day 30 is below 0.3 on bad kinds and above 0.7 on good kinds: about 55%.
