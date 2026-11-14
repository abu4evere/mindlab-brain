# WN: how many neurons? A size sweep of the memory child, and a growing brain (plan, frozen before any code or data)

**Frozen** as git tag `WN-frozen`, before any code or data.
- **The creator** (14 November 2026): "run the neuron size test in mind lab". On growth: "if we give Bob 1000 neurons
  can that develop itself and turn that into 10000 neurons".
- **An exploratory sweep, with no gated readings:** it asks where size stops helping. The creator asked for it to run
  directly, so **there is no council for this sweep**; any decision drawn from it goes through a council later.

## The task (WS's, unchanged)
- **The boxes:** 6 kinds; 2 lids opened in order (each lid its own ordered pair of 4 acts); a wrong lid ends the try;
  reward 1/2 per lid.
- **Tries:** 3 per kind per day, for 60 days.
- **The demonstrator:** one, reliable, who shows the whole box before each try on days 1–30; the showing is not in
  view during the try.
- **The rest:** WS's learning rule, copy rate 0.5, learning rate 0.05 and tests.

## The brains (24 children each, seeds 1–24; the same seeds and draws for every brain)
- **M-n:** WS's memory child (a learned recurrent ring) with n = 8, 16, 32, 64, 128 or 256 neurons.
- **F-n:** the same with no memory ring (WS's B0), with n = 8, 32 or 128.
- **G (growing):**
  - the memory child is born with 16 neurons and doubles at days 8, 16 and 24, to 128;
  - old connections are kept; each new neuron's connections start small (N(0, 0.01²));
  - **new neurons start silent:** their outgoing weights to the hands and to old neurons start at zero.

## Measures (descriptive, with 95% bootstrap intervals over the 24 seeds; numpy seed 20261114)
- Skill (full boxes, no showing) at days 7, 15, 30 and 60.
- Success after a showing at day 30.
- **G compared with M-128 (born big) and M-16 (stays small),** at days 30 and 60.
- Run time per child, by size.

**The fixed learning rates are the same at every size.** A large brain might need different ones, so a "no gain from
size" result here is about this setting, and it is stated as such.

## The assistant's prior
- Skill rises from 8 to about 32–64 neurons, then flattens or falls (more to fill, same experience): about 60%.
- Memory beats no memory at every size: about 80%.
- Growing reaches M-128 by day 60 but is behind at day 30: about 45%.
