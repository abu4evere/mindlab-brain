# WS: learning step-by-step skills fast. Which brain part lets a child learn a sequence from showings? (frozen plan)

**Frozen** as git tag `WS-frozen`, before any code or data.
- **Sign-off:** the creator, 13 November 2026: "ok go with your suggestion" (pause Cradle's copying rungs; build the
  part that learns sequences). Then, before sleeping: "keep working … keep it pushin". Under the sleep-mode autonomy:
  the council had seen the draft; estimate of success (a valid, informative study) about 60%.
- **Draft:** `../WS_draft.md`.

**Council** (opinions, not sign-off):
- **The chats:**
  - GPT: chatgpt.com/c/6af7e454-847c-83ea-87bc-352e414477ec;
  - Gemini: gemini.google.com/app/c02276bb41eff484;
  - DeepSeek: chat.deepseek.com/a/chat/s/b460145c-2985-4596-9b08-2e83d24cc12a.
- **Taken from all three:**
  - **an update-matched control:** replay gives extra updates, so Bu gets the same extra copy amount, immediately and
    with no replay;
  - **a buffer smaller than the task:** 4 episodes, so replay must select (Gemini);
  - **Brm in the readings;**
  - **retention** after day 30.
- **Taken from one model:**
  - GPT: a test that needs the memory. **Taken:** the "after a showing" test, where the box is shown just before the
    test, as in deferred imitation, so a memory can carry it;
  - DeepSeek: a pure-copy brain with no reward learning (Bp), and random demonstrations (Bx) to show the learning is
    specific;
  - Gemini: learned recurrence, not a fixed buffer (taken for Bm).
- **Not taken:**
  - **3 lids as the primary** (Gemini). C2-K2's difficulty check showed 3 lids at the floor;
  - **novel box combinations** (DeepSeek). C2 showed little transfer; later.
- **DeepSeek's caution, recorded:** with 30 days of showings and reward, this tests fairly slow learning, not one-shot
  imitation as in infants. The "after a showing" test is the nearest to the infants' task.

## The task (Cradle C2-K's boxes; C2-K2's easiest level)
- **The boxes:** 6 kinds, each with **2 lids** opened in order. Each lid opens by its own ordered pair of 4 acts (the
  2 pairs of a box differ). A wrong lid ends the try; reward 1/2 per lid opened.
- **Tries:** 3 per kind per day (18 a day), for 60 days.
- **One reliable demonstrator.** On days 1–30, before each try, the demonstrator shows the whole box (both lids
  right). In Bx, the shown pairs are random (fixed draws per seed), not the right ones.
- **The showing is not in view during the child's try** (deferred). The child's try input is only:
  - look 16;
  - the lid number 3;
  - its own first act 4;
  - step 1.

## The brains (48 children each, seeds 1–48, paired; C2's network size, 32 tanh units)
| brain | copy | reward learning (REINFORCE, C2's) | memory |
|---|---|---|---|
| **B0** | every showing copied before the try, rate 0.5 | yes | none |
| **Bc** | rate 1.0 | yes | none |
| **Bu** | rate 0.5 × (1 + 4/18) (the same total copy amount as Br) | yes | none |
| **Br** | rate 0.5, **plus nightly replay:** the last 4 showings are kept in an episodic store, and each night each one is rehearsed as one copy step at rate 0.5 | yes | episodic store |
| **Bm** | as B0, through a **learned recurrent state:** the showing is fed in as steps before the try, and the state carries it through the try | yes | **recurrent (learned)** |
| **Brm** | Bm plus Br's nightly replay | yes | both |
| **Bp** | as B0 | **no** (copy only) | none |
| **Bx** | as B0, **random showings** | yes | none |

**Bm's arithmetic:**
- h_t = tanh(Wx x_t + Wh h_(t−1) + b); the input adds the shown act 4 and a showing flag 1.
- **Each showing** is fed as 2 steps per lid (its 2 acts). The try then runs on the same state, which starts at zero
  before the showing.
- **The copy step** is cross-entropy toward the shown acts at the try steps, with the child's first act forced to the
  shown first act. It uses backpropagation through the whole sequence.
- **REINFORCE** uses the same backpropagation through the sequence.

## Tests (learning off; best acts)
1. **Skill:** no showing, as C2-K, at days 1, 2, 3, 5, 7, 10, 15, 30, 45, 60. **Full-box success** is the share of the
   6 kinds fully opened.
2. **After a showing** (day 30 and day 60): the right sequence is shown just before the test (Bm and Brm can carry it;
   for the others the showing has no input). Full-box success.

## Readings (paired bootstrap over seeds, 10,000 draws, `numpy.random.default_rng(20261113)`; n = 48 per brain)
1. **PRIMARY:** "Replaying showings helps, beyond the amount of copying": Br − Bu, skill at day 30, has a lower bound
   above 0.
2. "A learned memory helps the child copy a sequence": Bm − B0, after a showing at day 30, has a lower bound above 0.
3. "Both together beat either": Brm − max(Br, Bm), skill at day 30, has a lower bound above 0. The max is taken per
   seed.
4. "Replay beats the baseline": Br − B0, skill at day 30, has a lower bound above 0.

**Checks (reported):**
- Bx at or near T-like levels, so learning is specific to the right sequence;
- Bp against B0 (does reward learning add anything);
- Bc − B0;
- retention (day 60 − day 30), per brain;
- the target: which brains reach 0.5 by day 30;
- the partial score.

**Floor note:** if every brain's skill at day 30 is below 0.05, readings 1, 3 and 4 read "floor: not readable".

## Validity (code checks, All: PASS before data)
- showings are never in the try input (except Bm and Brm's showing steps before the try);
- Br replays exactly the last 4 showings each night;
- Bu's copy amount equals Br's;
- Bp never changes its weights from reward;
- Bx's showings are random;
- Bm's gradients (through time) equal finite differences;
- the same seed gives the same result twice.

## The assistant's prior
- Reading 1: about 45%.
- Reading 2: about 50%.
- Reading 3: about 30%.
- Reading 4: about 65%.
- Some brain at 0.5 by day 30: about 30%.
