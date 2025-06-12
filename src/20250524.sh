names=("2025-04-22_105021" "2025-04-22_121123" "2025-04-22_125616" "2025-04-22_143339" "2025-04-22_151235" "2025-04-23_092538" "2025-04-23_101426" "2025-04-23_111931" "2025-04-23_120857" "2025-04-23_133149" "2025-04-23_141540" "2025-04-23_150815" "2025-04-23_164126" "2025-04-24_090927" "2025-04-24_095802" "2025-04-24_105152" "2025-04-24_113915" "2025-04-22_095551")
ARG1="/groups/dennis/dennislab/dennise/github/cleared_brains/data/annotation_template_25_resliced.tif"
ARG2="/groups/dennis/dennislab/dennise/github/cleared_brains/data/allen_anns-and-labels.csv"
ARG3="/groups/dennis/dennislab/dennise/github/cleared_brains/data/ann_mask.tif"
ARG4="/groups/dennis/dennislab/dennise/github/cleared_brains/data/axial_allenCCF_25.tif"
ARG5="/groups/dennis/dennislab/Imaging/raw_imaging_data/${1}/processed/bigstitcher/${1}_fused_12.tif"

for ARGOPT in ${names[@]}; do
ARG7="/groups/dennis/dennislab/Imaging/raw_imaging_data/${ARGOPT}/processed/bigstitcher/output_axial_allenCCF_25_${ARGOPT}_fused-12"
ARG8="/groups/dennis/dennislab/Imaging/raw_imaging_data/${ARGOPT}/processed/bigstitcher/outputs/filtered_cells_for-transformix.txt"
echo $ARGOPT
bsub -J "transformix_${ARGOPT}" -o "logs/transformix_${ARGOPT}.txt" -n 2 ./5_transformix_cells.sh $ARG7 $ARG8 $ARG4
sleep 10s
bwait -w "ended(transformix_${ARGOPT})"
done

echo "done with transformix"

for ARGOPT in ${names[@]}; do
echo ${ARGOPT}
bsub -J "post_transformix_${ARGOPT}" -o "logs/posttransformix_${ARGOPT}.txt" -n 40 ./6_post_transformix.sh "/groups/dennis/dennislab/Imaging/raw_imaging_data/${ARGOPT}/processed/bigstitcher/outputs" $ARG1 $ARG2 $ARG3
sleep 10s
bwait -w "ended(post_transformix_${ARGOPT})"
done
