#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: ejdennis

inputs are
1- number of transoforms to do: if cell ch, 2 if reg ch, 1
2- string of npy filepath
3- elastix folder path
4- string where you want to save to

optional args:
5- brainname e.g. "e154", default "brainname"
6- flip y? 1 yes 0 no, default 0
7- switch x and z? 1 yes 0 no, default yes (axial -> sagittal)


via sys.argv, usually from bash or sbatch and aligns using the
folder logic from PRA repo, if you use different folder logic
or organizaiton, you'll need to change some of these functions
e.g. python 2 "/scratch/ejdennis/cm2_brains/a253/cells_642_filt.npy"
	"/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco/pb_udisco_a253/imaging_request_1/rawdata/resolution_3.6x/elastix"
	"/scratch/ejdennis/cm2_brains/aligned_cells/" 1 1 "mPRA"
"""

import os, csv, json, shutil, glob
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import SimpleITK as sitk
import tifffile as tif
import seaborn as sns

from utils.registration import points_resample, transform_points, create_text_file_for_elastix, modify_transform_files
from utils.registration import point_transformix, get_transform_files_from_folder, unpack_pnts, find_downsized_files
from utils.io import get_nested_tiffs

if __name__ == "__main__":

	if len(sys.argv) < 3:
		raise Exception('not enough arguments! only provided {}'.format(sys.argv))

	# get num of transforms to do 2 for cell, 1 for reg
	transform_type = int(sys.argv[1])

	# get numpy file of cells
	cells_filename = sys.argv[2]
	
	# get location of elastix folder
	elastix_dir = sys.argv[3]
	print(elastix_dir[-1])
	if elastix_dir[-1]=='/':
		elastix_dir = elastix_dir[:-1]

	# get location where you want to save stuff to
	save_dir = sys.argv[4]
	print(save_dir[-1])
	if '/' in save_dir[-1]:
		save_dir = save_dir[:-1]
	print(save_dir)

	if not os.path.isdir(save_dir):
		if os.path.isdir(os.path.dirname(save_dir)):
			os.mkdir(save_dir)
		else:
			raise Exception('save dir parent directory {} does not exist'.format(os.path.dirname(save_dir)))

	try:
		brainname = sys.argv[5]
	except:
		brainname = "brainname"

	# get flip y? default off
	# sometimes the imaging center images with the cerebellum at the top and
	# olfactory lobes at the bottom of the images, while our atlas is the opposite
	try:
		flip_y = int(sys.argv[6])
	except:
		flip_y = 0
	print("flip y is {}".format(flip_y))

	# get switch x and z default on
	# if True, this assumes that you have axial images and sagittal atlas/volumes
	try:
		switch_x_and_z = bool(int(sys.argv[7]))
	except:
		switch_x_and_z = True
	print("switch x and z is {}".format(switch_x_and_z))

	# load cells, reorient axial -> sagittal if needed
	df = pd.DataFrame(np.load(cells_filename))
	df = df.apply(pd.to_numeric,errors='coerce')
	if int(switch_x_and_z):
		print('switched: columns labeled z y x')
		df.columns=['z','y','x','size','source','bkrd']
		if not switch_x_and_z:
			print('but would not have been')	
	else:
		print('not switched, columns labeled x y z')
		df.columns = ['x','y','z','size','source','bkrd']
	print("df 0 is {}".format(df[df.index==0]))
	df_tosave = df[['z','y','x']].to_numpy()
	print("dftosave 0 is {}".format(df_tosave[0]))
	print("z max is {} y max is {} x max is {}".format(np.max(df['z']),np.max(df['y']),np.max(df['x'])))

	# filename to save cells in proper format, later we'll save after flipping y if needed
	if transform_type > 1:
		ch="642"
	else:
		ch="488"
	df_tosave_filename = os.path.join(save_dir,'{}_{}_cells.npy'.format(brainname,ch))

	# find reg__ and cell__ downsized_for_atlas files
	dszd_folder = find_downsized_files(elastix_dir)

	# get transform files and resample dims
	if transform_type > 1:
		# cells are in cell_ch
		transform_folders = [os.path.join(elastix_dir,"reg_to_cell"),os.path.join(elastix_dir,"atl_to_reg")]
		cell_file = os.path.join(dszd_folder,"cell__downsized_for_atlas.tif")
		# get resampled dims
		resampled_dims = np.shape(tif.imread(cell_file))
		# get original dims: find folder with full size data
		full_size_dir = os.path.join(os.path.dirname(elastix_dir),"Ex_642_Em_2_corrected")
	else:
		# cells are in reg_ch
		transform_folders = [os.path.join(elastix_dir,"atl_to_reg")]
		reg_file = os.path.join(dszd_folder,"reg__downsized_for_atlas.tif")
		resampled_dims = np.shape(tif.imread(reg_file))
		full_size_dir = os.path.join(os.path.dirname(elastix_dir),"Ex_488_Em_0_corrected")

	# get original dims, reorient and flip y if needed
	tiff_dir = get_nested_tiffs(full_size_dir)
	list_of_files = glob.glob(os.path.join(tiff_dir,"*.tif*"))

	z = len(list_of_files)
	y,x = np.shape(tif.imread(list_of_files[int(z/2)]))
	print("DIMENSIONS of raw tiffs (ZYX) {}".format((z,y,x)))

	if switch_x_and_z:
		original_dims = (x,y,z)
	else:
		original_dims = (z,y,x)

	if flip_y:
		df['y'] = -df['y'] + y
		df_tosave = df[['z','y','x']].to_numpy()
	np.save(df_tosave_filename,df_tosave)
	print('saved out {} as df with z,y,x formatting'.format(df_tosave_filename))

	print("DIMENSIONS of raw data AFTER FLIP, XY SWITCH (ZYX) ARE {}".format(original_dims))

	# get transform files
	transform_files = get_transform_files_from_folder(transform_folders[0])
	print("USING TRANSFORM FOLDER {}".format(transform_folders[0]))	
	# run transformation
	# reample first... [original_dims,resampled_dims]
	print("resampled dims are {}".format(resampled_dims))

	transform_points(df_tosave_filename,save_dir,transform_files,[original_dims,resampled_dims])
	# rename based on which process and if cell file, do second transform
	if transform_type > 1:
		# rename
		new_df_tosave_filename = os.path.join(save_dir,"{}_cell_in_reg_posttransform_zyx_voxels.npy".format(brainname))
		os.rename(os.path.join(save_dir,"posttransformed_zyx_voxels.npy"),new_df_tosave_filename)
		
		# DEBUGGING
		newdf = np.load(new_df_tosave_filename)
		print("MAX REG IN CELL DIMS ARE: (z,y,x) {},{},{}".format(np.max(newdf[:,0]),np.max(newdf[:,1]),np.max(newdf[:,2])))		
		print(" reg vol shape is {}".format(np.shape(tif.imread(os.path.join(dszd_folder,"reg__downsized_for_atlas.tif")))))

		transform_files = get_transform_files_from_folder(transform_folders[1])
		transform_points(new_df_tosave_filename,save_dir,transform_files)

		# prep to rename cell ch cells in atl space
		final_df_tosave_filename = os.path.join(save_dir,"{}_cell_in_atl_transform_zyx_voxels.npy".format(brainname))
	else:
		# prep to rename reg cells in atl space
		final_df_tosave_filename = os.path.join(save_dir,"{}_reg_in_atl_transform_zyx_voxels.npy".format(brainname))

	os.rename(os.path.join(save_dir,"posttransformed_zyx_voxels.npy"),final_df_tosave_filename)
