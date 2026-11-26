# BV1: Body v1, step 1 — today's brain through the standard body (DRAFT, not frozen; for the council and the creator)

Drafted 26 Nov 2026 (EST) on the second computer, after the creator asked for the next work "according to our plan"
(order: W3r -> Body v1 -> G0 -> G1 -> Play). **Not frozen; nothing built.** The handoff: freeze only after W3r's
result, with the creator's yes. Sources: `body_v1_draft.md` (revised after the round-table),
`roundtable_body_v1_2026-11-25.md`, Grok's first reply (`D:\acl\docs\grok_review_briefing_2026-11-25.md`).

## Question
Does today's best brain lose anything when it lives through **Body v1** (the standard senses, verbs and a per-world
adapter) instead of being wired straight into Mind Lab's world? Step 1 changes only the connection, never the brain
(the round-table: "test frozen-brain compatibility separately from adaptation").

## Facts that shape it (from `workbench/W3/world3.py`)
- The Mind Lab body has 5 actions: 4 moves and stay. Eating is automatic (on a full food cell when energy is below
  its maximum); resting is automatic (at the shelter, tiredness falls). No inventory, no thirst, no pain in W3r's world.
- So through Body v1: move(4) -> the 4 moves; rest -> stay; **use** and **operate(k)** exist but this world offers no
  operation (K = 0): "use" is always legal and changes nothing (feedback says so).
- Body v1's senses here: eyes = the raw look of each remembered cell (W3r's colour code, 8 codes) or "never seen";
  touch = the look in front and underfoot; hands = empty; feelings = hunger and tiredness (0-1, from energy and
  fatigue), pain = 0; feedback = signed changes after each action (place, hunger, tiredness); self = facing, steps
  since last meal and last rest.

## The brain (depends on W3r's result; fixed before any BV1 data)
- **If W3r passes** (RMS − RVS lower bound above 0): W3r's RM kept copies (RMS, 16 seeds), each with its meaning table.
  Through Body v1 the table learns from Body v1's **feedback** (blocked = place unchanged after a move; fed = hunger
  fell; rested = tiredness fell), never from the world's internal flags.
- **If W3r fails:** BV1 waits; Body v1's eyes give only raw looks, and without a working within-life learner the brain
  cannot read them (W3o: changing colours break it). The next step is then the consequence model itself (a council
  question below).

## Arms (W3r's changing-colour test lands; the 16 training seeds; each brain frozen)
| arm | the brain's connection | answers |
|---|---|---|
| **NATIVE** | W3r's own wiring (the rerun of RMS on the same test lands) | the reference |
| **BODY** | Body v1 + the Mind Lab adapter | the primary: no loss? |
| **BODY-SHUF** | as BODY, colour codes and verb numbers shuffled per land (seeded) | the adapter hides no meaning in its numbering |
| **BODY-PAD** | as BODY, plus 8 dummy operations (legal, do nothing, random order per land) | extra verbs change nothing |

## Primary reading (non-inferiority, set before data; the round-table's margins)
BODY vs NATIVE, paired by seed (16 seeds) on the same fresh test lands:
1. the lower 95% bound of the difference in mean lifespan above **−5% of NATIVE's mean**, AND
2. the lower 95% bound of the difference in full-life survival above **−3 points**, AND
3. the worst quarter of seeds (4 of 16) no more than **10%** worse in lifespan.
Bootstrap over seeds, 10,000 resamples, seed 1 (W3r's convention). Pass = all three.

## Measures beside it
Dead-action rate (use / operate chosen; the frozen brain cannot choose them, so 0 is expected and is itself a check),
stay rate, early vs late life, detours (the Bob Profile's R2), causes of death, the table's accuracy by age; the same
for BODY-SHUF and BODY-PAD.

## Checks before data (All: PASS required)
1. **Zero check:** BODY's table receives exactly the same (colour, consequence, fair-trial) events as NATIVE's table on a
   scripted life, and BODY reproduces NATIVE **bit for bit** on 2 seeds. (If the adapter is exact, BODY = NATIVE; the
   study's real content is then the audits; see council question 1.)
2. **Adapter audit as its own gate, before any brain is attached** (Grok, 25 Nov; the round-table's point 6): across
   randomised renamings, no adapter output (legality, availability, ordering, auto-targeting, hidden state) is
   correlated with reward-relevant kinds; a scripted random body shows the same feedback statistics under every
   renaming.
3. The brain never sees the true kinds; the table resets at every birth and every test land.
4. Same seed, same result.

## Expected (before data)
If check 1 passes, BODY = NATIVE exactly and the primary passes trivially; BODY-SHUF and BODY-PAD should also match
(within the bootstrap). The assistant: pass about 90% (the risk is in the build, not the brain).

## Compute
Test lives only (no training): 4 arms x 16 seeds on Oracle, a few hours. Machine recorded.

## Questions for the council (round-table)
1. If the adapter reproduces the native run bit for bit, is a non-inferiority run still worth doing, or is step 1 the
   zero check plus the audits, with the data budget moved to step 2 (the crafting world)?
2. Is "hands empty, use always does nothing, K = 0" a fair first test of the body, or does it test too little?
3. If W3r fails, what should step 1 be?
4. Are the margins (−5% lifespan, −3 points survival, worst quarter 10%) right for a frozen-brain, connection-only test?
