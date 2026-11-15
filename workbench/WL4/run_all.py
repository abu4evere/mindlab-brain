import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import wl4
out = Path(__file__).parent / "output"
out.mkdir(exist_ok=True)
part = int(sys.argv[1])
cells = [(w, a, n) for w in wl4.WORLDS for a in wl4.ARMS for n in (32, 128)]
for w, a, n in cells[part::2]:
    for s in range(1, 25):
        (out / f"{w}_{a}_{n}_seed_{s}.json").write_text(json.dumps(wl4.run_child(w, a, n, s)), encoding="utf-8")
    print("done", w, a, n, flush=True)
