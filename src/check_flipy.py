#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
function that takes a sys.argv, 
typically a parent folder provided via bash or sbatch command, 
and searches within that folder for any files ending in downsized_for_atlas.tif
It then takes the max projection along the final axis of that tiff
and saves it with the appendix _MAX

@author: ejdennis
"""

import os, sys, glob, shutil
import tifffile as tif 
import numpy as np

print(sys.argv)

listofdownsized = glob.glob(os.path.join(sys.argv[1],'*/*/rawdata/*/*downsized_for_atlas.tif'))

for filepath in listofdownsized:
	print(filepath)
	tif.imsave(filepath[:-4]+"_MAX.tif",np.amax(tif.imread(filepath),2))
