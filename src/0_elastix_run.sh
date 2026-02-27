source ./config_file.sh

MV_VOL=${1:-''}
FX_VOL=${2:-''}
OUTPUT_DIR=${3:-''}
ANN_VOL=${4:-''}

echo "path to environment: $ENV_PATH"
echo "mv: $MV_VOL"
echo "fx: $FX_VOL"
echo "using all four transforms"
echo "output dir (optional): $OUTPUT_DIR"
echo "annotation volume (optional): $ANN_VOL"

$ENV_PATH elastix_mv_to_fx.py "$MV_VOL" "$FX_VOL" "4" "$OUTPUT_DIR" "$ANN_VOL"


# remember, to get points in the allen atlas, you should be 
# aligning the allen (mv) TO your brain with cells (fx)
# because transformix for points is "backwards" 
# the elastix manual is very useful! https://www2.imm.dtu.dk/courses/02503/docs/elastix-5.2.0-manual.pdf