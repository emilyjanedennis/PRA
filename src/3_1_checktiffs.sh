#!/bin/bash

conda init
conda activate cm2

sleep 5
python checktiffs.py $1
wait
