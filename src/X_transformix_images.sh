#!/bin/bash
source ./config_file.sh
echo "path to environment: $ENV_PATH"

TRANSFORMS_FLD=${1:-''}
MV_VOL=${2:-''}
OUTPUT_FILE=${3:-''}

echo "folder from elastix output containing TransformParameters files: $TRANSFORMS_FLD"
echo "the tif you'd like to transform, this **must** have the same dimensions 
as the moving image used in the elastix call that generated the transforms folder above: $MV_VOL"
echo "a full path to where you'd like the image saved, ending in .tif: $OUTPUT_FILE"

$ENV_PATH transformix_image.py "$TRANSFORMS_FLD" "$MV_VOL" "$OUTPUT_FILE"