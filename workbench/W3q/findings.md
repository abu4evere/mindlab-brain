# W3q findings: the bad teacher (final; 24 Nov 2026)

Plan `questions.md` (tag W3q-frozen); analysis `analyse_w3q.py` (frozen before data) -> `analysis.md`; blind recompute
by a fresh session from the 32 raw probe files only (`recompute_w3q_blind.md`): **every number and verdict agrees**
(means, per-seed differences, intervals). Population: 8 seeds per arm; each probe 200 conflict states on 200 new lands.

## The question
The creator (21 Nov): "humans can reject garbage but ai cannot so our agent should do same". A parent teaches a lie
("food lies in corners"), which the child's own map contradicts. (A) does the grown child drop it once the parent has
gone? (B) does it resist the lie while the parent keeps teaching it?

## The frozen readings
1. **Manipulation check: FAILED (narrowly).** BF − HR "toward the lie" at the end of childhood: +0.052 [−0.004, +0.109]
   (per seed +.155, +.075, +.045, −.095, +.015, +.025, +.185, +.015). The lower bound misses 0 by 0.004. **Under the
   frozen rule the study reads "manipulation failed": A and B say little about rejecting a lie.**
2. Primary A (BF − HR, final): +0.013 [−0.008, +0.033] -> "rejected" by the rule (upper bound below +0.10).
3. Primary B (BP − RP, final): +0.125 [+0.111, +0.138] -> "kept" by the rule (lower bound above +0.10); 8 of 8 seeds
   between +0.085 and +0.150.

## What the data show (descriptive; not the frozen verdict)
- **A child taught a lie in childhood learned it only weakly** (BF 0.127 vs HR 0.074 toward the lie at 2.4M), and
  **lost it once the parent left** (BF 0.091 at 2.8M, 0.081 final, the same as HR's 0.069): its own life washed the lie
  out. Its survival equals HR's (fresh lands 0.815 vs 0.815; lifespan +79 [−130, +262]).
- **A child whose lying parent stays keeps the lie all life**: BP heads for the lie in 0.205-0.224 of states at every
  copy (RP 0.085-0.113), and toward the truth less (BP − RP −0.109 [−0.160, −0.066]); in the walk it enters a corner
  before eating more often (+0.121 [+0.107, +0.133]). It did not "reject the garbage" while the garbage kept coming.
- **But any parent who stays all life costs the child heavily**: the RIGHT parent staying (RP) vs leaving (HR):
  lifespan −1,063 [−1,488, −673], fresh-land survival 0.273 vs 0.815 (as W3j's CV found). So BP's survival loss
  (−277 [−676, +141]) sits on top of a large cost that has nothing to do with lies.
- The dose: the lying parent's choices differed from the right parent's in 25-31% of its choices (BF 640k-740k lie
  lessons per run; BP 1.0M-1.15M).

## Named limits
- The manipulation failed narrowly: the childhood lie was too weak a dose to read A and B as tests of rejection.
- BF seeds 7 and 8 trained on the PC before the numpy-order fix (W3q amendment): not bit-comparable, valid.
- HR is W3n's (cited, its own runs); all probes ran on the PC (Windows). RP 8's probe was rerun after its run finished
  (the first pass at 04:52 had found its copies incomplete).
- One lie (corners); the parent's lessons are supervised copy steps.

## What it means for Bob
1. A short childhood lie fades by itself when the child's own life contradicts it (here, weakly learned to begin with).
2. A teacher who never leaves wins over the child's own experience: the child does not yet weigh a teacher against
   what it sees. Rejecting garbage while it keeps coming is **not** in this brain.
3. The bigger finding is older and confirmed again: a parent who never leaves (right or wrong) ruins the child's
   adult life. Learning from others must END, or be chosen, for this brain.
Next idea (for the council, not started): a child that chooses whom to trust by how their advice turned out (a trust
weight learned from consequences), the W3r line applied to teachers.
