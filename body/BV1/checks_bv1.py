"""BV1's adapter audit (questions.md, gate item 1): run BEFORE any brain is attached. A scripted random body (no brain)
lives 500 steps on 4 fresh lands, once without renaming and under 3 renamings, with the same verb sequence (drawn by
verb name, then sent as that renaming's verb number). Checks:
  1. legality and availability: every verb number is always legal; the verb list never changes within a life;
  2. ordering and hidden state: every output other than the eyes (place_changed, the energy and fatigue parts, the
     body quantities, self) is identical under every renaming, so it can carry no information that depends on which
     looks mean what;
  3. the eyes and touch under a renaming are exactly the renamed unrenamed looks (a consistent relabelling, nothing
     added);
  4. the feedback's keys are only the body's own (no field naming food, wall or shelter);
  5. the meaning table learns only through the feedback: its counts, renamed back, are identical under every renaming.
Prints "All: PASS" when every check passes.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import body_v1 as B1  # noqa: E402
import numpy as np  # noqa: E402
from body_v1 import w3r, W  # noqa: E402

w3i = w3r.w3n.w3i
LANDS, STEPS, RENAMINGS = list(w3i.FRESH_SEEDS)[:4], 500, (None, 11, 12, 13)
FB_KEYS = {"verb", "place_changed", "energy", "fatigue", "energy_after", "fatigue_before"}


def scripted(ls, rename):
    w3r.configure("RM", 1)
    B1.BV1["rename"] = rename is not None
    if rename is not None:
        B1.BV1_SEED, keep = 20261126 + rename, B1.BV1_SEED
    w = B1.BodyWorld(W.make_land(ls), w3k_R())
    if rename is not None:
        B1.BV1_SEED = keep
    ad, rng, out = w.adapter, np.random.default_rng(ls), []
    lists = {tuple(ad.verb_numbers())}
    for _ in range(STEPS):
        if w.done():
            break
        name_idx = int(rng.integers(len(B1.VERBS)))
        number = int(ad.vperm[name_idx])
        assert all(ad.legal(v) for v in range(len(B1.VERBS)))
        s = ad.senses()
        fb, _, _ = ad.act(number)
        lists.add(tuple(ad.verb_numbers()))
        out.append({"eyes_native": np.argsort(ad.cperm)[s["eyes"]], "eyes": s["eyes"], "cperm": ad.cperm,
                    "touch": s["touch"], "self": dict(s["self"], facing=None), "feelings": s["feelings"],
                    "fb": {k: v for k, v in fb.items() if k != "verb"}, "fb_keys": set(fb), "name": name_idx})
    return out, lists, w


def w3k_R():
    return w3r.w3k.R3.regrowth()


def main():
    ok = True
    for ls in LANDS:
        runs = {r: scripted(ls, r) for r in RENAMINGS}
        base = runs[None][0]
        for r in RENAMINGS:
            rec, lists, _ = runs[r]
            c1 = len(lists) == 1
            c2 = len(rec) == len(base) and all(x["fb"] == y["fb"] and x["self"] == y["self"] and
                                               x["feelings"] == y["feelings"] for x, y in zip(rec, base))
            c3 = all(np.array_equal(x["eyes_native"], y["eyes"]) and
                     all(x["touch"][k] == int(x["cperm"][y["touch"][k]]) for k in y["touch"]) for x, y in zip(rec, base))
            c4 = all(x["fb_keys"] == FB_KEYS for x in rec)
            print(f"land {ls} renaming {r}: 1 legality/availability {c1}, 2 non-eye outputs identical {c2}, "
                  f"3 eyes/touch a pure relabelling {c3}, 4 feedback keys body-only {c4}")
            ok &= c1 and c2 and c3 and c4
        # 5: the table, renamed back, is identical under every renaming (it learns only through the feedback)
        t0 = runs[None][2].mod
        for r in RENAMINGS[1:]:
            w = runs[r][2]
            p = w.adapter.cperm
            c5 = np.array_equal(w.mod.pos[p], t0.pos) and np.array_equal(w.mod.neg[p], t0.neg)
            print(f"land {ls} renaming {r}: 5 table renamed back identical {c5}")
            ok &= c5
    print("All: PASS" if ok else "All: FAIL")


if __name__ == "__main__":
    main()
