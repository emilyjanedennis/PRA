#!/bin/bash
source ./config_file.sh
echo "path to environment: $ENV_PATH"

cd /groups/dennis/dennislab/dennise/github/ClearMap2/ClearMap/Scripts
echo 'in wd'
echo $1
echo $2

for i in {0..23}; do bsub -n 4 -J "maketiffs_${2}_${i}" -o "/groups/dennis/dennislab/dennise/github/cleared_brains/src/logs/job_${2}_${i}.txt" ${ENV_PATH} CellMap_parallel_tiffs.py $1 "fused.zarr" "${i}"; done

cd /groups/dennis/dennislab/dennise/github/cleared_brains/src
echo 'complete?'
