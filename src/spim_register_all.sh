#!/bin/env bash
#
#SBATCH -c 12                      # number of cores
#SBATCH -t 5
#SBATCH -o logs/smartspim_reg_%j.out        # STDOUT #add _%a to see each array job
#SBATCH -e logs/smartspim_reg_%j.err        # STDERR #add _%a to see each array job
#SBATCH --contiguous #used to try and get cpu mem to be contigous
#SBATCH --mem 80000

sbatch spim_register.sh 0 $1 $2 $3
sbatch spim_register.sh 1 $1 $2 $3
sbatch spim_register.sh 2 $1 $2 $3
sbatch spim_register.sh 3 $1 $2 $3

#1 is parent folder e.g. "/jukebox/LightSheetData/pbibawi/pb_udisco/pb_udisco-E155/imaging_request_1/rawdata/resolution_3.6x/"
#2 is reg folder e.g. "Ex_488_Em_0_corrected/"
#3 is cell folder e.g. "Ex_647_Em_2_corrected/"
#4 is scope e.g "smartspim" or "lavision"
