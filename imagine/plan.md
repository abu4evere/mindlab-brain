# Imagine: a brain that models its world, plans in its head, and picks its own goals (DRAFT)

**Why:** NB2's neural people only reacted, and most worlds died out. An autonomous mind looks ahead: it predicts what
will happen, tries plans in its head before acting, and chooses goals by what it expects to learn.

## The brain part, in three pieces (built and tested in the workbench first)
1. **A world model:** from what it senses and does, it learns to predict what it will sense next, and how its feelings
   will change. This is self-supervised, so it learns from every moment, not only from rewards.
2. **Planning in imagination:** before acting, it runs a few steps ahead inside the model, and picks the act whose
   imagined future feels best.
3. **Its own goals:** it values what it expects to learn (curiosity: the model's own errors, and how they shrink). So
   it sets goals nobody gave it.

## Tests
- In the workbench: the detour, the room of things to learn about, and the food patch.
- Against the same brain without imagination.
- Then into Cradle (does planning help the child keep up?) and into ACL (does a people that imagines survive where NB2
  did not?).

## Background to read first (in full, as always)
- **World models and planning in imagination:** for example the Dreamer line of agents (Hafner et al.) and MuZero
  (Schrittwieser et al.).
- **Curiosity from prediction error, and learning progress:** for example Pathak et al. 2017, and Oudeyer and Kaplan.
