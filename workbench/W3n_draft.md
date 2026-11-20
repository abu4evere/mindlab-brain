# W3n: the body's own mind, part 2: cheaper rest and a hunger reflex (DRAFT, 20 November 2026)

**Why:** W3m's sleep reflex (SL; preliminary, 11 of 16 seeds) cut exhaustion deaths from 69% to 18% and raised
fresh-land survival from 0.43 to 0.62. Hunger now kills: 76% of deaths with remembered food within 30 steps, about 150
steps after the last meal; 29% of deaths before step 300. A council (GPT, Gemini; options asked neutrally, 19 Nov) picked
a narrow hunger reflex; cheaper rest was judged realistic but small; drain growing with hunger and hunger raising
tiredness were rejected.

## Arms (W3m's SL: W3k's run R, 4.0M steps, 2.4M fade, the sleep reflex; kept copies; 16 seeds)
| arm | the new part |
|---|---|
| **CR, cheaper rest** | a step resting at the shelter costs 0.5 energy (was 1); the body's energy economy changes |
| **HR, hunger reflex** | at energy 80 or less, with food in the map memory, the body walks the shortest known way to the nearest remembered food and hands control back once it has eaten (or when no remembered food is left); it wins over the sleep reflex while on; it reads only the memory, so a moved patch is walked to in vain |
| **HC** | both |
| SL (W3m, cited) | with both new parts off, W3n trains W3m's SL bit for bit (checked) |

- **Calibration** (before data, calibration lands only): W3m's SL brains with the hunger reflex added at test, lines
  50/60/70/80: full lives 0.59 (no hunger reflex) → 0.78–0.80 (all lines within noise; 80 longest, chosen by the rule
  fixed in advance). The reflex takes under 1% of steps.
- The brain learns from steps as taken (as W3m). Each arm's kept copy is also tested with the hunger reflex off.

## Measures
Lifespan; survival; fresh-land survival; share of steps hungry and exhausted; death labels; the share of steps each
reflex takes; arrivals at remembered food that had gone (stale memory).

## Readings (paired by seed; bootstrap over 16 seeds)
1. **Primary (Bonferroni, 97.5%):** HRS − SLS and CRS − SLS on lifespan.
2. **Secondary (95%):** HR − SL, CR − SL (ends); HCS − HRS (does cheaper rest add on top?); HCS − CRS; HRS-off − SLS
   and HCS-off − SLS (did the brain learn to eat on time?); hungry share HRS − SLS.
3. **Toward the bar:** the best arm's fresh-land survival against 0.80.

## Questions for the council
1. CR changes the world's energy rules, so CRS is tested in a body where rest is cheaper. Is CRS − SLS a fair
   comparison, or should CR also be tested in the old body?
2. The calibrated hunger line (80) is high, not an "emergency" line; the lines 50–80 were within noise. Keep 80 (the
   rule set in advance) or use 50 (a true emergency)?
3. Anything that makes the hunger reflex an unfair "oracle" (it uses only the brain's own map memory)?
4. Your probability for each primary reading (lower bound above 0), and for any arm reaching 0.80 on fresh lands.
