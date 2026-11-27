"""BV1's gate (questions.md, BV1-frozen; the creator's sign-off 26 Nov 2026): exact parity.

One full life per seed in each arm, W3r's RM kept copy (RM_CS_{seed}.npz, copied into brains/), on that seed's first
fresh test land (W3i's FRESH_SEEDS[0]), the same random stream in every arm:
  NATIVE     W3r's own wiring (MeaningWorld)
  BODY       Body v1 + the Mind Lab adapter (body_v1.BodyWorld)
  BODY-SHUF  as BODY, colour codes and verb numbers renamed per land
Compared at every step: the action, the body state (position, energy, fatigue), the brain's input layers (obs_map)
and the table's counts (renamed back for BODY-SHUF). Pass: every life identical in all three arms, the 8 lives cover
wall hits, meals below and at the energy cap, rests at the shelter and map edges (else seeds 9-16 are added, the
frozen rule), and BODY on seed 1 run twice gives the same life.
  python bv1.py            -> output/gate.json, output/gate.md
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import body_v1 as B1  # noqa: E402  (W3r's chain first: the numerical settings before numpy loads)
import numpy as np  # noqa: E402
from body_v1 import w3r, W  # noqa: E402

w3k, w3i = w3r.w3k, w3r.w3n.w3i
R3 = w3k.R3
BRAINS, OUT = HERE / "brains", HERE / "output"
ARMS = ("NATIVE", "BODY", "BODY-SHUF")
NEED = ("wall_hits", "meals_below_cap", "meals_at_cap", "rests_at_shelter", "edge_steps")


def life(arm, seed):
    w3r.configure("RM", seed)
    W.World = w3r.MeaningWorld if arm == "NATIVE" else B1.BodyWorld
    B1.BV1["rename"] = arm == "BODY-SHUF"
    net = w3k.load_npz(BRAINS / f"RM_CS_{seed}.npz", seed)
    ls = w3i.FRESH_SEEDS[0]
    land, R, rng = W.make_land(ls), R3.regrowth(), np.random.default_rng(ls)
    rec, cov, prev = [], dict.fromkeys(NEED, 0), {}

    def on_step(w, a, d0, cur):
        perm = w.adapter.cperm if arm != "NATIVE" else np.arange(8)
        rec.append((int(a), tuple(w.pos), float(w.E), float(w.F), w.obs_map().copy(),
                    w.mod.pos[perm].copy(), w.mod.neg[perm].copy()))
        x, y = w.pos
        cov["edge_steps"] += x in (1, W.N - 2) or y in (1, W.N - 2)
        if arm == "BODY":
            fb = w.last_feedback
            cov["wall_hits"] += a != 4 and not fb["place_changed"]
            if fb["energy"][1] > 0:
                cov["meals_at_cap" if prev.get("E") == W.EMAX else "meals_below_cap"] += 1
            cov["rests_at_shelter"] += fb["fatigue"][1] < 0
        prev["E"] = w.E

    w, m = R3.run_life(w3i.policy(net, rng), land, R, rng, on_step=on_step)
    return rec, cov, {"lifespan": int(w.t), "died": bool(w.dead)}


def first_mismatch(r0, r1):
    names = ("action", "position", "energy", "fatigue", "brain input layers", "table positives", "table negatives")
    for i, (s0, s1) in enumerate(zip(r0, r1)):
        for k, name in enumerate(names):
            same = np.array_equal(s0[k], s1[k]) if isinstance(s0[k], np.ndarray) else s0[k] == s1[k]
            if not same:
                return {"step": i + 1, "what": name}
    if len(r0) != len(r1):
        return {"step": min(len(r0), len(r1)) + 1, "what": "life length"}
    return None


def main():
    OUT.mkdir(exist_ok=True)
    t0, res = time.time(), {"seeds": {}, "machine": w3k.machine.__doc__ and None}
    import platform
    res["machine"] = {"platform": platform.platform(), "python": platform.python_version(),
                      "numpy": np.__version__, "processor": platform.processor()}
    total = dict.fromkeys(NEED, 0)
    seeds, s = [], 1
    while s <= 16:
        if s > 8 and all(total[k] > 0 for k in NEED):
            break
        recs = {a: life(a, s) for a in ARMS}
        r = {"lifespan": recs["NATIVE"][2], "coverage": recs["BODY"][1],
             "BODY_vs_NATIVE": first_mismatch(recs["NATIVE"][0], recs["BODY"][0]),
             "BODY-SHUF_vs_NATIVE": first_mismatch(recs["NATIVE"][0], recs["BODY-SHUF"][0])}
        for k in NEED:
            total[k] += r["coverage"][k]
        res["seeds"][s] = r
        seeds.append(s)
        print(s, r, flush=True)
        s += 1
    again = life("BODY", 1)
    res["determinism_BODY_seed1"] = first_mismatch(life("BODY", 1)[0], again[0])
    res["coverage_total"] = total
    res["coverage_met"] = all(total[k] > 0 for k in NEED)
    res["parity"] = all(r["BODY_vs_NATIVE"] is None and r["BODY-SHUF_vs_NATIVE"] is None for r in res["seeds"].values())
    res["PASS"] = res["parity"] and res["coverage_met"] and res["determinism_BODY_seed1"] is None
    res["seconds"] = round(time.time() - t0, 1)
    (OUT / "gate.json").write_text(json.dumps(res, indent=1, default=str))
    L = ["# BV1 gate result", "", f"Seeds run: {seeds}; machine: {res['machine']}", "",
         "| seed | lifespan (NATIVE) | BODY vs NATIVE | BODY-SHUF vs NATIVE | wall hits | meals <cap | meals at cap | rests | edge steps |",
         "|---|---|---|---|---|---|---|---|---|"]
    for k, r in res["seeds"].items():
        c = r["coverage"]
        L.append(f"| {k} | {r['lifespan']['lifespan']} | {r['BODY_vs_NATIVE'] or 'identical'} | "
                 f"{r['BODY-SHUF_vs_NATIVE'] or 'identical'} | {c['wall_hits']} | {c['meals_below_cap']} | "
                 f"{c['meals_at_cap']} | {c['rests_at_shelter']} | {c['edge_steps']} |")
    L += ["", f"Coverage met: {res['coverage_met']} ({total}); determinism (BODY seed 1 twice): "
          f"{res['determinism_BODY_seed1'] or 'identical'}", "", f"**Gate: {'PASS' if res['PASS'] else 'FAIL'}**"]
    (OUT / "gate.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
