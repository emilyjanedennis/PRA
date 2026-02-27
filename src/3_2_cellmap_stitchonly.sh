#!/bin/bash
source ./config_file.sh
echo "path to environment: $ENV_PATH"

cd /groups/dennis/dennislab/dennise/github/ClearMap2/ClearMap/Scripts/
echo $PWD

echo 'using variables:'
echo $1
$ENV_PATH CellMap_parallel_juststitched.py $1
