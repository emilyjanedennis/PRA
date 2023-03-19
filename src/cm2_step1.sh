#!/bin/env bash
#
#SBATCH -c 12                      # number of cores
#SBATCH -t 240                  # time (minutes)
#SBATCH -o logs/clearmap2_%j_%a.out        # STDOUT #add _%a to see each array job
#SBATCH -e logs/clearmap2_%j_%a.err        # STDERR #add _%a to see each array job
#SBATCH --mem 120000 #120 gbs

cat /proc/$$/status | grep Cpus_allowed_list
module load anacondapy/2020.11
. activate cm2

echo "step 1 launching with inputs scope and file as follows:"
echo "$1"
echo "$2"

#make into blocks
#run cell detect on blocks
sleep $[ ( $RANDOM % 30 )  + 1 ]s
xvfb-run python cell_detect.py 1 $1 $2
