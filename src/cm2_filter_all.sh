#!/bin/env bash
#
#SBATCH -c 1                      # number of cores
#SBATCH -t 360                # time (minutes)
#SBATCH -o logs/cm2_filter_%j.out        # STDOUT
#SBATCH -e logs/cm2_filter_%j.err        # STDERR

cat /proc/$$/status | grep Cpus_allowed_list
module load anacondapy/2020.11
. activate cm2

# change these:
declare -a LIST_OF_BRAINS=("A296" "A300" "E130" "E131" "E154" "M122" "m128" "X073" "X078")
declare -a FOLDER = "/scratch/ejdennis/cm2_brains"

# sends out jobs
for (( n=0; n<=${#LIST_OF_BRAINS[@]}; n++ ))
do
    echo "$n"
    echo "${LIST_OF_BRAINS[n]}"
    sbatch cm2_filter.sh "$1" "${LIST_OF_BRAINS[n]}" "3" "30" "120" "reg"
    sbatch cm2_filter.sh "$1" "${LIST_OF_BRAINS[n]}" "3" "30" "120" "cell"
done

# 1 - directory where brain(s) live
# 2 - brainname
# 3 - source value (suggest 3 if at princeton using smartspim)
# 4 - size 1 value (suggest 30 if at princeton using smartspim)
# 5 - size 2 value (suggest 120 if at princeton using smartspim)
# 6 - channel "cell" or "reg"
