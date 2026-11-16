# WG2 implementation notes (written before the run)

- **`wg2.py` is WI's run with WI's dream extended to report the best imagined patch** (the most food eaten). The
  dream's draws and learning are WI's, so IM here reproduces WI's IM. Checked on seed 1:
  - activity, reach, dreams and the after-room lives are exact;
  - the pattern measure was compared within 0.002 (see below).
- **IQ:** after each dream with any food eaten, the best patch's 4 cells get `m_last = t − 10,000` in the waking map
  memory, so W3's uncertainty there is about 1. Nothing else changes.
- **Questions answered:** a question counts as answered if any of its cells is written as seen (`m_last > t_posed`)
  within 500 steps.
  - IM gets one random 2 × 2 block per dream, from the remembered land by W3's `_blocks`, with `[seed, 52]`. It is
    tracked the same way but not marked: the chance rate.
- **A platform note found by the checks:** zlib's compressed size can differ by one byte between Windows and the
  cloud's Linux (WI's IM seed 1, window 1: 0.153 locally against 0.154 on the cloud). Behaviour is identical. All WG2
  arms run on the cloud, so the comparisons are within one platform.
- Cloud: 2 jobs (IM, IQ), 8 seeds each. Checks: All: PASS (`checks.log`).
