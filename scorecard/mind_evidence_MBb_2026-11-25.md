# Mind evidence, a first baseline: MBb against Butlin et al.'s 14 indicator properties (25 Nov 2026)

**What this is:** the assistant's honest reading of Mind Lab's best brain (MBb: MoveVIN, 236 numbers; W3p) against the
14 indicator properties of Butlin, Long, Elmoznino, Bengio and 15 others, 2023 (arXiv 2308.08708; **read: the
indicator table, Table 1 in section 1, and sections 2.4.5-2.4.6**; the report text extracted locally). Exploratory, not
a frozen study, not reviewed yet by the council. The report itself concludes no current AI system is conscious; a
property present is evidence on that theory's terms, never proof. The creator asked for this line of work on 25 Nov
("yes write that research note and keep working in that side").

| Indicator (Butlin et al.) | MBb | Why (checked against `brain_mv.py`, W3n/W3p) |
|---|---|---|
| RPT-1 input modules using algorithmic recurrence | **partial** | the planner iterates 30 rounds of value spreading over the remembered map (recurrence over the input), but it is planning, not perception |
| RPT-2 organised, integrated perceptual representations | absent | the map memory is a hand-made writer; nothing perceptual is learned (W3r and CX2 begin to learn meanings) |
| GWT-1 multiple specialised modules in parallel | absent | one small network; the body's two reflexes are separate but hand-written |
| GWT-2 limited-capacity workspace with selective attention | absent | |
| GWT-3 global broadcast | absent | |
| GWT-4 state-dependent attention querying modules in succession | absent | the drives weight the lenses by state (hunger, tiredness, curiosity), but nothing queries modules |
| HOT-1 generative, top-down or noisy perception | absent | |
| HOT-2 metacognitive monitoring (reliable vs noise) | absent | no model of its own reliability (a target: "does it know when it doesn't know?") |
| HOT-3 belief formation updated by metacognition | absent | |
| HOT-4 sparse, smooth "quality space" coding | absent | |
| AST-1 a predictive model of its own attention | absent | |
| PP-1 input modules using predictive coding | absent | W3r's and CX2's modules predict consequences of actions, not the senses |
| AE-1 agency: learning from feedback, pursuing goals, flexible between competing goals | **present (weak)** | it learns from its own feelings (actor-critic) and weighs competing needs (the Bob Profile's A2 test: the first move follows the larger need) |
| AE-2 embodiment: modelling output-input contingencies and using it in control | **partial** | its learned "can I step here?" filter predicts whether a move will work and plans with it; other actions' effects are not modelled yet |

**Baseline: 1 present (weak), 2 partial, 11 absent.** As expected for a 236-number planner. What would move it (each a
possible future study, none started): a learned world model of consequences for all actions (AE-2; the W3r/CX2 line),
metacognition (HOT-2: an uncertainty the brain reads and acts on), learned perception from raw input (RPT-2; a general
body's raw eyes), and recurrence in perception (RPT-1). The creator's "no language models inside" rule keeps every one of
these honest: anything Bob shows, he did not copy from human text.
