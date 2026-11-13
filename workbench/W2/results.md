# W2: planning on what one remembers (results)

Frozen as `W2-frozen`. world2.py, brains2.py, run_w2.py, analyse_w2.py (written before any training).

## Validity

- Code checks (All: PASS): **yes**
- All 48 runs present: **yes**
- Scripted controls run: **yes**
- Bp, familiar efficient detour 1.000 (at least 0.90): **yes**
- B0 and the reactive controls, new-room efficient detour at most 0.20 (highest 0.083): **yes**
- **W2 is valid.**

## The scripted controls

| brain | detour new | detour familiar | control new | control familiar | empty | look-alike correct side |
|---|---|---|---|---|---|---|
| Bp | 0.125 | 1.000 | 0.925 | 0.967 | 1.000 | 0.662 |
| B0 | 0.000 | 0.000 | 0.925 | 0.925 | 1.000 | 0.500 |
| G | 0.000 | 0.000 | 0.908 | 0.908 | 1.000 | 0.000 |
| W | 0.075 | 0.075 | 0.933 | 0.933 | 1.000 | 0.500 |
| W2 | 0.000 | 0.000 | 0.933 | 0.933 | 1.000 | 0.500 |
| H2 | 0.000 | 0.000 | 0.933 | 0.933 | 1.000 | 0.500 |
| M- | 0.083 | 0.083 | 0.917 | 0.917 | 1.000 | 0.500 |

## The learned brains (16 seeds, 150,000 episodes): mean [95% bootstrap over seeds]

| measure | M | M0 | R |
|---|---|---|---|
| efficient detour, new room | 0.110 [0.091, 0.136] | 0.086 [0.066, 0.107] | 0.125 [0.116, 0.134] |
| efficient detour, familiar room | 0.463 [0.378, 0.546] | 0.086 [0.066, 0.107] | 0.157 [0.145, 0.170] |
| the tour's use (familiar - new) | 0.352 [0.269, 0.432] | 0.000 [0.000, 0.000] | 0.032 [0.023, 0.042] |
| control, new room | 0.860 [0.818, 0.897] | 0.691 [0.594, 0.779] | 0.798 [0.782, 0.814] |
| control, familiar room | 0.849 [0.797, 0.898] | 0.691 [0.594, 0.779] | 0.747 [0.734, 0.760] |
| empty room | 0.959 [0.917, 0.992] | 0.859 [0.764, 0.942] | 0.769 [0.755, 0.782] |
| look-alike: correct side | 0.263 [0.207, 0.323] | 0.449 [0.420, 0.475] | 0.494 [0.473, 0.516] |
| regret vs Bp, detour new (steps) | -1.027 [-1.413, -0.661] | -4.774 [-5.680, -3.966] | 1.621 [1.454, 1.791] |
| regret vs Bp, detour familiar (steps) | 0.731 [0.568, 0.907] | 1.237 [0.840, 1.674] | 5.681 [5.504, 5.859] |
| value-map correlation (true map) | 0.804 [0.719, 0.864] | 0.327 [0.245, 0.413] | – |

### M's memory probes (familiar detours)

- M: 0.463 [0.378, 0.546]; M-erase: 0.110 [0.091, 0.136]; M-shuffle: 0.184 [0.154, 0.214]
- M - M-erase: +0.352 [+0.269, +0.432]; M - M-shuffle: +0.279 [+0.217, +0.342]

## The frozen readings

- **Memory matters** (M - M0, familiar efficient detour): +0.377 [+0.296, +0.459] -> **yes**
- **Decisions follow memory:** M's look-alike correct side 0.263 [0.207, 0.323] (lower bound above 0.5: no); M - M-erase +0.352 [+0.269, +0.432] (above 0: yes) -> **no**
- **The given map beats a learned memory** (an architecture comparison; M - R, familiar): +0.305 [+0.222, +0.389] -> **yes**
- **Uses what it knows** (M familiar >= 0.80 x Bp's 1.000 = 0.800): M 0.463, absolute gap to Bp -0.537 -> **no**

## Secondary: bootstrap over layouts (2,000 draws; per-layout means over seeds)

- M - M0, familiar: +0.377 [+0.332, +0.420]
- M - R, familiar: +0.305 [+0.248, +0.358]
- M - M-erase: +0.352 [+0.301, +0.402]
- M's look-alike correct side (over the 40 pairs): 0.263 [0.218, 0.309]

M's memory is engineered (a fixed writer); its planner is learned. Behaviour, not proof of an inner look-ahead.

