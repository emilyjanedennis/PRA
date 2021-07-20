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
5- flip y? 1 yes 0 no, default 0
6- switch x and z? 1 yes 0 no, default yes (axial -> sagittal)
7- which annotations to use, default SIGMA

via sys.argv, usually from bash or sbatch and aligns using the 
folder logic from PRA repo, if you use different folder logic
or organizaiton, you'll need to change some of these functions
e.g. python 2 "/scratch/ejdennis/cm2_brains/a253/cells_642_filt.npy" 
	"/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco/pb_udisco_a253/imaging_request_1/rawdata/resolution_3.6x/elastix" 
	"/scratch/ejdennis/cm2_brains/aligned_cells/" 1 1 "MRI"
"""

import os, csv, json, shutil
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import SimpleITK as sitk
import tifffile as tif
import seaborn as sns

from utils.registration import points_resample, transform_points, create_text_file_for_elastix, modify_transform_files
from utils.registration import point_transformix, get_transform_files_from_folder, unpack_pnts

if __name__ == "__main__":

	# get numpy file of cells
	cells_filename = sys.argv[1]

	# get location where you want to save stuff to
	save_dir = sys.argv[3]

	# get location of elastix folder
	elastix_dir = sys.argv[2]

        # get flip y? default off
	if len(sys.argv) > 3:
		flip_y = int(sys.argv[4]
	else:
		flip_y = 0

	# get switch x and z default on
	if len(sys.argv) > 4:
		switch_x_and_z = bool(sys.argv[5])
	else:
		switch_x_and_z = True

        # get annotation file, name, labels
	if len(sys.argv) > 5:
		ann = sys.argv[6]
		# add if statements where if SIGMA, load sigma stuff
	else:
		ann = False

	# load cells, reorient if needed
	# save out as pdf_npy

	# get original dims
	# get resample dims
		
	# do first transform
	# rename

	# if needed, do second transform
	# rename

	# make some max projections and overlay on atlas, save out for easy QC
	# later add segment by values in atlas and output a data frame csv
