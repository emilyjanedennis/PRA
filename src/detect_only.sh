#!/bin/bash
source ./config_file.sh
echo "path to environment: $ENV_PATH"

cd /groups/dennis/dennislab/dennise/github/ClearMap2/ClearMap/Scripts

echo 'activated cm2'
echo 'using variables:'
echo $1
$ENV_PATH CellMap_parallel.py $1
echo 'complete?'
