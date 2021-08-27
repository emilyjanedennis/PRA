#!/bin/env bash
#

#SBATCH -c 1                      # number of cores
#SBATCH -t 20                  # time (minutes)
#SBATCH -o logs/clearmap2_%j.out        # STDOUT #add _%a to see each array job
#SBATCH -e logs/clearmap2_%j.err        # STDERR #add _%a to see each array job

cat /proc/$$/status | grep Cpus_allowed_list
module load anacondapy/2020.11
. activate cm2

# change these:
declare -a LIST_OF_FOLDERS=("/jukebox/LightSheetData/rat-brody/processed/201910_tracing/z268/full_sizedatafld/pbibawi_z268_ctbtracing_4x_488_647_017na_1hfds_z10um_150msec_20povlp_ch01"
			"/jukebox/LightSheetData/rat-brody/processed/201910_tracing/z269/full_sizedatafld/pbibawi_z269_ctbtracing_4x_555_647_017na_1hfds_z10um_150msec_20povlp_ch00")

echo "$LIST_OF_FOLDERS"

declare -a LIST_OF_BRAINNAMES=("z268"
				"z269")

echo "$LIST_OF_BRAINNAMES"
declare -a LIST_OF_CELL_REG=("cell"
			"reg")

echo "$LIST_OF_CELL_REG"

declare -a LIST_OF_ELASTIX_FOLDERS=("/scratch/ejdennis/lavision_brains/z268/elastix"
				"/scratch/ejdennis/lavision_brains/z269/elastix")

echo "$LIST_OF_ELASTIX_FOLDERS"

declare -a FLIP_Y=("0"
	"0")

for (( n=0; n<=${#LIST_OF_FOLDERS[@]}; n++ ))
do

    echo "$n"
    echo "${LIST_OF_FOLDERS[n]}"
    echo "${LIST_OF_ELASTIX_FOLDERS[n]}"
    echo "${LIST_OF_CELL_REG[n]}"

    scope="lavision"
    
    if [ "${LIST_OF_CELL_REG[n]}" = "cell" ];
        then
            CELL_VALUE="642"
            NUM_TRANSFORMS="2"
        else
            CELL_VALUE="488"
            NUM_TRANSFORMS="1"
    fi

    echo "$CELL_VALUE"
    echo "$NUM_TRANSFORMS"    
    DESTINATION="/scratch/ejdennis/lavision_brains/${LIST_OF_BRAINNAMES[n]}/${CELL_VALUE}"
    echo "$DESTINATION"
    FILT_NUMPY="${DESTINATION}/${LIST_OF_BRAINNAMES[n]}_${CELL_VALUE}_filt.npy"
    ALIGNED_NUMPY="${DESTINATION}/aligned_3_20_400/${LIST_OF_BRAINNAMES[n]}_${LIST_OF_CELL_REG[n]}_in_atl_transform_zyx_voxels.npy"
    echo "$ALIGNED_NUMPY"
    SCOPE="lavision"

    OUTRENAME=$(sbatch --array=0 -p Brody cm2_rename.sh "${LIST_OF_FOLDERS[n]}" "$DESTINATION")
    echo "$OUTRENAME"
    OUT0=$(sbatch --dependency=afterany:${OUTRENAME##* } --array=0 -p Brody cm2_step0.sh "$DESTINATION" "$SCOPE")
    echo "$OUT0"
    OUT1=$(sbatch --dependency=afterany:${OUT0##* } --array=0-300 -p Brody cm2_step1.sh "$DESTINATION" "$SCOPE")
    echo "$OUT1"
    OUT2=$(sbatch --dependency=afterany:${OUT1##* } --array=0 -p Brody cm2_step3.sh "$DESTINATION" "$SCOPE")
    echo "$OUT2"
    echo "${LIST_OF_BRAINNAMES[n]}"
    #OUT3=$(sbatch --dependency=afterany:${OUT2##* } -p Brody cm2_filter.sh "/scratch/ejdennis/cm2_brains" "${LIST_OF_BRAINNAMES[n]}" "3" "20" "400" "${LIST_OF_CELL_REG[n]}")
    OUT3=$(sbatch --dependency=afterany:${OUT2##* } -p Brody cm2_filter.sh "/scratch/ejdennis/lavision_brains" "${LIST_OF_BRAINNAMES[n]}" "3" "30" "120" "${LIST_OF_CELL_REG[n]}")
    echo "$OUT3"
    OUT4=$(sbatch --dependency=afterany:${OUT3##* } -p Brody cm2_align.sh "$NUM_TRANSFORMS" "$FILT_NUMPY" "${LIST_OF_ELASTIX_FOLDERS[n]}" "${DESTINATION}/aligned" "${LIST_OF_BRAINNAMES[n]}" "${FLIP_Y[n]}" "1" "lavision")
    echo "$OUT4"
    OUT5=$(sbatch --dependency=afterany:${OUT4##* } -p Brody cm2_segmentation.sh "$ALIGNED_NUMPY" "/jukebox/brody/ejdennis/SIGMA_ann_in_mPRA_90um_edge_90um_vent_erosion.tif" "/jukebox/brody/lightsheet/labels/SIGMA_in_PRA.csv" "${DESTINATION}/segmented" "${LIST_OF_BRAINNAMES[n]}" "$CELL_VALUE")
    echo "$OUT5"

done
