#!/bin/env bash
#
#SBATCH -c 1                      # number of cores
#SBATCH -t 360                # time (minutes)
#SBATCH -o logs/cm2_filter_%j.out        # STDOUT
#SBATCH -e logs/cm2_filter_%j.err        # STDERR
#SBATCH --mem 180000

cat /proc/$$/status | grep Cpus_allowed_list
module load anacondapy/2020.11
. activate cm2

xvfb-run python cm2_filter.py $1 $2 $3 $4 $5 $6
