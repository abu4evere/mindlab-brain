python wc.py evolve 1 2 > evo.out 2>&1 && python wc.py final > final.out 2>&1 && python analyse_wc.py > analyse.out 2>&1; echo finished >> final.out
