#!/bin/env bash
#
#SBATCH -c 11                      # number of cores
#SBATCH -t 240                  # time (minutes)
#SBATCH -o logs/transformix_%j_%a.out        # STDOUT #add _%a to see each array job
#SBATCH -e logs/transformix_%j_%a.err        # STDERR #add _%a to see each array job
#SBATCH --contiguous #used to try and get cpu mem to be contigous
#SBATCH --mem 120000 #120 gbs

module load anacondapy/2020.11
module load elastix/4.8
. activate lightsheet

echo $1
echo $2
echo $3
echo $4
echo $5
xvfb-run python general_transformix.py $1 $2 $3 $4 $5


# example: sbatch general_transformix.sh "/jukebox/brody/lightsheet/volumes/WHS_masked_atlas_to_fPRA" "/jukebox/brody/lightsheet/volumes/fPRA.tif" "/jukebox/brody/lightsheet/volumes/WHS_masked_annotations.tif" "/scratch/ejdennis/lightsheet/WHS_v4_anns_to_fPRA"
# this will use the Transform files in .../WHS_masked_atlas_to_fPRA (where WHS_masked_atlas.tif was aligned with general_elastix.sh to fPRA.tif)
# to transform WHS_masked_annotations.tif into fPRA space
