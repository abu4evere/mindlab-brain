"""Exploratory (after the data, labelled): the frozen reading 2 gave NaN because IQ seed 4 posed no question (it ate
nothing in any dream). Here: answered-within-500 over the seeds that posed questions, paired with IM's random blocks;
and per-seed lifespans after the room."""
import json
import numpy as np
S = range(1, 9)
R = {a: {s: json.load(open(f"output/{a}_{s}.json")) for s in S} for a in ("IM", "IQ")}
ok = [s for s in S if R["IQ"][s]["questions"]]
iq = np.array([np.mean([q["answered"] is not None for q in R["IQ"][s]["questions"]]) for s in ok])
im = np.array([np.mean([q["answered"] is not None for q in R["IM"][s]["questions"]]) for s in ok])
idx = np.random.default_rng(20261133).integers(0, len(ok), (10_000, len(ok)))
ci = lambda v: [round(float(v.mean()), 3), round(float(np.percentile(v[idx].mean(1), 2.5)), 3), round(float(np.percentile(v[idx].mean(1), 97.5)), 3)]
print("seeds with questions:", ok)
print("IQ answered", ci(iq), "IM random blocks", ci(im), "IQ - IM", ci(iq - im))
for s in S:
    print(s, "questions", len(R["IQ"][s]["questions"]), "life IM", round(np.mean([l["lifespan"] for l in R["IM"][s]["after"]])),
          "life IQ", round(np.mean([l["lifespan"] for l in R["IQ"][s]["after"]])))
