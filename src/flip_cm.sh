#!/bin/env bash
#SBATCH -n 1                      # number of cores
#SBATCH -t 120                 # time (minutes)
#SBATCH -o logs/flip_%j.out        # STDOUT
#SBATCH -e logs/flip_%j.err        # STDERR


module load anacondapy/2020.11
. activate lightsheet

python flip_cm.py $1
