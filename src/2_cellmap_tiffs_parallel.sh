#!/bin/bash
source ./config_file.sh
echo "path to environment: $ENV_PATH"
echo "path to clearmap2's scripts folder: $CM2_SCRIPTS_PATH"
echo "path to cleared_brains folder: $CLEARED_BRAINS_FLD"

cd $CM2_SCRIPTS_PATH
echo 'in wd'
echo $1
echo $2

for i in {0..23}; do bsub -n 4 -J "maketiffs_${2}_${i}" -o "${CLEARED_BRAINS_FLD}/src/logs/job_${2}_${i}.txt" ${ENV_PATH} CellMap_parallel_tiffs.py $1 "fused.zarr" "${i}"; done

cd $CLEARED_BRAINS_FLD
cd src