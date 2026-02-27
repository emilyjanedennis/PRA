#!/bin/bash
source ./config_file.sh
echo "path to environment: $ENV_PATH"

sleep 5
$ENV_PATH checktiffs.py $1
wait
