# W3n: moved to this PC (20 Nov 2026, after data from 33 of 48 jobs)
GitHub disabled the repository abu4evere/mindlab (terms of service) while 15 jobs were running; their partial progress was
on GitHub and is lost. The creator's standing permission (18 Nov: if GitHub cannot run a study, run it on the PC) is used:
the 15 jobs restart from step 0 here, 4 at a time (the PC's limit), with the frozen code unchanged. This PC (Intel Core
i3-1315U, Windows) is not one of the machines verified to train bit-identically with GitHub's; a run here is its own
numerical path. Pairing by seed with W3m's SL stays (same seed, same code); the findings will state which seeds ran where.

## 20 Nov 2026, 20:34: the 8 CR runs move to a Google Cloud VM
The creator set up a Google Cloud VM (n2-standard-8, Intel Xeon, Ubuntu 26.04, Python 3.14.4, numpy 2.5.3; 35.221.60.73).
The PC queue runner (run_local_7.py) was stopped before it started any CR run; CR 1, 2, 5, 8, 10, 11, 12, 16 run on the VM
(gcp_CR_<seed>.out there). Frozen code unchanged. The PC and the VM do not train bit-identically (machine_check.py in W3o);
each run's machine is in its machine_<arm>_<seed>.json. The PC keeps HR 4/10/15, HC 1 (running) and HC 5/12/14 (paused while
the creator uses the PC).
