#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""

Created on Mon Jul 27 17:37:30 2020

@author: wanglab, overhaul by ejdennis

purpose is to use the transform parameter files from an alignment to
get an image into another image's space (e.g. cell channel in reg volume space)

inputs are:
1 - full path to moving image (tiff)
2 - full path to fixed image (tiff)
3 - full path to the transform folder
4 - full path to the destination folder

optional inputs and their defaults are
5 - 0+ zoom amount (default 1.4x)
6 - 1 or 0: if jacobian determinate volumes and geometric displacement volumes should be made (default to 0, no)
"""


import os
import sys
import time
import tifffile as tif
import numpy as np
from scipy.ndimage.interpolation import zoom

sys.path.append("..")

from utils.registration import transformix_command_line_call, transformix_plus_command_line_call
from utils.registration import modify_transform_files, change_interpolation_order

print("sys.argv are: {}".format(sys.argv))

mv = sys.argv[1]
fx = sys.argv[2]
transformfldr = sys.argv[3]
dstfldr = sys.argv[4]

if len(sys.argv)>5:
	zoom = int(sys.argv[5])
else:
	zoom=1.4

if len(sys.argv)>6:
	jac=1
else:
	jac=0

moving = tif.imread(mv)
fixed = tif.imread(fx)

if zoom > 0:
        enlargedfilename= os.path.join(dstfldr,'zoomed.tif')
        zf, yf, xf = (fixed.shape[0]/moving.shape[0])*zoom, (fixed.shape[1] / moving.shape[1])*zoom, (fixed.shape[2]/moving.shape[2])*zoom)
        print("\nzooming...")
        moving_for_fixed = zoom(moving,(zf,yf,xf),order=0)
	
	print("\nsaving zoomed volume...")
	tif.imsave(enlargedfilename,moving_for_fixed.astype("uint16"))
else:
	enlargedfilename = mv

# copy the parameter files
a2r = [os.path.join(transformfldr, xx) for xx in os.listdir(transformfilepath) if "Transform" in xx]
a2r.sort()
	
transformfiles = modify_transform_files(transformfiles=a2r, dst=dst)[change_interpolation_order(xx, 0) for xx in transformfiles]
	
# change the parameter in the transform files that outputs 16bit images i>
for fl in transformfiles:  # Read in the file
	with open(fl, "r") as file:
		filedata = file.read()
	# Replace the target string
	filedata = filedata.replace('(ResultImagePixelType "float")', '(ResultImagePixelType "short")')
	
	# Write the file out again
	with open(fl, "w") as file:
		file.write(filedata)

# run transformix
if jac > 0:
	transformix_plus_command_line_call(enlargedfilename, dst, transformfiles[-1])
else:
	transformix_command_line_call(enlargedfilename, dst, transformfiles[-1])

