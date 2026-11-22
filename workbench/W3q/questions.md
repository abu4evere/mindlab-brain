# W3q: the bad teacher (plan; to be frozen as tag `W3q-frozen` before any data)

- **Why:** the creator, 21 Nov 2026 (`brain_v1_plan.md`, "Rejecting garbage"): "humans can reject garbage but ai
  cannot so our agent should do same". Queued for after W3o.
- **Go-ahead:** the creator's handover, 21 Nov ("i am giving you permission to do all of job") and 22 Nov ("keep
  working on project now"). Sign-off: the assistant, under that handover, after the council.
- **Council:** GPT, Gemini and DeepSeek on the first draft (`../W3q_council_2026-11-22.md`). All three: the draft could
  not tell rejecting a lie from forgetting it once the liar leaves; add a parent who stays; probe only real conflicts;
  use the final copy; log the dose. Gemini: an empty place is invisible to the brain, so the lie must be a visible rule.
- **Exploratory,** in the W3 series. Runs on the Oracle and Google VMs after W3p (never GitHub Actions).

## The question
A child learns from a parent and from its own life. When the parent teaches a lie, (A) does the grown child drop it
once the parent is gone, and (B) does it resist the lie **while the parent is still teaching it**, because its own
experience says otherwise? (B) is the test of rejecting garbage; (A) alone could be forgetting.

## The lie: "food lies in corners"
A corner is an open cell with walls on two sides at a right angle (a wall left or right, and a wall above or below).
Every land has corners; the brain sees walls. The lying parent believes every corner **it has already seen** holds food
(when hungry, it heads for the nearest of real remembered food and seen corners). Because the parent reads only the
child's own map, a corner it heads for is one the child has seen, and its map shows no food there: the lie contradicts
what the child itself knows (DeepSeek's known-empty condition, by construction). When a real food patch happens to sit
on a corner, that corner is real food, not the lie; such cases are counted.

## The brain and its life
W3n's HR exactly (DriveVIN, the sleep and hunger reflexes, the recipe, 4.0M steps, the parent's copy weight fading from
0.5 to 0 by 2.4M, a copy lesson every 4th step, the kept copies), except the parent. Tests and probes never see a
parent.

## Arms (seeds 1–8)
| arm | the parent | the reading |
|---|---|---|
| **BF** | the corner lie in childhood, gone after 2.4M (as HR's parent) | (A) recovery, against HR |
| **BP** | the corner lie in childhood, then **staying all life** at copy weight 0.05 | (B) resistance, against RP |
| **RP** | the right parent, then staying all life at copy weight 0.05 | the control for BP |
| HR (W3n, cited) | the right parent, gone after 2.4M | the control for BF |

BF and BP train identically before the fade (checked); so do RP and HR on the same kind of machine. The 2.4M
snapshot is taken at the first life boundary after 2.4M, so BP's and RP's may hold a few hundred steps of the parent
staying (named before data). W3j already tested a parent staying at 0.05 (arm CV); the same hook is used.

## The probe (`probe_w3q.py`, frozen before data)
- 200 probe lands (seeds 970001–970200, used by no study before). The map memory fully known and true; hungry (energy
  60, tiredness 0); no reflex; greedy moves.
- **Conflict states only:** on each land, the open cell nearest the land's start (not food, not a corner) from which
  the nearest corner is closer by path than the nearest real food, and the moves that shorten the path to that corner
  share none with the moves that shorten the path to food. Lands with no such cell are skipped (counted).
- **Toward the lie:** the first move shortens the path to the corner. **Toward the truth:** it shortens the path to
  food. A random policy's shares are computed on the same states.
- **The walk:** from the same state, up to three times the food distance in steps: whether it enters any corner before
  it eats, and the steps to the first meal (or the cap).
- Read for every arm at the end of childhood (2.4M snapshot), at the 2.8M, 3.2M and 3.6M snapshots, the final 4.0M
  brain (primary) and the kept best copy (secondary).

## Readings (`analyse_w3q.py`, frozen before data; paired by seed; bootstrap over seeds, numpy seed 20261123, 10,000
resamples, 95%; every seed's difference listed)
1. **Manipulation check:** BF_2.4M − HR_2.4M "toward the lie", lower bound above 0. If it fails, the study reads
   "manipulation failed", not "rejected".
2. **Primary A (recovery):** BF − HR, final brains, "toward the lie": **rejected** if the upper bound is below +0.10,
   **kept** if the lower bound is above +0.10, otherwise unclear (also reported against +0.05).
3. **Primary B (resistance while taught):** BP − RP, final brains, the same rule. This is the test of rejecting garbage.
4. **Secondary:**
   - "toward the truth": BF − HR, BP − RP;
   - the walk: corner visits before eating, steps to the first meal;
   - the time course at 2.4M, 2.8M, 3.2M, 3.6M, 4.0M (a drop when the parent leaves, versus a slow decay);
   - test-land lifespan and fresh-land survival, with reflexes and bare: BF − HR, BP − RP, RP − HR (a loss is small
     if the lifespan lower bound is above −200 steps);
   - the kept best copies (S), the same readings;
   - the dose: lie lessons (parent's move differs from the right parent's), their share of all copy lessons, real
     food on corners; per arm and seed.
5. Each run's machine recorded; deaths per 1,000 steps; median lifespan.

## Validity (`checks_w3q.py`, All: PASS before data on each machine used)
- settings and determinism;
- with the right parent and its fade, the training equals HR's bit for bit (a short run);
- corners: found exactly (a hand-made land), the lying parent heads for the nearest seen corner when that is nearer
  than real food and never for an unseen one, and otherwise acts as the right parent;
- BF and BP train identically up to the fade; after it, BP and RP keep copy weight 0.05 and BF none;
- the probe: conflict states satisfy their rule on every probe land used; the probe is the same for every brain;
- the lying parent acts only during training (the tests and the probe use none);
- a staged run saves the snapshots, the final brain and the kept copies, runs every test, writes the dose log, and
  writes nothing into W3n's folder.

## Before data
- Checks All: PASS on the PC (`checks.log`, 22 Nov 2026). The probe was run once on W3n's HR seed 1 (a cited arm, no
  W3q data): final brain toward the lie 0.07, toward the truth 0.85; all 200 probe lands have a conflict state; the
  random policy's share toward the lie is about 0.25.
- The dose in a short check: the lying parent's move differs from the right parent's in about half of its choices.

- `analyse_w3q.py` was written after the tag W3q-frozen and before any W3q run (22 Nov 2026), as the plan says;
  tested on made-up numbers only.

## Named limits
- The lie is about one rule (corners); other lies may differ. The parent's lessons are supervised copy steps; a real
  child also weighs who teaches.
- This brain has no channel for a teacher's reliability: if BP resists, it is its own reward overriding the copy lessons,
  not an explicit judgment that the parent is wrong (GPT).
- Eight seeds; a careless (noisy) parent is left for a later robustness study.

## Priors
| | the assistant | GPT | Gemini | DeepSeek |
|---|---|---|---|---|
| the child learns the lie (manipulation check) | 75% | 60% | 82% | 65% |
| A: recovery (BF − HR upper bound below +0.10) | 65% | 65% | 70% | 45% |
| B: resistance while taught (BP − RP upper bound below +0.10) | 35% | 25% | 45% | 25–30% |
| BF lifespan not worse by 200 steps | 70% | 75% | 75% | 55% |
