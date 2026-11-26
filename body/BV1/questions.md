# BV1: Body v1, step 1 — today's brain through the standard body (FROZEN, tag BV1-frozen)

**Sign-off:** the creator, 26 Nov 2026 (about 19:00 EST), in this Claude Code session: "Yes, sign off BV1".
History: `questions_draft.md` (first draft and the round-table's revision), `roundtable_bv1_2026-11-26.md` (GPT,
Gemini, DeepSeek, Grok; 2 rounds; each an opinion, not sign-off).

## What BV1 is
An **interface gate** (engineering), not a science result. It tests only that Body v1 (standard senses, verbs and a
per-world adapter) connects today's brain to Mind Lab's world **without changing anything the brain sees, learns or
does**. It tests no hands, use or operate(k) (Mind Lab's W3 world has none: K = 0, hands empty) and licenses no claim
about the body's generality; step 2 (a crafting world) does that.

## The brain
W3r's RM kept copies (RMS), each with its meaning table (W3r questions.md). W3r's official reading is not final at
freezing; a preliminary look (Oracle seeds 1-11, logged 26 Nov) shows RMS far above RVS. If the frozen W3r reading
fails, BV1's result still stands as an interface check, and the creator decides what follows.

## Body v1 in Mind Lab's world (from `workbench/W3/world3.py`)
- Verbs: move(4) -> the 4 moves; rest -> stay; use -> always legal, changes nothing; operate(k): none (K = 0).
- Senses: eyes = per remembered cell, the raw look (W3r's colour code) or "never seen"; touch = the look in front and
  underfoot; hands = empty; feelings = hunger and tiredness (0-1, from energy and fatigue), pain = 0; self = facing,
  steps since last meal and last rest.
- **Feedback = two signed parts per feeling** (the round-table and the code): the body's own per-step drift, and the
  change caused by the world's response to the action, measured after the drift; plus "place changed" (yes/no). In this
  world the step's cost comes before the meal check, so a meal always shows as a rise of at least 1, even at the cap.
- The meaning table learns only from Body v1's outputs: blocked = a move with place unchanged; fed = the world's
  response raised energy; rested = the world's response lowered fatigue; fair trials as W3r's rules (a step where a
  consequence could not happen teaches nothing about it).

## Arms (the brain frozen in every arm)
| arm | connection |
|---|---|
| NATIVE | W3r's own wiring |
| BODY | Body v1 + the Mind Lab adapter |
| BODY-SHUF | as BODY, with colour codes and verb numbers renamed per land (seeded), undone only for the comparison |

## The gate (pass = all of these; any mismatch = fail, then diagnose)
1. **Adapter audit first, before any brain** (`checks_bv1.py`): across randomised renamings, no adapter output
   (legality, availability, ordering, the feedback parts, hidden state) carries information about which looks are
   food, wall or shelter, including conditional on the action; a scripted random body shows the same statistics under
   every renaming.
2. **Exact parity:** on 8 seeds (RMS seeds 1-8), each on its own fresh test land (W3r's first fresh land for that
   seed), one full life per seed in each arm: BODY and BODY-SHUF reproduce NATIVE **bit for bit**, compared step by
   step on the brain's input layers, its action, the table's counts and the body state (position, energy, fatigue),
   not only lifespan. The 8 lives must between them include wall hits, meals below and at the energy cap, resting at the
   shelter and map edges; if they do not, more lives are added from seeds 9-16 until they do (fixed rule, before data).
3. Same seed, same result (each arm run twice on one seed).
No statistics; a mismatch is reported with the first differing step.

## Expected (before data)
Pass if the build is right (the assistant about 90%); the likely failure is a build bug caught by the gate.

## Compute
A few CPU-minutes on this PC (Idle priority). Machine recorded.
