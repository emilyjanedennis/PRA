#!/usr/bin/env python3

"""
INPUTS:
1. full path (str) to a folder containing TransformParameter files
2. csv of points to transform
3. moving image used to make the TransformParameters (tif)

OPTIONAL INPUTS
4. full path to an output_directory (str)

OUTPUTS:
1. a folder of results from transformix
2. a csv of cell locations in moving coordinates

"""

import itkConfig
itkConfig.LazyLoading=False
# the above is required to have elxParameterObject "work"
import itk, os, sys
import tifffile as tif
import pandas as pd
from scipy.ndimage import zoom
import numpy as np


if __name__ == "__main__":

	# parse inputs
	if len(sys.argv)>3:
		transform_folder = sys.argv[1]
		points_txt = sys.argv[2]
		mv_file = sys.argv[3]
	else:
		print('ERROR!!! you did not enter three inputs! you only entered {}'.format(sys.argv))
		sys.exit(1)
	if not os.path.isdir(transform_folder):
		new_transform_folder = transform_folder.split('fused')[0]+'fused_12'
		if os.path.isdir(new_transform_folder):
			transform_folder = new_transform_folder
		else:
			print('first input must be a string pointing to a folder, check your entry: {}'.format(transform_folder))
			sys.exit(1)
	transform_files = [os.path.join(transform_folder,file) for file in os.listdir(transform_folder) if "TransformParameters" in file]
	if len(transform_files)==0:
		print('ERROR, there are no TransformParameters files in the folder supplied! \n check the folder: {}'.format(transform_folder))
		sys.exit(1)
	try:
		mv=itk.imread(mv_file)
	except:
		print('ERROR! {} is not an image file or cannot be opened'.format(mv_file))
		sys.exit(1)
	try:
		pd.read_csv(points_txt)
	except:
		print('ERROR! {} is not a points.txt file, check contents or path'.format(points_txt))
		sys.exit(1)

	if len(sys.argv) > 4 and len(sys.argv[4])>0:
		if os.path.isdir(sys.argv[4]):
			output_directory = sys.argv[4]
		else:
			print('error, output_directory provided was not a directory. check path: {}'.format(output_directory))
			output_directory = os.path.join(os.path.dirname(transform_folder),'outputs')
			if not os.path.isdir(output_directory):
				os.mkdir(output_directory)
	else:
		output_directory = os.path.join(os.path.dirname(transform_folder),'outputs')
		if not os.path.isdir(output_directory):
			os.mkdir(output_directory)
	print('using output_directory: {}'.format(output_directory))

	# make transform from files
	transform_to_apply=itk.elxParameterObjectPython.elastixParameterObject_New()
	transform_files.sort()
	for file in transform_files:
		transform_to_apply.AddParameterFile(file)

	# remember, this is taking points from the FIXED volume and places them in the MOVING volume
	# for example, to get points in the allen atlas, you should be using a transform folder produced
	# by aligning the allen (mv) TO your brain with cells (fx)
	transformixed_coords=itk.transformix_pointset(mv, transform_to_apply,fixed_point_set_file_name=points_txt,output_directory=output_directory)
	dfx=pd.DataFrame(transformixed_coords)
	dfx.columns = dfx.columns.astype(str)
	dfx = dfx[['46','47','48']]
	dfx.columns = ['x','y','z']
	dfx.x=dfx.x.astype(int)
	dfx.y=dfx.y.astype(int)
	dfx.z=dfx.z.astype(int)
	dfx.to_csv(os.path.join(output_directory,'{}_points_transformixed.csv'.format(os.path.basename(points_txt)[:-4])))
