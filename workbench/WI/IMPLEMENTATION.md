# WI implementation notes (written before the run)

- **The brain:** W3c's GYFR weights in W3c's gated class (as trained). In the room both needs are 0, so the gate is
  inert there; in dreams the imagined body has needs, so the gate acts as it did in training.
- **Learning:** W3's A2C (64-step segments, W3's reward and settings) through a small segment helper. The waking
  segment is closed before each dream. Each dream has its own segments, closed at its end.
- **Dreams:** after room steps 500, 1,000, … 9,500 (19 dreams; none at the very end).
  - The imagined world is a W3 World over a land built from the map memory: remembered walls, border wall, unknown
    open; the remembered shelter; 3 patches by W3's own `_blocks` placement over that land, from `[seed, 51]`.
  - The imagined body is E ~ U(40, 150) and F ~ U(0, 150).
- **L reproduces WQ's GYFR living stay** on room 900001 (checked).
- **After the room:** the test of W3, W3b and W3c (learning off; one generator per test land). "Pre" is W3c's own
  `test_GYFR` for the same seeds.
- Cloud: 2 jobs (L, IM), 8 seeds each. Checks: All: PASS (`checks.log`).
