source ./config_file.sh

ARG1=${1:-''}
ARG2=${2:-''}
ARG3=${3:-''}
ARG4=${4:-''}

echo "path to environment: $ENV_PATH"
echo "mv: $ARG1"
echo "fx: $ARG2"
echo "output dir (optional): $ARG3"
echo "annotation volume (optional): $ARG4"

$ENV_PATH elastix_mv_to_fx.py "$ARG1" "$ARG2" "$ARG3" "$ARG4"
