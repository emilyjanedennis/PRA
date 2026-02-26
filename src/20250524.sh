names=("2024-10-31_120153" "2024-10-31_124847" "2024-10-30_101304" "2024-10-30_130649" "2024-10-30_151222" "2024-10-30_155638" "2024-10-31_140929" "2024-10-31_151057" "2024-10-31_161023" "2024-10-31_165732" "2025-04-23_120857" "2025-04-23_111931" "2025-04-23_133149" "2025-04-23_141540" "2024-10-30_165104" "2024-10-31_092559" "2024-10-31_101956" "2024-10-31_110645" "2025-06-11_102241" "2025-06-11_105805" "2025-06-11_113824" "2025-06-11_122242" "2025-06-11_130428" "2025-06-11_134243" "2025-06-11_142104" "2025-07-28_114959" "2025-07-28_123702" "2025-07-28_095122" "2025-07-28_104614" "2025-08-11_083150" "2025-08-11_095231" "2025-07-29_092710" "2025-07-29_101224" "2025-07-29_110339" "2025-07-29_115032" "2025-07-29_124553" "2025-07-29_133309" "2025-08-08_171106" "2025-08-08_175709" "2025-08-08_110320" "2025-08-08_114940" "2025-08-13_133423" "2025-08-13_141929" "2025-08-08_124809" "2025-08-08_133543" "2025-07-28_133449" "2025-07-28_142157" "2025-08-07_171246" "2025-08-07_180051" "2024-11-18_123535")
ANNVOL="/groups/dennis/dennislab/dennise/github/cleared_brains/data/ann_in_caroli.tif"
ANNCSV="/groups/dennis/dennislab/dennise/github/cleared_brains/data/allen_anns-and-labels.csv"
ANNMASK="/groups/dennis/dennislab/dennise/github/cleared_brains/data/caroli_ann-mask.tif"

#for ARGOPT in ${names[@]}; do
#BRAIN="/groups/dennis/dennislab/Imaging/raw_imaging_data/${ARGOPT}/processed/bigstitcher/${ARGOPT}_fused_12.tif"
#OUTPUTFLD="/groups/dennis/dennislab/Imaging/raw_imaging_data/${ARGOPT}/processed/bigstitcher/caroli_outputs"
#TRANSFORMFLD="/groups/dennis/dennislab/Imaging/raw_imaging_data/${ARGOPT}/processed/bigstitcher/caroli_elastix"
#TXTFORTRANSFORMIX="/groups/dennis/dennislab/Imaging/raw_imaging_data/${ARGOPT}/processed/bigstitcher/outputs/filtered_cells_for-transformix.txt"
#echo $ARGOPT
#bsub -J "transformix_${ARGOPT}" -o "logs/transformix_${ARGOPT}.txt" -n 2 ./5_transformix_cells.sh $TRANSFORMFLD $TXTFORTRANSFORMIX $ANNVOL $OUTPUTFLD
#sleep 10s
#bwait -w "ended(transformix_${ARGOPT})"
#done

#echo "done with transformix"

for ARGOPT in ${names[@]}; do
echo ${ARGOPT}
OUTPUTFLD="/groups/dennis/dennislab/Imaging/raw_imaging_data/${ARGOPT}/processed/bigstitcher/caroli_outputs"
bsub -J "post_transformix_${ARGOPT}" -o "logs/posttransformix_${ARGOPT}.txt" -n 40 ./6_post_transformix.sh $OUTPUTFLD $ANNVOL $ANNCSV $ANNMASK
sleep 10s
bwait -w "ended(post_transformix_${ARGOPT})"
done
