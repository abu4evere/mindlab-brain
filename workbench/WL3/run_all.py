import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import wl3
out = Path(__file__).parent / "output"
part = int(sys.argv[1])                          # two processes: part 0 and part 1
cells = [(w, a, n) for w in wl3.WORLDS for a in wl3.ARMS for n in (32, 128)]
for w, a, n in cells[part::2]:
    for s in range(1, 25):
        import json
        (out / f"{w}_{a}_{n}_seed_{s}.json").parent.mkdir(exist_ok=True)
        (out / f"{w}_{a}_{n}_seed_{s}.json").write_text(json.dumps(wl3.run_child(w, a, n, s)), encoding="utf-8")
    print("done", w, a, n, flush=True)
