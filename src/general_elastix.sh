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

echo $1
echo $2
echo $3
echo $4
echo $5
echo $6
xvfb-run python general_elastix.py $1 $2 $3 $4 $5 $6


# example: sbatch general_elastix.sh "/jukebox/brody/lightsheet/elastix_params/" "['/jukebox/brody/lightsheet/volumes/WHS_masked_atlas
.tif']" "/jukebox/brody/lightsheet/atlasdir/mPRA.tif" "/scratch/ejdennis/lightsheet" "1.4" ""
# this will align WHS_mastked_atlas.tif to mPRA.tif using the parameters in elastix_params
# it will save results in /scratch/ejdennis/lightsheet and use a 1.4x multiplier (making the moving volume 140% the size of the fixed volume)
