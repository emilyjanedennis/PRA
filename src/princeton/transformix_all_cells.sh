#!/bin/bash

ARG1=${1:-''}
ARG2=${2:-''}
ARG3=${3:-''}

echo "folder from elastix output containing TransformParameters files: $ARG1"
echo "folder of txt files containing points in fixed volume space: $ARG2"
echo "moving image: $ARG3"


for i in {0..9}
do (bsub -n 4 -o "transformix_all_0${i}.txt" -J "transformix_${i}" ./transformix_cells.sh "${ARG1}" "${ARG2}/s0${i}_bigstitcher_out_for-transformix.txt" "${ARG3}");
done

for i in {10..30}
do (bsub -n 4 -o "transformix_all_${i}.txt" -J "transformix_${i}" ./transformix_cells.sh "${ARG1}" "${ARG2}/s${i}_bigstitcher_out_for-transformix.txt" "${ARG3}");
done

