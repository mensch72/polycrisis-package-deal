#!/bin/sh
# Reproduce every Phase 0 result from a clean state. About 20 minutes on two cores.
set -e
cd "$(dirname "$0")/phase0"
rm -rf results results2
python3 run_phase0.py   | tee ../log_run_phase0.txt
python3 gate1_stress.py | tee ../log_gate1_stress.txt
python3 dynamics.py     | tee ../log_dynamics.txt
python3 extras.py       | tee ../log_extras.txt
python3 check_writeup.py | tee ../log_check_writeup.txt
# second instance and contested variant (session 2)
python3 run_instance2.py  | tee ../log_run_instance2.txt
python3 run_contested.py  | tee ../log_run_contested.txt
python3 check_writeup2.py | tee ../log_check_writeup2.txt
# towers in a pre-CPEP (session 2)
python3 run_tower.py instance2    | tee ../log_run_tower_instance2.txt
python3 run_tower.py contested    | tee ../log_run_tower_contested.txt
python3 run_tower_relaxed.py      | tee ../log_run_tower_relaxed.txt
python3 check_towers.py           | tee ../log_check_towers.txt
