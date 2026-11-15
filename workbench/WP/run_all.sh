python wp.py run stable > run.out 2>&1 && python wp.py run change >> run.out 2>&1 && python analyse_wp.py > analyse.out 2>&1; echo finished >> run.out
