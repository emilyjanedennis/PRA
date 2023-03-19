#!/bin/env bash
#
#SBATCH -c 12
#SBATCH -t 120                  # time (minutes)
#SBATCH -o logs/clearmap2_%j_%a.out        # STDOUT #add _%a to see each array job
#SBATCH -e logs/clearmap2_%j_%a.err        # STDERR #add _%a to see each array job
#SBATCH --mem 120000 #120 gbs

module load anacondapy/2020.11
. activate cm2

echo "rename slurm"
echo "$1"
echo "$2"
xvfb-run python spim_rename_for_cm2.py $1 $2
