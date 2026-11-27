"""V2-3's pilot rule (questions.md): seeds 1-2, pilot lands 999001-999020, FREE trained 1M steps in B1.
If FREE - FROZEN survival in B1 (mean over the two seeds) is at least +0.08, B = B1; otherwise B = B2.
  python pilot_decide.py  -> output/pilot_decision.json
"""
import json
from pathlib import Path

import numpy as np

OUT = Path(__file__).parent / "output"


def surv(name):
    L = [json.loads(x) for x in (OUT / name).read_text().splitlines() if x.strip()]
    assert len(L) == 20 and len({x["land"] for x in L}) == 20 and all(x["world"] == "B1" for x in L), name
    return float(np.mean([x["survived"] for x in L])), float(np.mean([x["lifespan"] for x in L]))


rows = {s: {"FREE": surv(f"P_FREE_{s}_pilot.jsonl"), "FROZEN": surv(f"P_FROZEN_{s}.jsonl")} for s in (1, 2)}
gain = float(np.mean([rows[s]["FREE"][0] - rows[s]["FROZEN"][0] for s in rows]))
res = {"per_seed": {s: {a: {"survival": v[0], "lifespan": v[1]} for a, v in r.items()} for s, r in rows.items()},
       "FREE_minus_FROZEN_survival": gain, "B": "B1" if gain >= 0.08 else "B2"}
(OUT / "pilot_decision.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
