import os, json, sys
mode = sys.argv[1]
if mode == "pin":
    os.environ["OPENBLAS_CORETYPE"] = "Haswell"; os.environ["NPY_DISABLE_CPU_FEATURES"] = "AVX512_SPR AVX512_ICL X86_V4"
import numpy as np
from numpy._core._multiarray_umath import __cpu_features__ as f, __cpu_dispatch__ as d, __cpu_baseline__ as b, __cpu_targets_info__ as t
cur = sorted({v["current"] for fn in t.values() for v in fn.values()})
print(mode, "baseline", b, "dispatch", d, "AVX512F", f.get("AVX512F"), "X86_V4", f.get("X86_V4"), "current targets", cur)
print(open("/proc/cpuinfo").read().split("model name")[1].split("\n")[0])
