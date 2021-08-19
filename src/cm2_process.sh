#!/bin/env bash
#
#SBATCH -c 1                      # number of cores
#SBATCH -t 4                  # time (minutes)
#SBATCH -o logs/clearmap2_%j_%a.out        # STDOUT #add _%a to see each array job
#SBATCH -e logs/clearmap2_%j_%a.err        # STDERR #add _%a to see each array job

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
else
    echo "smartspim"
    SCOPE="smartspim"
fi


echo "dest and scope ins"
echo "$DEST"
echo "$SCOPE"

# add step 1
OUT2=$(sbatch --array=0-300 cm2_step1.sh "$DEST" "$SCOPE")
echo $OUT2

# add step 3
OUT3=$(sbatch --dependency=afterany:${OUT2##* } --array=0 cm2_step3.sh $DEST $SCOPE)
echo $OUT3
