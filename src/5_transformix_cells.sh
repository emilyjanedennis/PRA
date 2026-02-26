#!/bin/bash
source ./config_file.sh
echo "path to environment: $ENV_PATH"

TRANSFORMS_FLD=${1:-''}
TXT_FILE=${2:-''}
MV_VOL=${3:-''}
OUTPUT_DIR=${4:-''}

echo "folder from elastix output containing TransformParameters files: $TRANSFORMS_FLD"
echo "txt file containing points in fixed volume space: $TXT_FILE"
echo "moving image: $MV_VOL"
echo "output directory (optional): $OUTPUT_DIR"

$ENV_PATH transformix_points.py "$TRANSFORMS_FLD" "$TXT_FILE" "$MV_VOL" "$OUTPUT_DIR"

