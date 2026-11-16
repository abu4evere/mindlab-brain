"""WX summary (questions.md): death labels per seed, then the mean over seeds; meals and first meal; Script beside."""
import json
import numpy as np
S = range(1, 9)
rows = []
for s in S:
    L = json.load(open(f"output/PYFR_{s}.json"))
    dead = [l for l in L if l["dead"]]
    lab = {k: (np.mean([d["labels"][k] for d in dead]) if dead else float("nan")) for k in ("no_food_known", "food_known_not_reached", "exhaustion")}
    rows.append({"seed": s, "deaths": len(dead), **lab, "meals": np.mean([l["meals"] for l in L]),
                 "first_meal": np.mean([l["first_meal"] if l["first_meal"] is not None else l["lifespan"] for l in L]),
                 "tired": np.mean([l["tired_share"] for l in L]), "known500": np.mean([l["known500"] for l in L]),
                 "lifespan": np.mean([l["lifespan"] for l in L]), "meals_per_100": np.mean([100 * l["meals"] / l["lifespan"] for l in L])})
print("seed deaths noFood knownNotReached exhaustion meals first_meal tired known500 lifespan meals/100steps")
for r in rows:
    print(r["seed"], r["deaths"], *(f"{r[k]:.2f}" for k in ("no_food_known", "food_known_not_reached", "exhaustion")),
          f"{r['meals']:.1f} {r['first_meal']:.0f} {r['tired']:.2f} {r['known500']:.2f} {r['lifespan']:.0f} {r['meals_per_100']:.2f}")
m = {k: float(np.nanmean([r[k] for r in rows])) for k in ("no_food_known", "food_known_not_reached", "exhaustion", "meals", "first_meal", "tired", "known500", "meals_per_100")}
print("mean over seeds", {k: round(v, 3) for k, v in m.items()})
sc = json.load(open("output/Script.json"))
print("Script: deaths", sum(l["dead"] for l in sc), "meals", round(np.mean([l["meals"] for l in sc]), 1), "first_meal", round(np.mean([l["first_meal"] or 0 for l in sc])),
      "tired", round(np.mean([l["tired_share"] for l in sc]), 3), "known500", round(np.mean([l["known500"] for l in sc]), 2),
      "meals/100", round(np.mean([100 * l["meals"] / l["lifespan"] for l in sc]), 2))
