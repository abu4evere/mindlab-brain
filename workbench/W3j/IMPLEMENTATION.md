# W3j implementation notes (written before the run)

- **`w3j.py` reuses W3i's world** (`StaleWorld`, the test with WX's death labels, the fresh lands) and W3d's training
  loop.
- **CK:** `brains3.LR` is set to 0.001 for every call of the training loop that starts at or after the fade snapshot.
  All updates go through `DriveVIN.apply`, so actor-critic, "that worked!" and replay are all scaled. It is restored
  afterwards.
- **CV:** W3d's copy weight and "parent present" functions are swapped, inside W3d's training namespace, for ones that
  keep the parent at 0.05 after the fade.
- **CF:** CK's end-of-fade snapshot (`test_CK_<seed>_1200k.json`). A check shows it equals C's own snapshot at that
  point.
- **Drift and parent agreement:** a replay of the final brain's own test lives, with the same generator, comparing
  greedy moves with the end-of-fade brain and with W3's Script on the same map view.
- **Checks: All: PASS (9).** Two check names first held non-ASCII characters that the Windows console could not
  print; they were renamed. The checks themselves are unchanged.
- **Cloud:** 33 jobs (CK, CV, C4, C2 × 8, and the reproduction job); `manage_w3j.py` resumes and collects.
