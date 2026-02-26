#!/bin/bash
source ./config_file.sh
echo "path to environment: $ENV_PATH"

TRANSFORMIX_OUT_FLD=${1:-''}
ANN_VOL=${2:-''}
ANN_CSV=${3:-''}
ANN_MASK=${4:-''}

echo "folder from transformix output, containing points_transformixed.csv files: $TRANSFORMIX_OUT_FLD"
echo "full path to annotation volume: $ANN_VOL"
echo "full path to an annotation labels file: $ANN_CSV"
echo "full path to an annotation mask: $ANN_MASK"

$ENV_PATH post_transformix.py "$TRANSFORMIX_OUT_FLD" "$ANN_VOL" "$ANN_CSV" "$ANN_MASK"


