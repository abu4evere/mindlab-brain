import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import ws
out = Path(__file__).parent / "output"
for b in ws.BRAINS:
    for s in range(1, 49):
        ws.run(b, s, out)
    print("done", b, flush=True)
