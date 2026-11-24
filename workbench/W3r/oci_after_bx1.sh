#!/bin/bash
# Oracle: W3r starts after BX1's after-school test has started (it takes 13 of the 16 threads first), checks first.
until [ -f ~/bx1/after.log ]; do sleep 300; done
cd ~/mindlab/workbench/W3r && ./start_after_checks.sh oci 16 jobs_oci.txt
