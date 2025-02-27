#!/bin/bash


cd ../../BigStit*
# todo, make this a part of the repo

export JAVA_HOME=/misc/sc/jdks/8.0.275.fx-zulu

export PATH=$PATH:/groups/dennis/dennislab/dennise/github/apache-maven-3.9.9/bin

export PATH=$JAVA_HOME/bin:$PATH

./create-fusion-container -x ${1}/dataset.xml -o ${1}/fused.zarr --preserveAnisotropy
./affine-fusion -o ${1}/fused.zarr

cd ../cleared_brains/src
