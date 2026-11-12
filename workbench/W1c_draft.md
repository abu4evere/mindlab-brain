# W1c: does spatial structure let a network learn to navigate, and then to detour? (DRAFT, not frozen)

**Why:**
- W1b was valid. No rule-based shortcut passed, and the planner did.
- But no learning brain learned even to walk to food it could see (`W1b/findings.md`): neither actor-critic, nor
  memory, nor imitation of the planner (0.43 move accuracy on new layouts after 30,000 tries).
- The flat network has no sense of space. ACL's people have the same kind of brain.
- W1c adds the two simplest kinds of spatial structure, and keeps everything else of W1b.

## Kept from W1b (unchanged)
The world, the 400 learning and 240 test layouts (`W1b/layouts.json`), the seven scripted brains as controls, the
measures, the readings and the validity rule. The scripted results are W1b's own (they are deterministic).

## The new brains
| brain | input | network | learning |
|---|---|---|---|
| **E** | **egocentric:** a 21 × 21 window centred on the agent, two channels (walls, food), so "food to my right" is the same input everywhere | 882 → 64 tanh → 5 + value | actor-critic |
| **E-imit** | as E | as E | imitating B |
| **C** | egocentric, as E | **convolutional:** 3 × 3 conv, 8 filters, ReLU; then 3 × 3 conv, stride 2, 8 filters, ReLU; then 800 → 64 tanh → 5 + value | actor-critic |
| **C-imit** | as C | as C | imitating B |

- **The same settings as W1b:** 16 seeds per brain, 30,000 episodes, learning rate 0.01, gradient-norm clip 1.0,
  γ 0.97, entropy 0.01.
- **W1b's F-imit is the reference** for the flat network.

## Questions (readings as W1b's)
1. **Navigation:** does E or C solve the control layouts (≥ 0.80), where W1b's networks could not?
2. **Looking ahead:** does any of them reach "looks ahead" (efficient detour ≥ 0.80, pocket ≥ 0.70, above G)?
3. **Which helps more,** the egocentric view (E against W1b's F) or the convolution (C against E)?

## Open questions for the council
1. Are these the right two first steps of spatial structure, or should a learned planner (value iteration in the
   network) come first?
2. Is 30,000 episodes still fair, or should the budget grow when the network is not the question?
3. What would make a pass by C-imit more than pattern-matching of seen shapes?

## The assistant's prior
- E-imit solves the controls: about 55%; C-imit: about 70%.
- Any brain "looks ahead": about 25% (most likely C-imit).
- Actor-critic brains (E, C) solve the controls: about 30%.
