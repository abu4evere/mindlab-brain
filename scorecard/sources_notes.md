# Scorecard sources (notes)

## Butlin, Long, Elmoznino, Bengio, Birch, … VanRullen (2023), "Consciousness in Artificial Intelligence: Insights from the Science of Consciousness", arXiv:2308.08708
- **Status:** the full text (88 pages) is saved locally in `sources/` (not committed). **It has not yet been read in full**
  (the rule: read sources in full before relying on them). So far only its abstract and Table 1 (page 5) have been read.
- **Their conclusion (abstract):** "no current AI systems are conscious, but also suggests that there are no obvious
  technical barriers to building AI systems which satisfy these indicators."
- **Table 1 (indicator properties),** the exact labels:
  - **Recurrent processing theory:**
    - RPT-1, input modules using algorithmic recurrence;
    - RPT-2, input modules generating organised, integrated perceptual representations.
  - **Global workspace theory:**
    - GWT-1, multiple specialised systems capable of operating in parallel (modules);
    - GWT-2, a limited-capacity workspace, entailing a bottleneck in information flow and a selective attention
      mechanism;
    - GWT-3, global broadcast (the workspace's information is available to all modules);
    - GWT-4, state-dependent attention, giving the capacity to use the workspace to query modules in succession to
      perform complex tasks.
  - **Computational higher-order theories:**
    - HOT-1, generative, top-down or noisy perception modules;
    - HOT-2, metacognitive monitoring that distinguishes reliable perceptual representations from noise;
    - HOT-3, agency guided by a general belief-formation and action-selection system, with a strong disposition to
      update beliefs by the outputs of metacognitive monitoring;
    - HOT-4, sparse and smooth coding generating a "quality space".
  - **Attention schema theory:** AST-1, a predictive model representing, and enabling control over, the current state of
    attention.
  - **Predictive processing:** PP-1, input modules using predictive coding.
  - **Agency and embodiment:**
    - AE-1, agency: learning from feedback and selecting outputs so as to pursue goals, especially with flexible
      responsiveness to competing goals;
    - AE-2, embodiment: modelling output–input contingencies, including some systematic effects, and using this model
      in perception or control.
- **First reading for us** (to be checked against the full text):
  - C1's recurrent child has RPT-1 at most in a weak sense; its recurrence is in the decision core, not an input
    module.
  - NB2's brain has AE-1's first part (learning from feedback toward goals).
  - **Imagine** would add AE-2 (a model of how its acts change what it senses) and PP-1-like prediction.
  - **Mirror** (the second brain part) targets HOT-2 and AST-1.
- **Next:** read sections 2 and 3 in full; write each indicator as a check we can run on our code and behaviour;
  council; freeze.
