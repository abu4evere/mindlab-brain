# CX2-C blind recompute

## Who and blindness

Independent blind recompute by a Claude Code subagent (Claude Opus 5.5). Opened only the four raw JSONL files listed under Inputs (first by a `head`/`wc`/`ls` peek to learn the field layout, then by this script). Did NOT open, read, grep or list the contents of analyse_cx2.py, analyse_cx1.py, any analysis.json / analysis.md, any findings*.md, any recompute_*.md (including CX2/recompute_cx2_blind.md), lane*.log, run_*.out / run_*.err, questions*.md, or anything in C:\acl, and did not search the disk for other analyses. Definitions were taken solely from the task brief (frozen plan text).

## Inputs

- `C:\mindlab\exam_crafter\CX2\output_confirm\learn.jsonl` (16109 lines read)
- `C:\mindlab\exam_crafter\CX2\output_confirm\named.jsonl` (15809 lines read)
- `C:\mindlab\exam_crafter\CX2\output_confirm\blind.jsonl` (17629 lines read)
- `C:\mindlab\exam_crafter\CX2\output_confirm\random5p.jsonl` (16465 lines read)

Script: `C:\mindlab\exam_crafter\CX2\recompute_cx2c_blind.py`, run with `python -I`.

## When

Thu Nov 26 01:27:35 EST 2026 (from `TZ='EST5EDT,M3.2.0,M11.1.0' date` in Git Bash).

## Machine

- Platform: Windows-10-10.0.19045-SP0
- Python: 3.12.10 (C:\mindlab\exam_crafter\.venv\Scripts\python.exe)
- numpy: 2.5.5

## Score definition

For each arm, s_i = percent (0-100) of the arm's lives in which achievement i has count > 0 (absent key = 0), over all 22 Crafter achievements. S = exp(mean_i ln(1 + s_i)) - 1, reported in score points (percent units). Intervals: 2,000 bootstrap resamples of lives with replacement, independently within each arm, full S recomputed in every resample; 95% percentile interval = numpy.percentile(..., [2.5, 97.5]) with numpy's default linear interpolation. Differences use the same resamples (S_x,b - S_y,b).

## RNG order

One generator `numpy.random.default_rng(0)`. For b = 1..2000, in this fixed order: learn, named, blind, random5p, each `rng.integers(0, n_arm, n_arm)` (n_arm = number of well-formed lives in that arm). No other draws are made from the generator.

## Per-arm results

| Arm | Lives | Total steps | S | 95% interval |
|---|---:|---:|---:|---|
| learn | 16109 | 3000056 | 1.4982 | [1.4884, 1.5075] |
| named | 15809 | 3000151 | 0.5978 | [0.5886, 0.6063] |
| blind | 17629 | 3000086 | 1.0523 | [1.0423, 1.0626] |
| random5p | 16465 | 3000052 | 1.4730 | [1.4631, 1.4828] |

## Nonzero achievement rates (s_i, percent of lives)

Only achievements with s_i > 0 in at least one arm are listed; a cell of 0 means the achievement was never unlocked in that arm. Number of lives in parentheses.

| Achievement | learn | named | blind | random5p |
|---|---:|---:|---:|---:|
| collect_drink | 91.7251 (14776) | 93.2064 (14735) | 55.7888 (9835) | 37.8257 (6228) |
| collect_wood | 87.6032 (14112) | 0.4112 (65) | 46.3781 (8176) | 73.5074 (12103) |
| defeat_skeleton | 5.6676 (913) | 0.0443 (7) | 1.8209 (321) | 0.6802 (112) |
| defeat_zombie | 18.9087 (3046) | 0.1645 (26) | 5.4172 (955) | 45.4479 (7483) |
| eat_cow | 15.4696 (2492) | 22.9173 (3623) | 6.1943 (1092) | 19.1376 (3151) |
| wake_up | 30.1633 (4859) | 6.7620 (1069) | 20.1203 (3547) | 97.4188 (16040) |

Never unlocked in any arm (16): collect_coal, collect_diamond, collect_iron, collect_sapling, collect_stone, eat_plant, make_iron_pickaxe, make_iron_sword, make_stone_pickaxe, make_stone_sword, make_wood_pickaxe, make_wood_sword, place_furnace, place_plant, place_stone, place_table.

## Comparisons

| Comparison | Role | Point | 95% interval | Interval vs 0 |
|---|---|---:|---|---|
| LEARN - RANDOM5P | PRIMARY | 0.0253 | [0.0114, 0.0381] | above 0 |
| LEARN - BLIND | secondary | 0.4460 | [0.4316, 0.4592] | above 0 |
| LEARN - NAMED | secondary | 0.9005 | [0.8872, 0.9131] | above 0 |
| NAMED - RANDOM5P | gate for 'close' | -0.8752 | [-0.8892, -0.8621] | below 0 |

## Confirmatory reading

- PRIMARY, LEARN - RANDOM-5P: 0.0253, 95% interval [0.0114, 0.0381], above 0. Reading: **Confirmed**.
- Secondary, LEARN - BLIND: 0.4460, [0.4316, 0.4592], above 0.
- Secondary, LEARN - NAMED: 0.9005, [0.8872, 0.9131], above 0. NAMED - RANDOM-5P interval [-0.8892, -0.8621] is not entirely above 0 (below 0), so the 'close' reading does not apply.

## Checks

| Arm | Malformed lines | Blank lines | Seed range | Duplicate seeds | Missing seeds | Out-of-range seeds | Seeds in file order 100001.. | Names outside the 22 | Zero-valued achievement keys | Steps min / median / max |
|---|---:|---:|---|---:|---:|---:|---|---|---:|---|
| learn | 0 | 0 | 100001-116109 | 0 | 0 | 0 | yes | none | 0 | 6 / 184 / 600 |
| named | 0 | 0 | 100001-115809 | 0 | 0 | 0 | yes | none | 0 | 6 / 184 / 824 |
| blind | 0 | 0 | 100001-117629 | 0 | 0 | 0 | yes | none | 0 | 6 / 166 / 537 |
| random5p | 0 | 0 | 100001-116465 | 0 | 0 | 0 | yes | none | 0 | 9 / 178 / 744 |

- learn: total steps 3000056 (over 3,000,000 by 56; last life 233 steps, so total minus last life = 2999823).
- named: total steps 3000151 (over 3,000,000 by 151; last life 249 steps, so total minus last life = 2999902).
- blind: total steps 3000086 (over 3,000,000 by 86; last life 276 steps, so total minus last life = 2999810).
- random5p: total steps 3000052 (over 3,000,000 by 52; last life 187 steps, so total minus last life = 2999865).

Noted without interpretation:

- learn: 6 of 22 achievements have s_i > 0; longest life 600 steps; lives per arm differ because each arm stops just past 3,000,000 total steps.
- named: 6 of 22 achievements have s_i > 0; longest life 824 steps; lives per arm differ because each arm stops just past 3,000,000 total steps.
- blind: 6 of 22 achievements have s_i > 0; longest life 537 steps; lives per arm differ because each arm stops just past 3,000,000 total steps.
- random5p: 6 of 22 achievements have s_i > 0; longest life 744 steps; lives per arm differ because each arm stops just past 3,000,000 total steps.
- Smallest nonzero s_i across arms: defeat_skeleton in named (0.0443%).
- All four arms use the same seed sequence starting at 100001, so lives with the same seed exist across arms; per the plan they are treated as unpaired.

Field layout per life (key sets seen):

- learn, 16109 lives: achievements, actions, blocked_moves, bout_hurt, bouts, cells, death, first_drink, first_food, pokes, reward, seconds, seed, steps, trials_blocked, trials_fed
- named, 15809 lives: achievements, actions, blocked_moves, bout_hurt, bouts, cells, death, first_drink, first_food, pokes, reward, seconds, seed, steps, trials_blocked, trials_fed
- blind, 17629 lives: achievements, actions, blocked_moves, bout_hurt, bouts, cells, death, first_drink, first_food, pokes, reward, seconds, seed, steps, trials_blocked, trials_fed
- random5p, 16465 lives: achievements, actions, blocked_moves, bout_hurt, bouts, cells, death, first_drink, first_food, pokes, reward, seconds, seed, steps, trials_blocked, trials_fed

