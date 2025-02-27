
ARG1=${1:-''}
ARG2=${2:-''}
ARG3=${3:-''}
ARG4=${4:-''}
ARG5=${5:-''}
ARGOPT=${6:-''}
ARG6="/groups/dennis/dennislab/Imaging/raw_imaging_data/${6:-''}/processed/bigstitcher"
ARG7="${ARG6}/output_axial_allenCCF_25_${6:-''}_fused_12"
ARG8="${ARG6}/outputs/filtered_cells_for_transformix.txt"
ARG9="${ARG6}/transformix_out"

echo "annotation volume: $ARG1"
echo "annotation labels: $ARG2"
echo "annotation mask volume: $ARG3"
echo "mv: $ARG4"
echo "fx: $ARG5"
echo "processed/bigstitcher folder: $ARG6"
echo "computed inputs:"

echo "elastix folder output: $ARG7"
echo "currently non existant file for transformix: $ARG8"
echo "transformix_out folder: $ARG9"

if [ -z "$ARGOPT" ]; then
   echo "no optional argument provided, running all steps"
elif ["$ARGOPT" == "0"]; then
   echo "running all steps"
   bsub -J "elastix" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/elastix.txt" -n 40 ./0_elastix_run.sh ${ARG4} ${ARG5}
   bsub -J "fuse" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/fused.txt" -n 40 -K ./1_fuse_volume.sh ${ARG6}
   bsub -J "make_tiffs" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/maketiffs.txt" -K -n 1 ./2_cellmap_tiffs_parallel.sh ${ARG6}
   bsub -J "babysit" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/babysit.txt" -n 1 -K ./3_cellmap_detect_and_filter_for_paralell.sh ${ARG6}                                                                                                                                 bsub -J "prep-for-transformix" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/prepfortransformix.txt" ./4_prep_for_trans       formix.sh $ARG6
   bsub -J "transformix" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/transformix.txt" -n 40 -K ./5_transformix_cells $ARG7 $ARG8 $ARG4
   bsub -J "post_transformix" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/posttransformix.txt" -K -n 40 ./6_post_transformix.sh $ARG9 $ARG1 $ARG2 $ARG3
elif ["$ARGOPT" == "1"]; then
   echo "running all steps except elastix"
bsub -J "fuse" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/fused.txt" -n 40 -K ./1_fuse_volume.sh ${ARG6}
bsub -J "make_tiffs" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/maketiffs.txt" -K -n 1 ./2_cellmap_tiffs_parallel.sh
 ${ARG6}
bsub -J "babysit" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/babysit.txt" -n 1 -K ./3_cellmap_detect_and_filter_for_
paralell.sh ${ARG6}
bsub -J "prep-for-transformix" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/prepfortransformix.txt" ./4_prep_for_trans
formix.sh $ARG6
bsub -J "transformix" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/transformix.txt" -n 40 -K ./5_transformix_cells
$ARG7 $ARG8 $ARG4
bsub -J "post_transformix" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/posttransformix.txt" -K -n 40 ./6_post_tran
sformix.sh $ARG9 $ARG1 $ARG2 $ARG3
elif ["$ARGOPT" == "2"]; then
echo "skipping making tiffs and elastix, running all other steps starting at cell detect"
bsub -J "make_tiffs" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/maketiffs.txt" -K -n 1 ./2_cellmap_tiffs_parallel.sh
 ${ARG6}
bsub -J "babysit" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/babysit.txt" -n 1 -K ./3_cellmap_detect_and_filter_for_
paralell.sh ${ARG6}
bsub -J "prep-for-transformix" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/prepfortransformix.txt" ./4_prep_for_trans
formix.sh $ARG6
bsub -J "transformix" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/transformix.txt" -n 40 -K ./5_transformix_cells
$ARG7 $ARG8 $ARG4
bsub -J "post_transformix" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/posttransformix.txt" -K -n 40 ./6_post_tran
sformix.sh $ARG9 $ARG1 $ARG2 $ARG3
fi

bsub -J "elastix" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/elastix.txt" -n 40 ./0_elastix_run.sh ${ARG4} ${ARG5}
bsub -J "fuse" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/fused.txt" -n 40 -K ./1_fuse_volume.sh ${ARG6}
bsub -J "make_tiffs" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/maketiffs.txt" -K -n 1 ./2_cellmap_tiffs_parallel.sh
 ${ARG6}
bsub -J "babysit" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/babysit.txt" -n 1 -K ./3_cellmap_detect_and_filter_for_
paralell.sh ${ARG6}
bsub -J "prep-for-transformix" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/prepfortransformix.txt" ./4_prep_for_trans
formix.sh $ARG6
bsub -J "transformix" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/transformix.txt" -n 40 -K ./5_transformix_cells 
$ARG7 $ARG8 $ARG4
bsub -J "post_transformix" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/posttransformix.txt" -K -n 40 ./6_post_tran
sformix.sh $ARG9 $ARG1 $ARG2 $ARG3

