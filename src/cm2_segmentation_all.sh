#!/bin/env bash
#
#SBATCH -c 1                      # number of cores
#SBATCH -t 10

sbatch cm2_segmentation.sh $1 "/jukebox/brody/ejdennis/SIGMA_ann_in_mPRA_90um_edge_90um_vent_erosion.tif" "/scratch/ejdennis/sigma_202107.csv"

#inputs are
#1 - path to aligned .npy cells file
#2 - path to annotation tiff
#3 - path to annotation labels
#4 - save dir
#5 - brain name
#6- channel


