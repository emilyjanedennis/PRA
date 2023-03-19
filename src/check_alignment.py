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

listofdownsized = glob.glob(os.path.join(sys.argv[1],'*/*/rawdata/resolution_3.6x/elastix/*/result*.tif'))

for filepath in listofdownsized:
	print(filepath)
	fileparts = filepath.split('/')
	savename = os.path.join(sys.argv[2],'{}_{}_{}_MAX.tif'.format(fileparts[-7],fileparts[-2],fileparts[-1][:-4]))
	tif.imsave(savename,np.amax(tif.imread(filepath),2))
