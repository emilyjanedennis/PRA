#!/bin/bash

ARG1=${1:-''}
ARG2=${2:-''}
ARG3=${3:-''}
ARG4=${4:-''}

echo "mv: $ARG1"
echo "fx: $ARG2"
echo "output dir (optional): $ARG3"
echo "annotation volume (optional): $ARG4"

~/miniforge3/envs/cm2/bin/python elastix_fx_to_mv_ATLAS.py "$ARG1" "$ARG2" "$ARG3" "$ARG4"
