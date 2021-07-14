#!/bin/env bash
#
#SBATCH -c 1                      # number of cores
#SBATCH -t 5                  # time (minutes)
#SBATCH -o logs/id_inj_%j.out        # STDOUT #add _%a to see each array job
#SBATCH -e logs/id_inj_%j.err        # STDERR #add _%a to see each array job
#SBATCH --contiguous #used to try and get cpu mem to be contigous


OUT0=$(sbatch --array=0 id_inj_make_volume.sh "$1" "$2")
OUT1=$(sbatch --dependency=afterok:${OUT0##* } --array=0 id_inj_align.sh "$1" "$2")

# input 1: src which should have cell__ and reg__ volumes + an elastix folder
# input 2: dst can be any folder

    
    
