#!/bin/bash

source activate base
conda activate cm2

echo 'activated cm2'
echo 'input should be a full path to a processed/bigstitcher folder'
echo $1
python filtcells_to_locs.py $1

cd ../../BigStit*
# todo, make this a part of the repo

export JAVA_HOME=/misc/sc/jdks/8.0.275.fx-zulu

export PATH=$PATH:/groups/dennis/dennislab/dennise/github/apache-maven-3.9.9/bin

export PATH=$JAVA_HOME/bin:$PATH

for i in {0..9};
do (./transform-points --csvIn="${1}/outputs/s0${i}_filtered_cells.csv" --xml="${1}/dataset.xml" -vi="0,${i}" --csvOut="${1}/outputs/s0${i}_bigstitcher_out.txt" | tail -1);
done

for i in {10..30};
do (./transform-points --csvIn="${1}/outputs/s${i}_filtered_cells.csv" --xml="${1}/dataset.xml" -vi="0,${i}" --csvOut="${1}/outputs/s${i}_bigstitcher_out.txt" | tail -1);
done

./transform-points -p=0,0,0 --xml="${1}/dataset.xml" -vi="0,0" > "${1}/outputs/bounding_box.txt"

cd ../cleared_brains/src
python adjust_bigstitcher_by_bounding.py $1
