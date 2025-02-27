#!/bin/bash

conda activate cm2

echo 'activated cm2'
echo 'input should be a full path to a processed/bigstitcher folder:'
echo $1
python filtcells_to_locs.py $1
wait
python pre_transformix.py $1
wait
