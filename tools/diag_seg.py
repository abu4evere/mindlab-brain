"""On the runner it lands on: a short W3d training under each numerical setting, each in its own process."""
import os, subprocess, sys
cpu = next(l for l in open("/proc/cpuinfo") if l.startswith("model name")).split(":", 1)[1].strip()
print("cpu", cpu, flush=True)
prog = ("import sys; sys.path.insert(0,'workbench/W3i'); import w3i; from w3i import w3d, R3; "
        "w3i.install(); w3d.ARMS['X']={'parts':'YR','always':False}; w3d.configure('X'); w3d.CFG.update(child=1500); "
        "n,s,_=w3d.train_net_parent('X',4,3000,R3.regrowth(),hours=1.0); import hashlib; print('ok', hashlib.sha256(b''.join(n.p[k].tobytes() for k in sorted(n.p))).hexdigest()[:16])")
N = "AVX512_SPR AVX512_ICL X86_V4"
variants = {"npy_all": {"NPY_DISABLE_CPU_FEATURES": N},
            **{f"core_{c}": {"OPENBLAS_CORETYPE": c, "NPY_DISABLE_CPU_FEATURES": N}
               for c in ("Zen", "Sandybridge", "Nehalem", "Prescott")}}
for name, env in variants.items():
    e = dict(os.environ, OPENBLAS_NUM_THREADS="1", **env)
    r = subprocess.run([sys.executable, "-c", prog], env=e, capture_output=True, text=True, cwd="..")
    print(name, "exit", r.returncode, (r.stdout.strip().splitlines() or [""])[-1], r.stderr.strip()[-200:], flush=True)
