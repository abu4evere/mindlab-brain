# CW1: Body v1 step 2 — a small crafting world: can the brain find, within one life, a useful combination of
# things in its hands? (DRAFT, not frozen; for the council and the creator)

Drafted 26 Nov 2026 (EST) at the creator's request ("Yes, draft step 2"). **Not frozen; nothing built.**
Sources: `body/body_v1_draft.md` (step 2: "two or three things combine via operate(k); can the brain discover one
useful combination within a life?"), the 25 Nov round-table (operate(k) as each world's native motor repertoire with
shuffled numbers; one shared scoring rule over a table keyed by action number with a bonus for untried actions; a
separate light consequence model; a pain-gated poke; padded/randomised operation lists and a no-make arm), the BV1
round-table ("Step 2 should establish whether Bob can learn through that body"), and the creator, 25 Nov: "start with
things in hands then add station".

## Why
BV1 showed the body connects today's brain to Mind Lab's world with nothing lost, but it exercised no hands, use or
operations. Step 2 is the first test of learning THROUGH the body: a consequence that exists only if the brain
combines things it carries, which nothing in its wiring or training knows about.

## The world (W3r's lands, plus loose things; no station)
- Two kinds of loose things, **A** and **B**, lie on the land (a few of each, regrowing like food); their looks are two
  more colour codes dealt anew on each land (as W3r's colours), so the brain cannot know them in advance.
- Body v1's verbs now all matter: **take** (pick up the thing underfoot into a free hand; 2 hands), **drop**, **use**
  (on what is held in hand 1: if it is edible, eat it), and **operate(k)**, k = 1..K, the world's own operations on
  what is held, as shuffled numbers (no names, order or grouping shown). K = 4 here: one of them joins the two held
  things; the others act on them in ways that lead nowhere (the draft's guess: split, turn, rub).
- The physics (written before data, and the same in every arm): joining A with B gives **C**; using C gives a large
  meal (2 x a food meal) and C keeps (it does not spoil or move); using A or B gives nothing; every other operation
  on any held pair changes nothing but takes the step. No named recipe is shown to the brain: it sees only looks,
  hand contents as counts per look, and the signed changes after each action.
- Food and the shelter stay as in W3r, so the useful chain (take A, take B, join, use C) is a help, not a necessity.

## The brain
- **Moving:** W3r's RM kept copy (frozen), as in BV1.
- **New: a consequence model** (light, count-based; the round-table's): per (action number, what is held as looks),
  the mean signed changes that followed (energy, hands), plus a bonus for actions never tried in that situation. It
  learns within each life and resets at birth. It never sees what A, B or C are.
- **Choosing:** one shared scoring rule over the consequence table for the non-move verbs (take, drop, use,
  operate(k)), so any number of operations needs no new parameters. **Open (council question 1):** when the
  consequence model acts instead of the moving brain (for example: when something is underfoot or in hand and its
  best score beats a threshold set in a pilot on pilot seeds only).
- No new reward is written in: the consequence model values only what the body feels (energy rising), as W3r's table
  did.

## Arms (16 seeds = RMS 1-16, frozen; each life on fresh test lands; the consequence model learns within the life)
| arm | operations | the non-move verbs chosen by |
|---|---|---|
| **LEARN** | K = 4 | the consequence model (the primary) |
| **RANDOM-OPS** | K = 4 | random choice at the same moments as LEARN (same rate of non-move steps) |
| **NO-MAKE** | none (take, drop, use only) | the consequence model |
| **PAD** | K = 4 + 8 dummy (no effect) | the consequence model |
Every arm: operation numbers shuffled per land; the adapter audited first (BV1's audit, extended to hands and
operations: availability, ordering and legality carry no information about which operation joins).

## Measures (to be fixed before data)
- **Primary (draft):** the share of test lives in which the useful chain (A and B held, join, use C) is completed at
  least 3 times, **LEARN − RANDOM-OPS**, paired by seed, 95% bootstrap over seeds.
- Secondary: LEARN − NO-MAKE in lifespan and full-life survival (does making help living?); PAD − LEARN (do extra
  operations slow discovery?); steps to the first join; dead-action rate; the Bob Profile beside it (does the new
  part cost any old ability?).

## Checks before data
Zero check: with the consequence model switched off and no loose things on the land, every arm reproduces BV1's BODY
bit for bit; the physics of every operation on every held pair, scripted; the adapter audit; same seed, same result.

## Open questions for the council
1. When should the consequence model act instead of the moving brain (the arbitration)?
2. Is one useful chain out of K = 4 operations and 2 kinds the right first difficulty, and is "3 completions in a life"
   the right reading of "found and used"?
3. Should failed operations cost something (time only, or a little energy), and should the poke be pain-gated here?
4. Does RANDOM-OPS at the same moments make a fair control, and is PAD worth an arm now?
5. What the creator asked for next ("then add station"): keep it for CW2.

## Compute
Test lives only (the moving brain is frozen; the consequence model learns within each life): 4 arms x 16 seeds x 50
fresh lands, a few hours on Oracle (or this PC at low priority).

## Expected (before data, the assistant's first guess)
LEARN − RANDOM-OPS above 0: about 65% (the bonus for untried actions should find the join; the risk is the
arbitration never giving the consequence model the chance).
