#!/bin/env bash
#SBATCH -n 1                      # number of cores
#SBATCH -t 120                 # time (minutes)
#SBATCH -o logs/flip_check_%j.out        # STDOUT
#SBATCH -e logs/flip_check_%j.err        # STDERR


module load anacondapy/2020.11
. activate lightsheet

python check_flipy.py $1
