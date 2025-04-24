#!/bin/bash

cd /groups/dennis/dennislab/dennise/github/ClearMap2/ClearMap/Scripts/
echo $PWD

echo 'using variables:'
echo $1
~/miniforge3/envs/cm2/bin/python CellMap_parallel_juststitched.py $1
