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
module load terastitcher
which terastitcher


echo "Experiment name / TeraStitcher folder hierarchy:" "$1"
echo "Storage directory:" "$2"

#!/bin/env bash

# Run this file like: 
# spim_stitching_pipeline.sh /path/to/terastitcher_folder_hierarchy /path/to/stitched

echo "Experiment name / TeraStitcher folder hierarchy:" "$1"
echo "Storage directory:" "$2"

# # # import
OUT0=$(sbatch --parsable --export=ALL,input_dir=$1,output_dir=$2 spim_stitch_import.sh)
echo $OUT0

# #displacement computation
OUT1=$(sbatch --parsable --dependency=afterok:${OUT0##* } --export=ALL,input_dir=$1,output_dir=$2 spim_stitch_compute.sh)
echo $OUT1

# # #thresholding
OUT2=$(sbatch --parsable --dependency=afterok:${OUT1##* } --export=ALL,input_dir=$1,output_dir=$2 spim_stitch_proj.sh)
echo $OUT2

#merge
OUT3=$(sbatch --parsable --dependency=afterok:${OUT2##* } --export=ALL,input_dir=$1,output_dir=$2 spim_stitch_merge.sh)
echo $OUT3
