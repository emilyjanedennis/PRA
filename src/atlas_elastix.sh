#!/bin/bash
source ./config_file.sh
echo "path to environment: $ENV_PATH"

MV_VOL=${1:-''}
FX_VOL=${2:-''}
OUTPUT_DIR=${3:-''}

echo "mv: $MV_VOL"
echo "fx: $FX_VOL"
echo "using three transforms: one affine and two bsplines"
echo "output dir (optional): $OUTPUT_DIR"

$ENV_PATH elastix_mv_to_fx.py "$MV_VOL" "$FX_VOL" "3" "$OUTPUT_DIR"
