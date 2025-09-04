#!/bin/bash

echo 'input below, it should be a full path to a processed/bigstitcher folder:'
echo $1
~/miniforge3/envs/cm2/bin/python filtcells_to_locs.py $1
wait
sleep 5m
~/miniforge3/envs/cm2/bin/python pre_transformix.py $1
wait
