#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 15:13:28 2019
@author: emilyjanedennis borrowed heavily from wanglab
PURPOSE: to align a moving volume (or volumes) to a fixed volume
INPUTS:
	1. param_fld: a string containing the full path to a folder where the parameter files for alignment can be found
	2. [mvtiffs]: a list of strings. Either full paths or file names (if using optional input 4), e.g. ["/scratch/ejdennis/files_to_align/brain1.tiff", "/scratch/ejdennis/files_to_align/brain2.tiff"]
	3. fxtiff: a string containing a full path to a tiff file that you'd like to align the [mvtiffs] to
	4. output_dir: a string pointing to a full path where you'd like the outputs saved
OPTIONAL INPUTS:
	5. mult: default 1.4
 	6. src: a folder name where all the volumes are found, no default
OUTPUTS:
	for each mvtiff provided, it will produce two folders in output_dir (input 4). enlarged_tiffs, which contains the resized mvtiff (mult value * size of fxtiff) for alignment, and output_dirs which contains the step-by-step alignment, files, and final volume.
"""

import os
import numpy as np
import tifffile as tif
import sys
from scipy.ndimage import zoom
sys.path.append("../")
from utils.registration import elastix_command_line_call


if __name__ == "__main__":
	# deal with inputs to function

	try:
		param_fld=str(sys.argv[1])
		if not os.path.isdir(param_fld):
			print("the parameter folder {} does not exist, please check your path".format(param_fld))
		else: 
			print("using param_fld {}".format(param_fld))
	
	except:
		print("this function requires four inputs, the first must be a string containing a full path to the param_fld, e.g. '/scratch/ejdennis/parameter_folder_a2b')")

	try:
		mvtiffs = eval(str(sys.argv[2]))
		print(mvtiffs)
		if type(mvtifffs)!=list:
			print('the second input mvtiffs should be a list structured as ["/scratch/ejdennis/files_to_align/brain1.tiff","/scratch/ejdennis/files_to_align/brain2.tiff"] or ["brain1.tiff","brain2.tiff"] if using src (optional input 4). \n you entered {} which is a {}'.format(mvtiffs,type(mvtiffs)))
		else:
			for val in mvtiffs:
				if "tif" not in val[-4:]:
					print("at least one mvtiff file is not a tiff file, check {}".format(val))
					break
	except:
		print("this function requires four inputs, the second input (mvtiffs) should be a list containing strings, e.g.  ['/scratch/ejdennis/files_to_align/brain1.tiff','/scratch/ejdennis/files_to_align/brain2.tiff'] or ['brain1.tiff','brain2.tiff'] if using src (optional input 4)")

	try:
		fxtiff = str(sys.argv[3])
		if not os.path.isfile(fxtiff):
			print("the third input (fxtiff) should be a string pointing to a file, you entered {} which does not exist".format(fxtiff))
		elif "tif" not in fxtiff[-4:]:
			print("the third input (fxtiff) must be a tif or tiff file, you entered {}".format(fxtiff))
	except:
		print("this function requires four inputs, the third input (fxtiff) must be a full path to a tiff file")

	try:
		output_dir = str(sys.argv[4])
		if not os.path.isdir(outputdir):
			os.mkdir(output_dir)
	except:
		print("this function requires four inputs, the fourth must be a folder with a parent directory that exists")

	if len(sys.argv) > 5:
		try:
			mult=float(sys.argv[5])
			src=""
		except:
			print("a fifth argument (mult) was provided, but it could not be converted to a float, USING DEFAULT VALUE OF 1.4")
	else:
		mult=1.4
		src=""

	if len(sys.argv) > 6:
		try:
			if os.path.isdir(str(sys.argv[6])):
				src=str(sys.argv[6])
			else:
				src=""
				print("a sixth argument (src) was provided as {} but it is not a directory, proceeding with no src".format(sys.argv[6]))
		except:
			src=""
			print('no sixth argument, no src used')
	print("printing all inputs: param_fld, mvtiffs, fxtiff, output_dir, mult, src".format(param_fld, mvtiffs, fxtiff, output_dir, mult, src))

	for pairnum in np.arange(0,len(mvtiffs)):
		mvtiff = mvtiffs[pairnum]
		mvtiff_base=os.path.basename(mvtiff).split('.')[0]
		fxtiff_base=os.path.basename(fxtiff).split('.')[0]
		print(fxtiff)
		print('mvtiff')
		print(mvtiff)
		print('mvtiff_base')
		print(mvtiff_base)
		fx = os.path.join(src,fxtiff)
		mv = os.path.join(src,mvtiff)
		output_filename = os.path.join(output_dir,"enlarged_tiffs/{}_for_{}.tif".format(mvtiff_base,fxtiff_base))
		print('output_filename')
		print(output_filename)
		print('output_directory')
		output_directory = os.path.join(output_dir,"{}_to_{}".format(mvtiff_base,fxtiff_base))
		print(output_directory)
		if not os.path.isdir(os.path.join(output_dir,"enlarged_tiffs")):
			os.mkdir(os.path.join(output_dir,"enlarged_tiffs"))
		if not os.path.isdir(output_directory):
			os.mkdir(output_directory)
		
		# need to make moving larger (~140% seems to work well?) to transform to fixed
		moving = tif.imread(mv)
		fixed = tif.imread(fx)
		zf, yf, xf = (fixed.shape[0]/moving.shape[0])*mult, (
			    fixed.shape[1] /
	    		moving.shape[1])*mult, (fixed.shape[2]/moving.shape[2])*mult
		print("\nzooming...")
		moving_for_fixed = zoom(moving, (zf, yf, xf), order=0,mode='nearest')

		# saved out volume
		print("\nsaving zoomed volume...")
		tif.imsave(output_filename,moving_for_fixed.astype("uint16"))


		if not os.path.exists(output_directory):
	    		os.mkdir(output_directory)

		params = [os.path.join(param_fld, xx) for xx in os.listdir(param_fld)]
		params.sort()
		e_out, transformfiles = elastix_command_line_call(fx, output_filename, output_directory, params)
