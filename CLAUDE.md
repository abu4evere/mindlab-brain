# Mind Lab: the brain workbench, the imagining brain, and the scorecard (started 11 November 2026)

**Handoff (13 November 2026, account switch):** read `D:\acl\docs\HANDOFF_2026-11-13.md` first; it covers all three projects and where the brain stands.

**The creator's goal:**
- **First:** an autonomous cognitive mind ("to emerge or to be built").
- **Ultimately:** an independent conscious mind.

Their words are in ACL's local book notes, `drafts/book_rewrite/part2/notes_for_book_2026-11-11.md`.

**The five projects** (the creator, 11 November 2026: "i would go with 1 and 2 and 5 but we gotta continue these with
acl and cradle so overall 5 project works"):

| project | where | asks |
|---|---|---|
| ACL | `D:\acl` | can culture appear from nothing, with a neural brain in a deep-time world? |
| Cradle | `D:\cradle` | can a neural child keep up with an ordinary life among AI people? |
| **Workbench** | `workbench/` | which brain design gives which ability? One ability at a time, fast. |
| **Imagine** | `imagine/` | can a brain learn a model of its world, plan in its head, and choose its own goals? |
| **Scorecard** | `scorecard/` | a fixed, published-theory-based checklist of autonomy and of features linked to consciousness, scored the same way for every brain |

**How they connect:**
1. The workbench tests brain parts one ability at a time.
2. What passes goes into Cradle (a life) and ACL (deep time and culture).
3. The scorecard measures every brain in all four.
4. "Imagine" is the first brain part the workbench builds, because NB2 showed that a brain which only reacts is not
   enough.

**Rules** (as ACL and Cradle):
- A frozen plan before code or data; the council (GPT, Gemini, DeepSeek); the blind recompute; findings that never
  hide a failure.
- No language model inside any mind.
- No keys or money handled by the assistant.
- Public surfaces (a GitHub repo, posts) are created only by the creator.
- No "Claude" or Co-Authored-By lines in commits.
- Talk to the creator simply.
- **Honesty about consciousness:** nobody can test for it today. The scorecard measures indicator features named by
  published theories, never "it is conscious".

**How the three work:**
- **They are not worlds like ACL or Cradle.** The workbench is a set of small fast tasks, one ability each; Imagine is a
  brain part; the scorecard is a fixed set of tests run on every brain.
- **GPT's ideas** (`gpt_view_projects_2026-11-11.md`) fold in:
  - Genesis is the workbench's "alone vs with others" condition;
  - Mirror is the second brain part, and a scorecard test;
  - Darwin is ACL;
  - Odyssey is Imagine's own goals;
  - Embody comes later.
- **The workbench's first experiment** is GPT's question: does a mind need other minds to develop, or can it become
  autonomous alone?

**Status:** this folder is local (git, no remote). Cloud runs need a GitHub repo, which the creator creates when ready.

## Log
- 2026-11-11: started. Three plans, drafts, not frozen: `workbench/plan.md`, `imagine/plan.md`, `scorecard/plan.md`.
- 2026-11-11: GPT's five ideas (pasted by the creator) folded in, labelled as GPT; the first workbench experiment is alone vs with others.
- 2026-11-13: W3 (drives only) council (GPT, Gemini, DeepSeek; two rounds), frozen (W3-frozen), built, checks All: PASS, calibration R = 200, launched (jobs_w3.py; 32 runs x 800,000 steps + tests; about 14-18 hours).

## Cloud runs (since 14 November 2026)
Public repo **github.com/abu4evere/mindlab** (the creator made it on 14 November). The workflow `.github/workflows/run.yml`
runs one study command on GitHub's machines: checks first (it stops unless they print All: PASS), then the command,
then the chosen paths saved as an artifact.
- Example: `gh workflow run run.yml -R abu4evere/mindlab -f name=WN -f dir=workbench/WN -f checks=checks_wn.py -f command="python run_all.py" -f save="output checks.log"`
- `gh` is at `C:\Users\User\gh\bin\gh.exe`.
- The first test (run 43670938233) passed WN's checks in the cloud, including M32 reproducing WS's saved local
  children exactly (the same numbers on Linux as on the PC).
- Long runs go to the cloud, so the creator's PC stays free. One job is limited to about 6 hours; split longer
  studies into jobs.
