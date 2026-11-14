"""WE final test: each run's evolved schedule (median genes of the last generation) on 48 fresh children (seeds
1001-1048), beside WG's GA, M32 and M128. Writes output/<brain>_seed_<s>.json and evolved.json."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import we  # noqa: E402

HERE = Path(__file__).parent
SEEDS = range(1001, 1049)
brains = {"GA": (16, {8: 32, 16: 64, 24: 128}), "M32": (32, {}), "M128": (128, {})}
evolved = {}
for run in (1, 2):
    last = json.loads((HERE / f"evo_run{run}.json").read_text())[-1]
    med = np.median(np.array(last["genes"]), axis=0)
    n0, sched = we.schedule(med)
    evolved[f"E{run}"] = {"median_genes": [float(x) for x in med], "born": n0, "schedule": sched}
    brains[f"E{run}"] = (n0, sched)
(HERE / "evolved.json").write_text(json.dumps(evolved, indent=1), encoding="utf-8")
out = HERE / "output"
out.mkdir(exist_ok=True)
for b, (n0, sched) in brains.items():
    for s in SEEDS:
        r = we.run_child(n0, sched, s, tests=True)
        r["brain"], r["seed"] = b, s
        (out / f"{b}_seed_{s}.json").write_text(json.dumps(r), encoding="utf-8")
    print("done", b, flush=True)
