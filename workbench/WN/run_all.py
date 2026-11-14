import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import wn
out = Path(__file__).parent / "output"
for b in wn.BRAINS:
    for s in range(1, 25):
        wn.run(b, s, out)
    print("done", b, flush=True)
