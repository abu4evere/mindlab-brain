# W3n: the body's own mind, part 2: cheaper rest and a hunger reflex (plan, frozen before any study data)

**Frozen** as git tag `W3n-frozen`.
- **Sign-off:** the creator (20 Nov 2026), after choosing cheaper rest and accepting three arms: "ok bro whatever you say";
  then "keep working". The hunger reflex was put to GPT and Gemini neutrally the evening before (both picked it).
- **Council:** `../W3n_council_hunger_2026-11-19.md` (the options) and `../W3n_council_2026-11-20.md` (this plan: GPT;
  Gemini's answer did not load). Draft: `../W3n_draft.md`.
- **Exploratory,** in the W3 series. Calibration used only W3's calibration lands.

## Why (W3m, final)
The sleep reflex (SLS) raised fresh-land survival from 0.445 to 0.646 (SLS − CS +388 [+101, +689]) and cut exhaustion
deaths from 0.66 to 0.25. Hunger now kills: 83% of SLS's deaths had remembered food within 30 steps.

## Arms (`w3n.py`: W3m's SL = W3k's run R, 4.0M steps, 2.4M fade, the sleep reflex; kept copies; 16 seeds)
| arm | the new part |
|---|---|
| **CR, cheaper rest** (the creator's) | a step resting at the shelter costs 0.5 energy (was 1): the body's energy economy changes |
| **HR, hunger reflex** | at energy 80 or less, with food in the map memory, the body walks the shortest known way to the nearest remembered food and hands control back once it has eaten (or when none is left); it wins over the sleep reflex while on (each interruption counted); it reads only the map memory, so a moved patch is walked to in vain |
| **HC** | both |
| SL, SLS, SLY, SLS-off (W3m, cited) | with both new parts off, `w3n.py` trains W3m's SL bit for bit (checked) |

- **Calibration** (`calib_n.py`, calibration lands 800001–800050 only; W3m's SL kept copies seeds 1, 2, 3, 6, the hunger
  reflex added at test): full lives 0.59 without it; 0.795, 0.775, 0.785, 0.80 at lines 50, 60, 70, 80; lifespan
  2,602 / 2,610 / 2,571 / **2,616**. Line **80** by the rule fixed in advance (longest); all four within noise; it is
  preventive hunger regulation, not an emergency line (GPT). The reflex takes under 1% of steps.
- The brain learns from the steps as taken. Each arm's kept copy is also tested: with the hunger reflex off (HR, HC:
  **S-off**); in the old body, rest at full price (CR, HC: **S-old**, GPT); and **bare**, both reflexes off in the old
  body (all arms: **S-bare**, GPT), read against W3m's SLS-off.

## Measures
Lifespan; survival to 3,000 and 1,000; fresh-land survival; the share of steps hungry and exhausted (per life, then per
seed); death labels; the share of test steps each reflex takes; sleep interrupted by hunger; arrivals at remembered
food that had gone (stale memory).

## Readings (`analyse_w3n.py`, frozen; paired by seed; bootstrap over 16 seeds, numpy seed 20261210)
1. **Two primary readings (Bonferroni, 97.5%, lower bound above 0):** **HRS − SLS** ("the hunger reflex helps") and
   **CRS − SLS** ("cheaper rest helps", read as a change of the body's economy, not a better brain), on lifespan.
2. **Secondary (95%):** HR − SL, CR − SL (the ends); HCS − HRS (does cheaper rest add on top?); HCS − CRS;
   HRS-off − SLS, HCS-off − SLS; CRS-old − SLS (did CR's brain adapt, or is it only the cheaper rest?);
   HRS-bare, CRS-bare, HCS-bare − SLS-off (what the brain does on its own); the hungry share, HRS − SLS.
3. **Toward the bar:** each arm's fresh-land survival against 0.80, with its interval (no claim from the best arm
   alone, GPT).

## Validity (hard stops)
Checks All: PASS before data (`checks_w3n.py`, 10: settings; arms; parts off = W3m's SL bit for bit; cheaper rest's
cost; the hunger reflex on a hand-made body; it does nothing without remembered food and wins over sleep; HR trains
differently, split = unsplit, repeatable; CR trains differently; a staged run saves its copies and runs every test,
with the body restored after).

## The assistant's prior (GPT's beside it)
- HRS − SLS above 0: about 80% (GPT 85%). CRS − SLS above 0: about 25% (GPT 60%): a rest costs ~5 energy less, small
  against the hunger deaths.
- HCS − HRS above 0: about 20%. HRS-bare − SLS-off above 0: about 30%.
- Any arm's fresh-land survival at or above 0.80 (observed): about 40% (GPT 55%).
