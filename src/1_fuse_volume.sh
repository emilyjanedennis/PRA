#!/bin/bash
source ./config_file.sh

cd $BIG_STITCHER_PATH

./create-fusion-container -x ${1}/dataset.xml -o ${1}/fused.zarr --preserveAnisotropy
./affine-fusion -o ${1}/fused.zarr

cd $CLEARED_BRAINS_FLD
cd src