#!/usr/bin/env python3

"""
INPUTS: 
1. full path (str) to a tif file (moving volume)
2. full path (str) to a tif file (fixed volume)

OPTIONAL INPUTS
3. full path (str) to an output directory, if none, will use working directory + /transformix_out
4. full path (str) to an annotation file, if none, will not use

OUTPUTS:
1. folder in working directory or output directory of elastix alignment results
2. aligned volume
"""


import itk, os,sys
import tifffile as tif
import pandas as pd
from scipy.ndimage import zoom
import numpy as np


if __name__ == "__main__":

	if len(sys.argv) < 3:
		print('this script requires at minimum two inputs: a full path to the moving volume and a full path to the fixed volume (.tif)')
	else:
		mv_file = sys.argv[1]
		fx_file = sys.argv[2]
		if not os.path.isfile(mv_file):
			print('the first argument should be a full path to a .tif file, mv {} is not a file'.format(mv_file))
		elif not os.path.isfile(fx_file):
			if len(fx_file.split('_fused_12'))>1:
				f12=fx_file.split('_fused_12')[0]+'_fused-12.tif'
				justf=fx_file.split('_fused_12')[0]+'.tif'
				if os.path.isfile(f12):
					fx_file=f12
				elif os.path.isfile(justf):
					fx_file=justf
				else:
					print('both arguments should be a full path to a file, fx {} is not a file'.format(fx_file))
			elif len(fx_file.split('_fused-12'))>1:
                                f_12=fx_file.split('_fused-12')[0]+'_fused_12.tif'
                                justf=fx_file.split('_fused-12')[0]+'.tif'
                                if os.path.isfile(f_12):
                                        fx_file=f_12
                                elif os.path.isfile(justf):
                                        fx_file=justf
                                else:
                                        print('both arguments should be a full path to a file, fx {} is not a file'.format(fx_file))
	mv_base=os.path.basename(mv_file).split('.')[0]
	fx_base=os.path.basename(fx_file).split('.')[0]

	num_transforms=int(sys.argv[3])

	if len(sys.argv[4]) > 1:
		output_dir = sys.argv[4]
		if not os.path.isdir(output_dir):
			os.mkdir(output_dir)
	else:
		output_dir = os.path.join(os.path.dirname(fx_file),'output_{}_{}'.format(mv_base,fx_base))
		if not os.path.isdir(output_dir):
			os.mkdir(output_dir)
		print('using {} as ouput directory'.format(os.path.dirname(fx_file)))
	if len(sys.argv[4]) > 1:
		ann_file = sys.argv[4]
		if not os.path.isfile(ann_file):
			ann_vol=0
			print('ann_file entered is not a real file, not using ann file {}'.format(ann_file))
		elif ".tif" not in ann_file:
			print('ann_file entered is not a tif, not using ann_file: {}'.format(ann_file))
			ann_vol=0
		else:
			ann_vol = itk.imread(ann_file,pixel_type=itk.US)
			print('using ann file: {}'.format(ann_file))
			ann_base = os.path.basename(ann_vol).split('.')[0]
	else:
		ann_vol=0
	mv = itk.imread(mv_file,pixel_type=itk.US)
	fx = itk.imread(fx_file,pixel_type=itk.US)
	print('using mv_base {} and fx_base {}'.format(mv_base,fx_base))

	# make parameter object from files, this is somehow much faster than making programmatically 
	# num_transforms allows for flexible number of bsplines
	parameter_object = itk.ParameterObject.New()
	parameter_object.AddParameterFile('../parameter_folder/Order1_Par0000affine.txt')
	if num_transforms>1:
		parameter_object.AddParameterFile('../parameter_folder/Order3_Par0000bspline.txt')
	elif num_transforms>2:
		parameter_object.AddParameterFile('../parameter_folder/Order3_Par0000bspline.txt')
	else:
		parameter_object.AddParameterFile('../parameter_folder/Order3_Par0000bspline.txt')

	# align mv to fx
	result_img_elx, result_transform_params = itk.elastix_registration_method(fx,mv,parameter_object, log_to_file=True,output_directory = output_dir)
	
	# save aligned image
	tif.imsave(os.path.join(output_dir,"{}_to_{}.tif".format(mv_base,fx_base)),np.asarray(result_img_elx).astype(np.float32))

	# apply to anns if anns present
	if ann_vol != 0:
		result_image_transformix = itk.transformix_filter(ann_vol, result_transform_params)
		tif.imsave(os.path.join(output_dir,"{}_in_{}.tif".format(ann_base,fx_base)),np.asarray(result_image_transformix).astype(np.float32))

