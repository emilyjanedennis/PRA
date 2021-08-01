#!/bin/env bash
#
#SBATCH -c 1                      # number of cores
#SBATCH -t 4                  # time (minutes)
#SBATCH -o logs/clearmap2_%j_%a.out        # STDOUT #add _%a to see each array job
#SBATCH -e logs/clearmap2_%j_%a.err        # STDERR #add _%a to see each array job

cat /proc/$$/status | grep Cpus_allowed_list
module load anacondapy/2020.11
. activate cm2

if [[ $4 = "lavision" ]]
then
    echo "lavision"
    SCOPE="lavision"
else
    echo "smartspim"
    SCOPE="smartspim"
fi

if [ "$#" -eq  "5" ]
then
    echo "yflip is ${5}"
    YFLIP="$5"
else
    echo "yflip is default ON"
    YFLIP="1"
if [ "$#" -eq "6" ]
then
    echo "x and z switch is ${6}"
    XZSWITCH="$6"
else
    echo "x and z switch is default ON"
    XZSWITCH="1"

if [ "$#" -eq  "7" ]
then
    echo "ann tiff is ${7}"
    ANNTIFF="$7"
else
    echo "ann tiff set to default 
    ANNTIF="/jukebox/brody/ejdennis/SIGMA_ann_in_mPRA_90um_edge_90um_vent_erosion.tif"

if [ "$#" -eq "8" ]
then
    echo "ann label file is ${8}
else
    echo "ANNLAB is set to default /scratch/ejdennis/sigma_202107.csv"
    ANNLAB="/scratch/ejdennis/sigma_202107.csv"

# ~~~~~ FILTER ~~~~~
OUT1=$(sbatch cm2_filter.sh $1 $2 "3" "6" "200" "cell")
OUT2=$(sbatch cm2_filter.sh $1 $2 "3" "6" "200" "reg")
echo $OUT1
echo $OUT2

#inputs to cm2_filter.sh
# 1st - folder of brain/s
# 2nd - brainname
# 3rd, 4th, and 5th - cm2 filter parameters - source (3), min/max (6/200)
# 6th - cell or reg to indicate if 642 or 488 channel


# ~~~~~ALIGN~~~~~
# first set variables based on inputs
SAVEDIR = "${1}/${2}"
CELLNPY="${1}/${2}/642/${2}_642_filt.npy"
REGNPY="${1}/${2}/488/${2}_488_filt.npy"
echo "npys are"
echo $CELLNPY
echo $REGNPY

OUT3=$(sbatch --dependency=afterany:${OUT1##* } cm2_align.py 2 $CELLNPY $3 $SAVEDIR $2 $YFLIP $XZSWITCH)
OUT4=$(sbatch --dependency=afterany:${OUT2##* } cm2_align.py 1 $REGNPY $3 $SAVEDIR $2 $YFLIP $XZSWITCH)
echo $OUT3
echo $OUT4 

# inputs to cm2_align.py explained
# 1st- number of transoforms to do: if cell ch, 2 if reg ch, 1
# 2nd- string of npy filepath
# 3rd- elastix folder path
# 4th- string where you want to save to
# 5th- brainname e.g. "e154", default "brainname"
# 6th- flip y? 1 yes 0 no, default 0
# 7th- switch x and z? 1 yes 0 no, default yes (axial -> sagittal)



# ~~~~~SEGMENT~~~~~
# first make variables based on inputs
ALIGNEDCELLS=""
ALIGNEDREG=""

OUT5=$(sbatch --dependency=afterany:$OUT3##* } cm2_segmentation.sh $ALIGNEDCELLS $ANNTIFF $ANNLAB $SAVEDIR $2 "642")
OUT6=$(sbatch --dependency=afterany:$OUT4##* } cm2_segmentation.sh $ALIGNEDREG $ANNTIFF $ANNLAB $SAVEDIR $2 "488")



#inputs are
#1 - path to aligned .npy cells file
#2 - path to annotation tiff
#3 - path to annotation labels
#4 - save dir
#5 - brain name
#6- channel

