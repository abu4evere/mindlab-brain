"""Exploratory (after data, not in the plan): how much do G's added neurons drive the hands by day 60?
Mean |outgoing weight to the hands| (M columns): the 16 born neurons against the 112 added ones; and for M128."""
import numpy as np, wn, ws
def final_net(brain, seed):
    home = ws.Home(seed); rec = True
    net = wn.Net(seed, 16 if brain == "G" else int(brain[1:]), rec)
    rng = np.random.default_rng([seed, 3, ws.BRAINS.index("Bm")])
    for d in range(1, ws.DAYS + 1):
        for k, look, rnd in home.day(d):
            prefix = []
            if d <= ws.DEMO_DAYS:
                prefix = ws.show_steps(look, home.pairs[k])
                ws.copy_step(net, look, home.pairs[k], prefix, wn.COPY_RATE)
            ws.try_box(net, look, home.pairs[k], prefix, rng, True)
        if brain == "G" and d in wn.GROW_AFTER:
            net.grow(wn.GROW_AFTER[d])
    return net
for s in (1, 2, 3, 4):
    g = final_net("G", s); m = final_net("M128", s)
    a = np.abs(g.p["M"]); b = np.abs(m.p["M"])
    print(s, "G born16 %.3f added112 %.3f | M128 first16 %.3f rest %.3f" % (a[:, :16].mean(), a[:, 16:].mean(), b[:, :16].mean(), b[:, 16:].mean()))
