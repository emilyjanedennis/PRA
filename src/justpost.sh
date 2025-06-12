ARGOPT=${1:-''}
ARG1="/groups/dennis/dennislab/dennise/github/cleared_brains/data/annotation_template_25_resliced.tif"
ARG2="/groups/dennis/dennislab/dennise/github/cleared_brains/data/allen_anns-and-labels.csv"
ARG3="/groups/dennis/dennislab/dennise/github/cleared_brains/data/ann_mask.tif"
ARG4="/groups/dennis/dennislab/dennise/github/cleared_brains/data/axial_allenCCF_25.tif"
ARG5="/groups/dennis/dennislab/Imaging/raw_imaging_data/${ARGOPT}/processed/bigstitcher/${ARGOPT}_fused_12.tif"
ARG6="/groups/dennis/dennislab/Imaging/raw_imaging_data/${ARGOPT}/processed/bigstitcher"
ARG7="${ARG6}/output_axial_allenCCF_25_${ARGOPT}_fused_12"
ARG8="${ARG6}/outputs/filtered_cells_for-transformix.txt"
ARG9="${ARG6}/outputs"

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

bsub -J "prep-for-transformix_${ARGOPT}" -n 1 -o "logs/prepfortransformix_${ARGOPT}.txt" ./4_prep_for_transformix.sh $ARG6
bwait -w "ended(prep-for-transformix_${ARGOPT})"
echo "finished prepping, not running transformix"
bsub -J "transformix_${ARGOPT}" -o "logs/transformix_${ARGOPT}.txt" -n 2 ./5_transformix_cells.sh $ARG7 $ARG8 $ARG4
bwait -w "ended(transformix_${ARGOPT})"
echo "finished transformix, formatting final ouputs"
bsub -J "post_transformix_${ARGOPT}" -o "logs/posttransformix_${ARGOPT}.txt" -n 40 ./6_post_transformix.sh $ARG9 $ARG1 $ARG2 $ARG3
bwait -w "ended(post_transformix_${ARGOPT})"
echo "complete! probably"

