#!/bin/env bash
#
#SBATCH -c 1                      # number of cores
#SBATCH -t 240                  # time (minutes)
#SBATCH -o logs/inj_accum_%j.out        # STDOUT #add _%a to see each array job
#SBATCH -e logs/inj_accum_%j.err        # STDERR #add _%a to see each array job
#SBATCH --contiguous #used to try and get cpu mem to be contigous
#SBATCH --mem 120000 #120 gbs

module load anacondapy/2020.11
. activate lightsheet

xvfb-run python inj_accum.py $1 $2

# input 1: src which should have many subfolders of individual brains
# input 2: dst can be any folder



