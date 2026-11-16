"""Exploratory (after the data, labelled): paired lifespan differences, which the frozen reading 4 did not use
because GYFR's survival (0.013) was not 0. Same bootstrap as the frozen analysis."""
import sys
sys.argv = ["x"]
src = open("analyse_w3c.py", encoding="utf-8").read().split("learned_all_zero")[0]
exec(compile(src.replace("Path(__file__).parent", "Path('.').resolve()"), "analyse_w3c_head", "exec"))
for a, b in (("G", "D3 (W3)"), ("Gi", "D3i (W3)"), ("GYFR", "YFR (W3b)"), ("G", "Z0"), ("GYFR", "G")):
    print(f"{a} - {b} lifespan {diff(a, b, 'lifespan')}")
import json
for s in range(1, 9):
    l = json.load(open(f"output/test_GYFR_{s}.json"))
    print("GYFR seed", s, "survived lives", sum(x["survived"] for x in l), "mean lifespan", round(sum(x["lifespan"] for x in l) / 50))
