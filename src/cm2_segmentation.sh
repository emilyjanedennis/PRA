#!/bin/env bash
#
#SBATCH -c 1                      # number of cores
#SBATCH -t 300
#SBATCH -o logs/cm2_seg_%j.out        # STDOUT #add _%a to see each array job
#SBATCH -e logs/cm2_seg_%j.err        # STDERR #add _%a to see each array job
#SBATCH --mem 20000

echo "In the directory: `pwd` "

module load anacondapy/2020.11
. activate lightsheet


python cm2_segmentation.py $1 $2 $3 $4 $5 $6

#inputs are
#1 - path to aligned .npy cells file
#2 - path to annotation tiff
#3 - path to annotation labels
#4 - save dir
#5 - brain name
#6- channel
