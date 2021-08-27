#!/bin/env bash
#
#SBATCH -c 11                      # number of cores
#SBATCH -t 300
#SBATCH -o logs/transformix.out        # STDOUT #add _%a to see each array job
#SBATCH -e logs/transformix_%j.err        # STDERR #add _%a to see each array job
#SBATCH --contiguous #used to try and get cpu mem to be contigous
#SBATCH --mem 180000

echo "In the directory: `pwd` "

module load anacondapy/2020.11
module load elastix/4.8
. activate lightsheet

xvfb-run python general_transformix_imgs.py $1 $2 $3 $4 $5 $6

#inputs are:
#1 - full path to moving image (tiff)
#2 - full path to fixed image (tiff)
#3 - full path to the transform folder
#4 - full path to the destination folder

#optional inputs and their defaults are
#5 - 0+ zoom amount (default 1.4x)
#6 - 1 or 0: if jacobian determinate volumes and geometric displacement volumes should be made (default to 0, no)
