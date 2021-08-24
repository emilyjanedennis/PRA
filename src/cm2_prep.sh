#!/bin/env bash
#
#SBATCH -c 12                      # number of cores
#SBATCH -t 4                  # time (minutes)
#SBATCH -o logs/clearmap2_%j_%a.out        # STDOUT #add _%a to see each array job
#SBATCH -e logs/clearmap2_%j_%a.err        # STDERR #add _%a to see each array job
#SBATCH --contiguous #used to try and get cpu mem to be contigous
#SBATCH --mem 120000 #120 gbs


cat /proc/$$/status | grep Cpus_allowed_list
module load anacondapy/2020.11
. activate cm2

echo "one is "
FOLDER="$1"
echo "$FOLDER"
echo "two is "
DEST="$2"
echo "$DEST"
echo "three is "

if [[ $3 = "lavision" ]]
then
    echo "lavision"
    SCOPE="lavision"
    echo "starting rename"
    OUT0=$(sbatch --array=0 cm2_rename.sh $FOLDER $DEST)
    echo $OUT0
    OUT1=$(sbatch --dependency=afterany:${OUT0##* } --array=0 cm2_step0.sh "$DEST" "$SCOPE")
else
    echo "smartspim"
    SCOPE="smartspim"
    echo "starting rename"
    OUT0=$(sbatch --array=0 cm2_rename.sh $FOLDER $DEST)
    OUT1=$(sbatch --dependency=afterany:${OUT0##* } --array=0 cm2_step0.sh "$DEST" "$SCOPE")
    echo $OUT1
    echo "ran step0"
fi
