#!/bin/bash

cd /groups/dennis/dennislab/dennise/github/ClearMap2/ClearMap/Scripts

conda init
wait
echo 'done wait 1'
conda activate cm2
wait


echo 'activated cm2'
echo 'using variables:'
echo $1
python CellMap_parallel.py $1
echo 'complete?'
