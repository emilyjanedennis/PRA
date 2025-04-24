#!/bin/bash

ARG1=${1:-''}
ARG2=${2:-''}
ARG3=${3:-''}
ARG4=${4:-''}

echo "folder from elastix output containing TransformParameters files: $ARG1"
echo "txt file containing points in fixed volume space: $ARG2"
echo "moving image: $ARG3"
echo "output directory (optional): $ARG4"

~/miniforge3/envs/cm2/bin/python transformix_points.py "$ARG1" "$ARG2" "$ARG3" "$ARG4"

