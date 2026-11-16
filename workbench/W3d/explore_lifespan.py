"""Exploratory (after the data, labelled): paired lifespan and land-known differences (the frozen readings 2-3 read
survival, which was not 0 for P). Same bootstrap as the frozen analysis."""
import sys
sys.argv = ["x"]
src = open("analyse_w3d.py", encoding="utf-8").read().split("out = {")[0]
exec(compile(src.replace("Path(__file__).parent", "Path('.').resolve()"), "analyse_w3d_head", "exec"))
for a, b in (("P", "D3 (W3)"), ("PYFR", "D3 (W3)"), ("PYFR", "P"), ("PYFR", "YFR (W3b)"), ("PA", "P"), ("PA", "D3 (W3)")):
    print(f"{a} - {b}: lifespan {diff(a, b, 'lifespan')}; known_end {diff(a, b, 'known_end')}")
import json
for s in range(1, 9):
    l = json.load(open(f"output/test_PYFR_{s}.json"))
    print("PYFR seed", s, "full lives", int(sum(x["survived"] for x in l)), "of 50; mean lifespan", round(sum(x["lifespan"] for x in l) / 50))
