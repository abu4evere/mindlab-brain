"""V2-3 B check (on the pilot lands only, no arm trained): can B be survived, and does the frozen walker lose there?
For regrowth R in {200, 250, 300, 400} (home R = 200; B1 = 400), on pilot lands 999001-999020 in W3r's world: the
frozen walker (RMS seeds 1-2, its reflexes on) and W3's scripted forager (W.Script, the calibration's reference).
W3's calibration (workbench/W3/calib.json, plain world): Script survived 0.0 at R = 400 and 0.9 at R = 200.
  python b_scan.py  -> output/b_scan.json
"""
import json
import sys
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import numpy as np  # noqa: E402
import v23  # noqa: E402
from v23 import W, R3, w3m  # noqa: E402


def job(arg):
    R, who, seed = arg
    out = []
    for ls in v23.PILOT_LANDS:
        v23.configure(seed)
        land = W.make_land(ls)
        rng = np.random.default_rng(ls)
        if who == "Script":
            s = W.Script()
            pol = lambda w: s.act(W.MapView(w))  # noqa: E731
        else:
            net, rfx = v23.load_rms(seed), w3m.Reflex()
            pol = lambda w: rfx.act(w, net.act(w.obs_map(), R3.levels(w, "D3"), w.pos, rng)[0])  # noqa: E731
        _, m = R3.run_life(pol, land, R, rng)
        out.append((float(m["survived"]), float(m["lifespan"])))
    return {"R": R, "who": who, "seed": seed, "survival": float(np.mean([o[0] for o in out])),
            "lifespan": float(np.mean([o[1] for o in out]))}


if __name__ == "__main__":
    jobs = [(R, who, s) for R in (200, 250, 300, 400) for who in ("FROZEN", "Script") for s in (1, 2)]
    with Pool(11) as p:
        rows = p.map(job, jobs)
    (v23.OUT / "b_scan.json").write_text(json.dumps(rows, indent=1))
    for r in rows:
        print(r)
