names=("2025-07-29_101224" "2025-07-29_092710" "2025-07-28_142157" "2025-07-28_133449" "2025-07-28_123702" "2025-07-28_114959" "2025-07-28_104614" "2025-07-28_095122")

for ARGOPT in ${names[@]}; do
#./runbybasename.sh $ARGOPT
bsub -J "detectsingle_${ARGOPT}" -n 50  -o "logs/detectsingle_${ARGOPT}.txt" ./3_3_cellmap_detectsingle.sh "/groups/dennis/dennislab/Imaging/raw_imaging_data/${ARGOPT}/processed/bigstitcher"
bwait -w "ended(detectsingle_${ARGOPT})"
done

for ARGOPT in ${names[@]}; do
./runtransformix.sh $ARGOPT
done
