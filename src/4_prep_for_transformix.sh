#!/bin/bash
source ./config_file.sh
echo "path to environment: $ENV_PATH"

echo 'input below, it should be a full path to a processed/bigstitcher folder:'
echo $1
$ENV_PATH filtcells_to_locs.py $1
wait
sleep 5m
$ENV_PATH pre_transformix.py $1
wait
