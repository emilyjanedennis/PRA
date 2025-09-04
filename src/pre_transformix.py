#!/usr/bin/env python3
"""
INPUTS:
1. full path (str) to a tif file (moving volume)

OPTIONAL INPUTS

OUTPUTS:
"""

import os, sys
import pandas as pd
import numpy as np
import tifffile as tif
import zarr

if __name__ == "__main__":

	if len(sys.argv) < 2:
		print('this requires one input: a string that is a full path to a bigstitcher folder containing an output folder')
		sys.exit(1)
	elif not os.path.isdir(os.path.join(sys.argv[1],'outputs')):
		os.mkdir(os.path.join(sys.argv[1],'outputs'))
		print('no outputs folder found, making one')
	else:
		fld=sys.argv[1]

	outfld=os.path.join(fld,'outputs')
	file = "filtered_cells.csv"
	try:
		stitched = np.load(os.path.join(fld,'tiffs','stitched.npy'), mmap_mode='r')
	except:
		print('ERROR! could not load stitched.npy file, check your path {}'.format(os.path.join(fld,'tiffs','stitched.npy')))
		sys.exit(1)
	try:
		df = pd.read_csv(os.path.join(outfld,file),header=None)
	except:
		print('ERROR! could not load {}, check your path!'.format(os.path.join(outfld,file)))
		sys.exit(1)
	df.columns=['x','y','z']
	stackshape=np.shape(stitched)
	xfull = stackshape[0]
	yfull= stackshape[1]
	zfull = stackshape[2]

	# put into downsampled space, have dims from file above
	for filename in os.listdir(fld):
		if ".tif" in filename:
			[dsz,dsy,dsx]=np.shape(tif.imread(os.path.join(fld,filename)))
	df['x_ds']=(df.x*(dsx/xfull)).astype(int)
	df['y_ds']=(df.y*(dsy/yfull)).astype(int)
	df['z_ds']=(df.z*(dsz/zfull)).astype(int)
	print('full x: {} \n full y: {} \n full z: {}'.format(xfull,yfull,zfull))
	print('ds x: {} \n ds y: {} \n ds z: {}'.format(dsx,dsy,dsz))
	df.to_csv(os.path.join(outfld,file[:-4]+'.csv'))

	# reformat for transformix
	intermediate=df[['x_ds','y_ds','z_ds']]
	intermediate.columns=['x','y','z']
	transformix_df = pd.DataFrame([['point','',''],[str(len(df)),'','']],columns=['x','y','z'])
	transformix_df = pd.DataFrame([['point','',''],[str(len(df)),'','']],columns=['x','y','z'])
	transformix_df=pd.concat([transformix_df,intermediate]).reset_index(drop=True)
	print('=================================')
	transformix_df.to_csv(os.path.join(outfld,file[:-4]+'_for-transformix.txt'),sep=' ',header=None,index=None)
