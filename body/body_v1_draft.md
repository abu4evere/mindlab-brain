# Body v1: the Standard Body (DRAFT; not frozen, nothing built; for the creator and a second council round)

**Why.** The creator, 24-25 Nov 2026: the body is the connector between a brain and a world ("if we want to put the
brain to different world we gotta put that brain to different body which means connector"); "our old acl agent does
not have general body and i think that was our mistake"; and the worry that a body built from Crafter's score list is
a Crafter body. Council (GPT, Gemini, DeepSeek; `council_general_body_2026-11-24.md`): a standard INTERFACE, not a
universal physical body; add action feedback; drop look and signal for now; adapters judge legality, never choose; do
not spend months on the perfect body; show it in Mind Lab first.

## The body (written before looking at any world's rewards)
**Senses (every step):**
| sense | what it is | never |
|---|---|---|
| eyes | a local map around me; each cell a raw look (a kind number or a colour code), plus "never seen" | a label like food, wall, danger |
| touch | the look of the cell in front of me and under me | |
| hands | what I hold, as counts per kind number | item names |
| feelings | hunger, thirst, tiredness, pain, each 0-1, from the body's own state | which things relieve them |
| **feedback** | did my last action change anything (my place, my hands, the cell in front, my feelings)? one bit per kind of change | why |
| self | my facing; time since I last ate, drank, slept | |

**Verbs (one per step):** move (up, down, left, right); use (on the cell in front); operate(k) (the world's own
operations as numbered actions, k = 1..K, numbers shuffled per world; GPT's opaque ids); rest. Later, as general
additions (Body v2+): take, put, signal (ACL's language goal).

## The adapter rule (one per world)
- It may translate formats (the world's tile ids to kind numbers, its inventory to counts, its stats to feelings).
- It may say whether an action is legal (an illegal one does nothing and feedback says "no change").
- It may never label meaning, never choose among the world's operations for Bob, never hide failing ones.
- A check for every adapter: shuffling all kind numbers and operation numbers leaves the brain's lives unchanged
  in distribution (CX2's relabelling check, made general).

## What the brain must learn through it (the W3r / CX2 line)
Which looks block, feed, water, rest or hurt; what each operation does; when "use" and "operate(k)" are worth trying.

## The order (each step a frozen study, each with the Bob Profile beside it)
1. **Mind Lab through Body v1:** today's brain (with W3r's learned meanings) must still live as well as through the
   old sorted eyes (no loss beyond a margin set before data).
2. **A small crafting world in Mind Lab** (DeepSeek's advice): two or three things combine via operate(k); can the brain
   discover one useful combination within a life?
3. **Crafter through Body v1:** the same brain and body, Crafter's 17 actions mapped to move, use, rest and operate(k).
4. Later: Craftax, ACL (after the 7 December review), and the signal verb for ACL's language goal.

## Open questions for the second council round
1. Is "operate(k)" with shuffled numbers honest enough, or does it still smuggle in Crafter's recipe structure?
2. How should the brain read hands and feedback (new layers for MoveVIN, or a small separate module)? The brain will grow
   past 236 numbers (about 45 per new sense layer).
3. What margin counts as "no loss" in step 1?

## Revised after the first round-table (25 Nov 2026; `roundtable_body_v1_2026-11-25.md`; still a draft, not frozen)
- **operate(k)** stays, labelled as each world's native motor repertoire (shuffled numbers; no names, order, grouping
  or legality shown); controls: padded / randomised operation lists and a no-make arm; combine(slot_a, NONE | slot_b |
  FRONT_TILE) is a v2 ablation.
- **Actions are chosen by one shared scoring rule over a table** keyed by action number (tries and the signed changes
  that followed, plus a bonus for untried ones), so any number of operations fits with no new parameters.
- **Feedback** becomes signed changes (hands and each feeling, up or down), not one bit per kind of change.
- **The brain:** MoveVIN stays the spatial planner; a separate light consequence model (count-based first, with
  uncertainty) learns what actions do and feeds MoveVIN's reward and passability maps; hands and feelings do not go onto
  the map.
- **The poke is pain-gated:** poke untried kinds; stop poking kinds whose pokes brought pain; a reflex-only baseline.
- **Step 1 = the frozen brain through Body v1 only** (no consequence model yet). Pass: on 10+ paired seeds, the lower
  95% bound of the difference above −5% relative mean lifespan AND above −3 points full-life survival, and the worst
  quarter of seeds no more than 10% worse. Also: dead-action and idle rates, early vs late life, detours, causes of
  death; adapter audits beyond id shuffling (availability, ordering, auto-targeting, hidden state).
- **Step 2 (the creator, 25 Nov 2026: "start with things in hands then add station"):** the Mind Lab crafting world first
  combines only what Bob holds; a station nearby comes next.
