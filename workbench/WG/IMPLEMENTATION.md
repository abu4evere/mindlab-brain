# WG implementation notes (written before the run)

- `wg.py` reuses WN's network (`../WN/wn.py`) and WS's task. Only the growth step differs by brain. G uses WN's own
  growth (`wn.Net.grow`), so M32 and G on seed 1 equal WN's saved children (checked).
- GA and GF draw new connections from the same growth stream as WN's G (`[seed, 9]`), at a born neuron's scale (0.1).
  In GF, the new outgoing connections go to the hands and to the old neurons. In GA they start at zero.
- Growth happens at the end of the growth day, after that day's tests, as in WN.
- Manipulation measure: the mean |M| over the born neurons' columns against the added ones' at day 60.
- Checks: All: PASS (`checks.log`). The checks ran GA32, GF and M128 on seed 2 without printing any skill.
