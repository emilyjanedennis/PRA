#!/bin/bash

ARG1=${1:-''}
ARG2=${2:-''}
ARG3=${3:-''}
#ARG4=${4:-''}

echo "listofbrains: $ARG1"
echo "output dir: $ARG2"
echo "output tif (optional): $ARG3"

~/miniforge3/envs/cm2/bin/python atlas_make_median.py "$ARG1" "$ARG2" "$ARG3"

