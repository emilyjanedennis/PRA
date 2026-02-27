#!/bin/bash
source ./config_file.sh
echo "path to environment: $ENV_PATH"

# LIST_OF_BRAINS should be formatted as ("path/to/brain1.tif" "path/to/brain2.tif")
LIST_OF_BRAINS=${1:-''}
OUTPUT_DIR=${2:-''}
# OUTPUT_TIF must end in .tif, else result.tif will be made in the OUTPUT_DIR above
OUTPUT_TIF=${3:-''}

echo "listofbrains: $LIST_OF_BRAINS"
echo "output dir: $OUTPUT_DIR"
echo "output tif (if provided): $OUTPUT_TIF"

$ENV_PATH atlas_make_median.py "$LIST_OF_BRAINS" "$OUTPUT_DIR" "$OUTPUT_TIF"