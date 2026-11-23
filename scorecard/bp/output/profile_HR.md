# Bob Profile, levels 2 and 5: HRS, seeds [1, 2, 3, 4, 5, 6, 7, 8]

- **Learning 2: PASS.** normalised lifespan mean 0.94, lower bound 0.92 (random 174, Script 2963 steps; pass >= 0.50)
- **Reasoning 2: fail.** success mean 0.27, lower bound 0.22 over 36 cases (Script 1.00, greedy 0.00, random 0.00; pass >= 0.80)
- **Reasoning 5 (detour half): fail.** success mean 0.12, lower bound 0.06 over 8 cases (Script 1.00, greedy 0.00, random 0.00; pass >= 0.80)
- **Memory 2: fail.** success mean 0.82 (lower bound 0.70); memory erased 0.48, drop lower bound 0.21 (Script 1.00, random 0.04; pass >= 0.80 and drop >= 0.20). Source: the designer's map memory (allowed at level 2)
- Memory 5: **fail by construction**: the brain has no learned memory of its own (its map memory is written by our code)
- **Generalization 2: PASS.** ratio mean 0.79, lower bound 0.76 (Script 0.97; pass >= 0.50)
- **Autonomy 2: PASS.** tracks mean 0.82, lower bound 0.71 over 7 lands (Script 1.00, random -0.07; pass >= 0.30). Source: the drives and their mix are the designer's; the weights are learned
- **Autonomy 5: fail.** bare fresh-land survival mean 0.38, lower bound 0.30 (Script 0.94; pass >= 0.50)
- Learning 5, Generalization 5, Reasoning 5 (value half): — (tests not built yet)

| Learning | Reasoning | Memory | Generalization | Autonomy | measured total |
|---|---|---|---|---|---|
| 2 | 0 | 0 | 2 | 2 | 6 |

Levels above 2 are not awarded until their tests are built and frozen; the goal is at least 10 in each.
