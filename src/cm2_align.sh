#!/bin/env bash
#
#SBATCH -c 11                      # number of cores
#SBATCH -t 300
#SBATCH -o logs/cm2_align_reg_%j.out        # STDOUT #add _%a to see each array job
#SBATCH -e logs/cm2_align_%j.err        # STDERR #add _%a to see each array job
#SBATCH --contiguous #used to try and get cpu mem to be contigous
#SBATCH --mem 80000

echo "In the directory: `pwd` "

module load anacondapy/2020.11
module load elastix/4.8
. activate lightsheet

python cm2_align.py $1 $2 $3 $4 $5 $6 $7

# functionality
# in the PRA/src folder 
# 1- number of transoforms to do: if cell ch, 2 if reg ch, 1
# 2- string of npy filepath
# 3- elastix folder path
# 4- string where you want to save to
# 5- brainname e.g. "e154", default "brainname"
# 6- flip y? 1 yes 0 no, default 0
# 7- switch x and z? 1 yes 0 no, default yes (axial -> sagittal)
