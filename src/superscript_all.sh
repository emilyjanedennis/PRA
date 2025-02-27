
ARG1=${1:-''}
ARG2=${2:-''}
ARG3=${3:-''}
ARG4=${4:-''}
ARG5=${5:-''}
ARGOPT=${6:-''}
ARG6="/groups/dennis/dennislab/Imaging/raw_imaging_data/${6:-''}/processed/bigstitcher"
ARG7="${ARG6}/output_axial_allenCCF_25_${6:-''}_fused_12"
ARG8="${ARG6}/outputs/filtered_cells_for-transformix.txt"
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

conda activate cm2
wait

#bsub -J "elastix" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/elastix.txt" -n 40 ./0_elastix_run.sh ${ARG4} ${ARG5}
#bsub -J "fuse" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/fused.txt" -n 40 ./1_fuse_volume.sh ${ARG6}

#bsub -n 1 -o 'logs/launchtiffjobs.txt' ./2_cellmap_tiffs_parallel.sh ${ARG6}
#echo "entering waiting loop"
#for i in {0..23}; do
#   echo "waiting for ${i}"
#   bwait -w "ended(maketiffs${i})"
#done

cd /groups/dennis/dennislab/dennise/github/cleared_brains/src


#echo "finished maketiffs, starting detect and filter (GPUs)"

#bsub -J "babysit_${ARGOPT}" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/babysit_${ARGOPT}.txt" -n 1 ./3_1_checktiffs.sh ${ARG6} ${ARGOPT}
#bwait -w "ended(babysit_${ARGOPT})"
#bsub -J "stitchonly_${ARGOPT}" -n 36 -q gpu_a100 -gpu "num=3" -o "logs/stitchonlymonitor_${ARGOPT}.txt" ./3_2_cellmap_stitchonly.sh $ARG6
#bwait -w "ended(stitchonly_${ARGOPT})"
bsub -J "detectsingle_${ARGOPT}" -n 50  -o "logs/detectsingle_${ARGOPT}.txt" ./3_3_cellmap_detectsingle.sh $ARG6
bwait -w "ended(detectsingle_${ARGOPT})"
echo "finished detect, prepping for transformix: "
bsub -J "prep-for-transformix_${ARGOPT}" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/prepfortransformix_${ARGOPT}.txt" ./4_prep_for_transformix.sh $ARG6
bwait -w "ended(prep-for-transformix_${ARGOPT})"
echo "finished prepping, not running transformix"
bsub -J "transformix_${ARGOPT}" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/transformix_${ARGOPT}.txt" -n 40 ./5_transformix_cells.sh $ARG7 $ARG8 $ARG4
bwait -w "ended(transformix_${ARGOPT})"
echo "finished transformix, formatting final ouputs"
bsub -J "post_transformix_${ARGOPT}" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/posttransformix_${ARGOPT}.txt" -n 40 ./6_post_transformix.sh $ARG9 $ARG1 $ARG2 $ARG3
bwait -w "ended(post_transformix_${ARGOPT})"
echo "complete!"


