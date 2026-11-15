import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import wd
out = Path(__file__).parent / "output"
out.mkdir(exist_ok=True)
part = int(sys.argv[1])
cells = [(a, n) for a in wd.ARMS for n in (32, 128)]
for a, n in cells[part::2]:
    for s in range(1, 49):
        (out / f"{a}_{n}_seed_{s}.json").write_text(json.dumps(wd.run_child(a, n, s)), encoding="utf-8")
    print("done", a, n, flush=True)
