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

if __name__ == "__main__":

	if len(sys.argv) < 2:
		print('this requires one input: a string that is a full path to a bigstitcher folder containing an output folder')
	elif not os.path.isdir(os.path.join(sys.argv[1],'outputs')):
		print('no outputs folder found, check path {}'.format(sys.argv[1]))
	else:
		fld=sys.argv[1]

	outfld=os.path.join(fld,'outputs')
	with open(os.path.join(outfld,'bounding_box.txt'),'r') as file:
		for line in file:
			if "bounding" in line:
				x=line
	dims = eval(x.split('dimensions ')[1])
	bounds=eval(x.split('[')[1].split(']')[0])
	print('bounds are: {}'.format(bounds))
	if type(bounds)!=tuple:
        	print('ERROR: bounds were not found correctly, should be a tuple, but is this {}'.format(bounds))
	elif type(dims)!=tuple:
		print('ERROR: dims were not found correctly, should be a tuple but is this {}'.format(dims))
	else:
		# now get the dfs and adjust them, save adjusted dfs but save out for transformix!
		listoffiles=[file for file in os.listdir(outfld) if 'bigstitcher_out.txt' in file]
		# for each file, adjust!
		for file in listoffiles:
			df = pd.read_csv(os.path.join(outfld,file),header=None)
			df.columns=['x','y','z']
			df['x_adj']=df.x-bounds[0]
			df['y_adj']=df.y-bounds[1]
			df['z_adj']=df.z-bounds[2]
			print(os.path.join(outfld,file[:-4]+'csv'))
                        # put into downsampled space, have dims from file above
			for testfile in os.listdir(fld):
				if "fused" in testfile and ".tif" in testfile:
					[dsz,dsy,dsx]=np.shape(tif.imread(os.path.join(fld,testfile)))
			df['x_ds']=(df.x_adj*(dsx/dims[0])).astype(int)
			df['y_ds']=(df.y_adj*(dsy/dims[1])).astype(int)
			df['z_ds']=(df.z_adj*(dsz/dims[2])).astype(int)
			df.to_csv(os.path.join(outfld,file[:-4]+'.csv'))
			# reformat for transformix
			intermediate=df[['x_ds','y_ds','z_ds']]
			intermediate.columns=['x','y','z']
			transformix_df = pd.DataFrame([['point','',''],[str(len(df)),'','']],columns=['x','y','z'])
			transformix_df = pd.DataFrame([['point','',''],[str(len(df)),'','']],columns=['x','y','z'])
			transformix_df=pd.concat([transformix_df,intermediate]).reset_index(drop=True)
			print('=================================')
			transformix_df.to_csv(os.path.join(outfld,file[:-4]+'_for-transformix.txt'),sep=' ',header=None,index=None)
