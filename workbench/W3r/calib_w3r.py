"""W3r pilot (questions.md: the ensemble's learning rate is set BEFORE the study, on pilot seeds 9001-9004, never study
seeds, by how fast it ranks the food colour first; then frozen). No brain is trained here: W3's parent script (which
reads the map memory) lives one life on each pilot land with W3o's changing colours, and the ensemble learns from its
consequences. For each candidate rate: the median step (over the 4 lands) at which "fed" first ranks the land's food
colour above wall, shelter and floor after its first meal (never = LIFE + 1). Among the STABLE rates (every member's
weights finite and at most 10 in size on every pilot land; amendment before data, 24 Nov: 1.0 diverged to 7e37) the
fastest wins; ties go to the smaller rate.
Writes calib_w3r.json.

  python calib_w3r.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import w3r  # noqa: E402
import numpy as np  # noqa: E402
from w3r import W, w3k  # noqa: E402
from w3k import R3  # noqa: E402

PILOT = (9001, 9002, 9003, 9004)
RATES = (0.01, 0.03, 0.1, 0.3, 1.0)


def one(lr, seed, R):
    w3r.ENS["lr"] = lr
    w = W.World(W.make_land(seed), R)
    script = W.Script()
    while not w.done():
        w.step(script.act(W.MapView(w)))
    big = float(np.abs(w.mod.w).max())
    return (w.food_first if w.food_first is not None else W.LIFE + 1), w.fair_fed, big


def main():
    w3r.w3o._configure_n("RE5", 1)
    W.World = w3r.MeaningWorld
    w3r.w3o.EYES.update(mode="vary", swap=False)
    w3r.MOD.update(module="ens", oracle=False)
    R = R3.regrowth()
    res = {}
    for lr in RATES:
        runs = [one(lr, s, R) for s in PILOT]
        res[lr] = {"food_first": [r[0] for r in runs], "fair_fed": [r[1] for r in runs],
                   "max_weight": [r[2] for r in runs], "median": float(np.median([r[0] for r in runs])),
                   "stable": bool(all(np.isfinite(r[2]) and r[2] <= 10.0 for r in runs))}
        print(lr, res[lr], flush=True)
    best = min((r for r in RATES if res[r]["stable"]), key=lambda r: (res[r]["median"], r))
    (HERE / "calib_w3r.json").write_text(json.dumps({"lr": best, "pilot_seeds": PILOT, "results":
                                                     {str(k): v for k, v in res.items()}}, indent=1))
    print("chosen lr", best)


if __name__ == "__main__":
    main()
