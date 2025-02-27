#!/usr/bin/env python3

# the above is required to have elxParameterObject "work"
import os, sys
import tifffile as tif
import pandas as pd
from scipy.ndimage import zoom
import numpy as np

"""
INPUTS: 
1. full path of a folder containing "..._points_transformixed.csv" files
2. full path to an annotation volume
3. full path to an annotation file
4. full path to an annotation mask
"""

if __name__ == "__main__":

	# parse inputs
	if len(sys.argv)>3:
		fld = sys.argv[1]
		ann_vol_path = sys.argv[2]
		ann_file_path = sys.argv[3]
		mask_vol_path=sys.argv[4]
	else:
		print('ERROR!!! you did not enter three inputs! you only entered {}'.format(sys.argv))



	# read in a folder with csvs with all the data
	#/groups/dennis/dennislab/Imaging/raw_imaging_data/2024-11-19_124952/processed/bigstitcher/transformix_out/
	filelist=[]
	dfs=[]
	for file in os.listdir(fld):
		if "_points_transformixed" in file:
			filelist.append(os.path.join(fld,file))
			dfs.append(pd.read_csv(filelist[-1],index_col=0))
			print('on file {}'.format(file))
	df = pd.concat(dfs,ignore_index=True)
	
	# now we have a df with all the cell centers in the annotation volume
	# next we need to go through the cells, place them in a volume, and summarize
	mvshape=np.shape(tif.imread(ann_vol_path))
	annvol=tif.imread(ann_vol_path)
	cells = np.zeros(np.shape(tif.imread(ann_vol_path)))
	for idx in df.index:
		x,y,z=[df.x[idx],df.y[idx],df.z[idx]]
		if (x<mvshape[0]) and (y<mvshape[1]) and (z<mvshape[2]):
			cells[x,y,z]+=1
	mask=tif.imread(mask_vol_path)
	cells=cells*mask
	np.save(os.path.join(fld,'cells_vol.npy'),cells)
	
	#summarize in a csv
	cellcounts=[]
	areas=[]
	anndf=pd.read_csv(ann_file_path)
	for idx in anndf.index:
		#allen_label_no
		thiscount=np.sum(cells[annvol==anndf.allen_label_no[idx]])
		cellcounts.append(thiscount)
		thisarea=len(annvol[annvol==anndf.allen_label_no[idx]])
		areas.append(thisarea)
		print(idx,anndf.allen_label_no[idx],'count ',thiscount,'area ',thisarea)
	cellpercent=(cellcounts/np.sum(cellcounts))*100
	anndf['cellcounts']=cellcounts
	anndf['areas']=areas
	anndf['percentofcells']=cellpercent
	anndf['cellspervoxel']=anndf.cellcounts/anndf.areas
	anndf.to_csv(os.path.join(fld,'celldata_out.csv'))
