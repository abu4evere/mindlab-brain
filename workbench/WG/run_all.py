import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import wg
out = Path(__file__).parent / "output"
for b in wg.BRAINS:
    for s in range(1, 49):
        wg.run(b, s, out)
    print("done", b, flush=True)
