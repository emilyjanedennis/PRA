#!/bin/env bash
#
#SBATCH -c 11                      # number of cores
#SBATCH -t 240                  # time (minutes)
#SBATCH -o logs/id_inj_%j_%a.out        # STDOUT #add _%a to see each array job
#SBATCH -e logs/id_inj_%j_%a.err        # STDERR #add _%a to see each array job
#SBATCH --contiguous #used to try and get cpu mem to be contigous
#SBATCH --mem 120000 #120 gbs

module load anacondapy/2020.11
module load elastix/4.8
. activate lightsheet

xvfb-run python identify_injection_sites.py 1 $1 $2

# input 1: src which should have cell__ and reg__ volumes + an elastix folder
# input 2: dst can be any folder


    
    
