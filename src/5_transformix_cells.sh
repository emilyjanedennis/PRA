#!/bin/bash
source ./config_file.sh
echo "path to environment: $ENV_PATH"

ARG1=${1:-''}
ARG2=${2:-''}
ARG3=${3:-''}
ARG4=${4:-''}

echo "folder from elastix output containing TransformParameters files: $ARG1"
echo "txt file containing points in fixed volume space: $ARG2"
echo "moving image: $ARG3"
echo "output directory (optional): $ARG4"

$ENV_PATH transformix_points.py "$ARG1" "$ARG2" "$ARG3" "$ARG4"

