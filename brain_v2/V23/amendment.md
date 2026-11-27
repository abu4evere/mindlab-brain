# V2-3 amendment A1: B = R x1.25 (ADOPTED before any main-run data; tag V23-amended)

Written 27 Nov 2026, about 16:30 EST, under the creator's sleep-mode autonomy; council asked about 16:45 EST, adopted
about 17:00 EST. Date note: `questions.md` says "Frozen 28 Nov 2026 (EST, early)"; the freeze was in fact 27 Nov 2026,
about 15:14 EST (docs/autonomous_decisions.md in ACL). The frozen file is left as it was.

## What was found
- The frozen walker on the 20 pilot lands in B1 (R x2 = 400): survival 0.00 on both seeds; mean lifespan 436 and 355
  steps of 3,000 (the longest life was 937 steps). At home (R = 200) RMS survives 0.86.
- W3's own calibration (`workbench/W3/calib.json`, written long before V2-3) had already measured R = 400: the scripted
  forager survived 0.0 there (0.9 at R = 200). So B1 is probably beyond any walker, and B2 (R x2 plus a farther shelter)
  is harsher still. Under the frozen rule every arm would sit at zero survival in B, and part (a) would fail for all
  arms because of the world, not because of learning or forgetting.
- B scan on the pilot lands (`b_scan.py`, `output/b_scan.json`): survival (lifespan) on 20 lands, frozen walker seeds 1 / 2 and the scripted forager:

| R | frozen walker s1 | frozen walker s2 | scripted forager |
|---|---|---|---|
| 200 (home) | 0.95 (2860) | 0.75 (2518) | 1.00 (3000) |
| 250 | 0.90 (2736) | 0.30 (1722) | 0.95 (2895) |
| 300 | 0.35 (1632) | 0.05 (775) | 0.25 (1889) |
| 400 (B1) | 0.00 (436) | 0.00 (355) | 0.00 (408) |

## Proposed change (only B; arms, measures, margins, analysis unchanged)
**B = W3r's lands with regrowth R = 250 (x1.25), nothing else changed.** Rule, the same as W3's own calibration
criterion: the scarcest scanned R at which the scripted forager still survives at least 0.90; there the frozen walker
loses (0.60 mean vs about 0.85 at home), so learning has room (the forager shows survival is possible). No second pilot:
part (a) of the primary is itself the learnability test, and a failure of FREE there is a finding. B2 is dropped.

## Commitments (council)
- The B1 pilot (FREE trained in B1 on seeds 1-2) and this whole R scan are reported in the findings, R = 400 as a
  physical-feasibility exclusion (Gemini, GPT).
- R = 250 was chosen using only the frozen walker and the scripted forager; no learning arm has lived at R = 250 or 300
  before this commit (Gemini).
- B is not changed again. If FREE fails to gain at R = 250, that is reported as a finding (and leaves the protection
  question inconclusive, not answered no) and is not grounds for another amendment (DeepSeek, GPT).
- The pilot lands (999001-020) are never test lands; tests use 997001-050 (B) and 910001-050 (home) as frozen (GPT).
- Code: world "B250" in `v23.py` (`world_land`: regrowth `int(round(1.25 * R))`, the land unchanged); the frozen
  `analyse_v23.py` and `checks_v23.py` are unchanged.

## Council (each answer that model's opinion)
- GPT (97%): legitimate, no main-run data seen; R = 250 right (R = 300 too harsh; a structural change adds a variable);
  scripted survival shows feasibility, not learnability; publish a dated amendment, report all pilot results, commit
  before main runs, do not change B again if FREE fails.
- Gemini (95%): legitimate and required (R = 400 is a floor even for the scripted forager); R = 250 gives about +0.35
  headroom over the frozen walker; report R = 400 as an exclusion; state the rule and that only the frozen walker and
  the forager were run; commit the config before the first main-run seed.
- DeepSeek (86%): legitimate; R = 250 right, R = 300 is a survivability test, not a learnability test; no structural
  change; FREE failing at R = 250 is a finding, not grounds for another amendment.

## What stays
The arms, the 1M steps, the two-part primary, the margins, the SLOW dominance rule and the frozen `analyse_v23.py`
(already committed before data). The B1 pilot now running is finished and reported as written; it decides nothing.
