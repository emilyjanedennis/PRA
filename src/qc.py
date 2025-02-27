#!/usr/bin/env python3

# the above is required to have elxParameterObject "work"
import os, sys
import tifffile as tif
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
INPUTS: 
1. string of basename, e.g. "2024-01-08_100346"
OPTIONAL INPUTS:
OUTPUTS:
"""

if __name__ == "__main__":

	if len(sys.argv) < 1:
		print('ERROR, you did not provide any inputs! this script requires a basename, like 2024-01-08_100346')
		sys.exit(1)
	else:
		basename=sys.argv[1]
	if not os.path.isdir(os.path.join('/groups/dennis/dennislab/Imaging/raw_imaging_data',basename,'processed/bigstitcher')):
		print('ERROR: {} is not a real directory! check your inputs'.format(os.path.join('/groups/dennis/dennislab/Imaging/raw_imaging_data',basename,'processed/bigstitcher'))
		sys.exit(1)
	else:
		basefolder = os.path.join('/groups/dennis/dennislab/Imaging/raw_imaging_data',basename,'processed/bigstitcher')
		print('using base path : {}'.format(basepath))

	output_fld = 
	stitched = np.load(os.path.join(basefolder,'tiffs/stitched.npy'), mmap_mode='r')
	print('shape of stitched file: ',np.shape(stitched)

	cellsfilt = np.load(os.path.join(basefolder,'tiffs/cells_filtered.npy'))
        if len(sys.argv)>2:
                output_fld = sys.argv[2]
        else:
                output_fld = os.path.join(basefolder,'qc')
		if not os.path.isdir(output_fld):
			os.mkdir(output_fld)

	xr=np.ceil(np.shape(stitched)[0]/1000)
	yr=np.ceil(np.shape(stitched)[1]/1000)
	plt.figure(figsize=(xr,yr))
	plt.scatter(cellsfilt['x'],cellsfilt['y'],s=1,c='k')#,c=cellsfilt['z'])
	plt.ylim(np.shape(stitched)[1],0)
	plt.title('cm2 output')
	plt.savefig(os.path.join(output_fld,'{}_cm2out.png'.format(basename)))
	plt.close()

cellsfilt = np.load(os.path.join(basefolder,'tiffs/cells_filtered.npy'))
cellsdf=pd.read_csv(os.path.join(basefolder,'outputs/filtered_cells.csv'))
plt.figure(figsize=(6,8))
plt.scatter(cellsdf.x_ds,cellsdf.y_ds,s=1,c='k')#,c=dsval.z_ds)
plt.ylim(800,0)
plt.title('downsampled volume space used for transformix')
plt.savefig(os.path.join(output_fld,'{}_cm2_downsampled.png'.format(basename)))
plt.close()

# transformed data (in downsampled volume space)
cellst = pd.read_csv(os.path.join(basefolder,'transformix_out/filtered_cells_for-transformix_points_transformixed.csv'))

plt.figure(figsize=(5,5.5))
plt.scatter(cellst.x,cellst.y,s=1,c='k')#,c=dsval.z_ds)
plt.ylim(550,0)
plt.title('transformixed points')
plt.savefig(os.path.join(output_fld,'{}_transformixed.png'.format(basename)))
plt.close()
