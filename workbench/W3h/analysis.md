# W3h analysis (the frozen analysis, analyse_w3h.py)

- Checks All: PASS: **yes**
- All 32 runs present: **yes**

| arm | thorn steps / 1,000 | entries / opportunity | bout | lifespan | survived | near-thorn meal share (food there) |
|---|---|---|---|---|---|---|
| TH | 35.576 [30.971, 40.851] | 0.281 [0.267, 0.296] | 2.36 | 404.050 [328.904, 467.640] | 0.013 [0.003, 0.022] | 0.185 (0.178) |
| THP | 22.206 [15.403, 29.537] | 0.168 [0.129, 0.209] | 2.30 | 512.827 [424.502, 577.045] | 0.033 [0.013, 0.055] | 0.184 (0.178) |
| THw | 26.785 [20.122, 33.731] | 0.185 [0.143, 0.228] | 2.27 | 581.555 [501.318, 664.836] | 0.050 [0.033, 0.068] | 0.181 (0.178) |
| THPw | 14.296 [10.312, 18.542] | 0.142 [0.098, 0.188] | 2.22 | 581.663 [367.195, 789.773] | 0.070 [0.025, 0.117] | 0.181 (0.178) |

## Readings

- **1. Pain teaches avoidance (THP - TH, thorn steps / 1,000; upper < 0):** -13.370 [-22.802, -4.327] -> **yes**
- **2. Pain helps it live (THP - TH, lifespan; lower > 0):** 108.778 [-12.334, 217.437] -> **no**
- **3. Watching teaches avoidance (THw - TH, thorn steps / 1,000; upper < 0):** -8.791 [-19.158, 0.616] -> **no**
- **4. Pain adds to watching (THPw - THw, thorn steps / 1,000; upper < 0):** -12.490 [-22.347, -2.829] -> **yes**

## Secondary (paired differences, no gate)

- THP - TH: entries/opportunity -0.114 [-0.149, -0.075]; survived 0.020 [-0.003, 0.045]; near-thorn meal share -0.000 [-0.012, 0.013]
- THw - TH: entries/opportunity -0.096 [-0.151, -0.041]; survived 0.038 [0.018, 0.057]; near-thorn meal share -0.004 [-0.016, 0.008]
- THPw - THw: entries/opportunity -0.044 [-0.109, 0.016]; survived 0.020 [-0.030, 0.075]; near-thorn meal share 0.001 [-0.012, 0.014]
- THPw - THP: entries/opportunity -0.026 [-0.074, 0.028]; survived 0.037 [0.005, 0.070]; near-thorn meal share -0.003 [-0.020, 0.012]

## Training (means over seeds)

- TH: thorn steps / 1,000 per 100,000-step block: [43.1, 41.3, 44.0, 43.0, 36.6, 30.6, 29.5, 27.2, 26.0, 29.9, 29.6, 31.1, 32.2, 32.6, 32.3, 33.2, 35.2, 35.2, 34.1, 34.0]
  - the thorn channel's final weight norm: 0.599 (seeds: [0.878, 0.493, 0.475, 0.499, 0.479, 0.873, 0.629, 0.47])
- THP: thorn steps / 1,000 per 100,000-step block: [44.2, 41.6, 40.0, 38.1, 25.9, 21.9, 18.8, 17.6, 18.6, 18.7, 17.9, 17.9, 17.0, 17.2, 18.1, 19.4, 19.2, 17.2, 16.9, 17.1]
  - the thorn channel's final weight norm: 0.525 (seeds: [0.361, 0.563, 0.396, 0.779, 0.403, 0.584, 0.596, 0.514])
- THw: thorn steps / 1,000 per 100,000-step block: [23.8, 12.2, 8.6, 5.9, 5.9, 7.5, 8.5, 9.3, 10.6, 11.3, 12.3, 12.8, 15.2, 17.6, 19.6, 20.6, 21.8, 21.4, 21.2, 22.7]
  - the thorn channel's final weight norm: 0.560 (seeds: [0.451, 0.609, 0.608, 0.604, 0.478, 0.659, 0.58, 0.491])
- THPw: thorn steps / 1,000 per 100,000-step block: [24.0, 12.8, 8.7, 6.9, 7.8, 8.3, 9.2, 8.9, 10.2, 10.4, 12.3, 12.2, 13.3, 12.1, 12.5, 13.2, 12.0, 12.8, 14.3, 14.2]
  - the thorn channel's final weight norm: 0.739 (seeds: [0.685, 0.899, 0.503, 1.361, 0.522, 0.589, 0.857, 0.497])
