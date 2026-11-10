#!/bin/sh
# Reproduce every Phase 0 result from a clean state. About a quarter of an hour on two cores.
set -e
cd "$(dirname "$0")/phase0"
rm -rf results
python3 run_phase0.py   | tee ../log_run_phase0.txt
python3 gate1_stress.py | tee ../log_gate1_stress.txt
python3 dynamics.py     | tee ../log_dynamics.txt
python3 extras.py       | tee ../log_extras.txt
python3 check_writeup.py | tee ../log_check_writeup.txt
