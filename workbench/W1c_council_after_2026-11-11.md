# W1c council: answers (11 November 2026)

The full answers are summarised in `W1c/questions.md` ("The council, in short").
- **GPT** (chat 6af53925): run W1c before a learned planner. It added a 100k-episode check, a learning audit, held-out
  topologies, an empty-room check and matched demonstrations.
- **Gemini** (chat 112218f0): the same view. It added a deeper convolution (receptive field), DAgger imitation against
  covariate shift, explicit boundary encoding and a geometric holdout. Its lower learning rate was not taken (the
  reason is in the plan).
