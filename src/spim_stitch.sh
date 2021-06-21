#!/bin/env bash
#
#SBATCH -p all                # partition (queue)
#SBATCH -c 1                      # number of cores
#SBATCH -t 10                # time (minutes)
#SBATCH -o logs/smartspim_stitch_%j.out        # STDOUT #add _%a to see each array job
#SBATCH -e logs/smartspim_stitch_%j.err        # STDERR #add _%a to see each array job

echo "In the directory: `pwd` "
echo "As the user: `whoami` "
echo "on host: `hostname` "

#specifications
cat /proc/$$/status | grep Cpus_allowed_list
cat /proc/meminfo

module load anacondapy/2020.11
. activate lightsheet

echo "Experiment name / TeraStitcher folder hierarchy:" "$1"
echo "Storage directory:" "$2"

#import
OUT0=$(sbatch spim_smartspim_import.sh "$1")
echo $OUT0

#displacement computation
OUT1=$(sbatch --dependency=afterok:${OUT0##* } spim_smartspim_compute.sh "$1")
echo $OUT1

#thresholding
OUT2=$(sbatch --dependency=afterok:${OUT1##* } spim_smartspim_proj.sh "$1")
echo $OUT2

#merge
OUT3=$(sbatch --dependency=afterok:${OUT2##* } spim_smartspim_merge.sh "$1" "$2")
echo $OUT3

#functionality
#go to smartspim_pipeline folder and type sbatch spim_stitch.sh [path to terstitcher folder hierarchy] [destination of stitched directory]
