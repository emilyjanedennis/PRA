#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
function that takes in a sys.argv, 
typically a folder provided via bash or sbatch slurm,
and finds all of the downsized_for_atlas.tif images within.
it then flips those sagittal images along the y axis
@author: ejdennis
"""

import os, sys, glob, shutil
import tifffile as tif 
import numpy as np

print(sys.argv)

listofdownsized = glob.glob(sys.argv[1]+"*downsized_for_atlas.tif")

for filepath in listofdownsized:
	print(filepath)
	tif.imsave(filepath,np.fliplr(tif.imread(filepath)))
