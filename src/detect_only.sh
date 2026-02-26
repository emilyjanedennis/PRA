#!/bin/bash
source ./config_file.sh
echo "path to environment: $ENV_PATH"

cd $CM2_SCRIPTS_PATH

echo 'activated cm2'
echo 'using variables:'
echo $1
$ENV_PATH CellMap_parallel.py $1
