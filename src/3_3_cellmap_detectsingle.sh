#!/bin/bash

cd /groups/dennis/dennislab/dennise/github/ClearMap2/ClearMap/Scripts

echo 'activated cm2'
echo 'using variables:'
echo $1
~/miniforge3/envs/cm2/bin/python CellMap_parallel_nostitched.py $1
echo 'complete?'
