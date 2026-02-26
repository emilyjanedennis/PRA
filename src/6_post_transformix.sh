#!/bin/bash
source ./config_file.sh
echo "path to environment: $ENV_PATH"

ARG1=${1:-''}
ARG2=${2:-''}
ARG3=${3:-''}
ARG4=${4:-''}

echo "folder from transformix output, containing points_transformixed.csv files: $ARG1"
echo "full path to annotation volume: $ARG2"
echo "full path to an annotation labels file: $ARG3"
echo "full path to an annotation mask: $ARG4"

$ENV_PATH post_transformix.py "$ARG1" "$ARG2" "$ARG3" "$ARG4"


