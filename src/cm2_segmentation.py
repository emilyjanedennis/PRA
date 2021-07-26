#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: ejdennis

takes cell centers in atlas space and uses
annotations to segment results by brain region
saves out 
- a 3d volume of cell centers
- a vector of data for pooling results
- a list of regions as a csv file

inputs are
1 - path to aligned .npy cells file
2 - path to annotation tiff
3 - path to annotation labels
4 - save dir
5 - brain name
6- channel
"""

import os, csv, json, shutil, glob, sys
import numpy as np
import pandas as pd
import tifffile as tif

if __name__ == "__main__":

	# load aligned cells
	cells = np.load(sys.argv[1])	
	cells = np.array(list(zip(*cells)))[0:3,:]
	# load an annotation volume (usually eroded) in atlas space
	ann_volume = tif.imread(sys.argv[2])
	print("shape of ann_vol = {}".format(np.shape(ann_volume)))
	ann_labels = pd.read_csv(sys.argv[3])

	# get save_dir, brainname, and channel
	save_dir = sys.argv[4]
	brain_name = sys.argv[5]
	ch = sys.argv[6]

	print("everything loaded")
	# get floor of aligned cells
	cells_floored = np.floor(cells).astype('int')
	print(np.shape(cells_floored))

	# find region for each cell center and make 3d volume of just cells
	region_list = []
	fails=0
	bool_cell_vol=np.zeros(np.shape(ann_volume))

	#debugging
	print("max x is {}".format(np.max(cells_floored[0,:])))
	print("max y is {}".format(np.max(cells_floored[1,:])))
	print("max z is {}".format(np.max(cells_floored[2,:])))


	print("making 3d volume and list")
	for i in np.arange(0,np.shape(cells_floored)[1]):
		z,y,x = cells_floored[:,i]
		try:
			if ann_volume[x,y,z] > 0:
				print(ann_volume[x,y,z])
				region_list.append(ann_volume[x,y,z])
			bool_cell_vol[x,y,z]+=1
		except:
			fails+=1
	print("{} failed points outside volume space".format(fails))

	tif.imsave(os.path.join(save_dir,"{}_{}_bool_cell_volume.tif".format(brain_name,ch)),bool_cell_vol.astype('uint8'))
	df_to_save = pd.DataFrame(region_list)
	df_to_save.to_csv(os.path.join(save_dir,"{}_{}_region_list.csv".format(brain_name,ch)))

	# make a vector for plotting
	ann_labels.insert(3,"cell_totals",value=0)
	for idx in np.arange(0,len(ann_labels)):
		ann_labels.cell_totals[idx]=region_list.count(int(ann_labels.id[idx]))
	# save vector
	np.save(os.path.join(save_dir,"{}_{}_vector.npy".format(brain_name,ch)),ann_labels.cell_totals.to_numpy())
