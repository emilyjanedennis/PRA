
import os, sys, time, glob, json, math, warnings, csv
import tifffile as tif
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns
import numpy as np
import pandas as pd
import scipy.spatial.distance as spd
import scipy.cluster as scc
import scipy.cluster.hierarchy as shc
from scipy.cluster.hierarchy import dendrogram, linkage, cophenet, fcluster
from sklearn.cluster import AgglomerativeClustering
import scipy
from scipy.spatial.distance import pdist
from scipy.ndimage.interpolation import zoom
from scipy import ndimage

from itertools import chain

from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache
from allensdk.api.queries.ontologies_api import OntologiesApi

if __name__ == '__main__':
	print('sysarg v output is {}'.format(sys.argv))
	Allen_grid_for_seg=tif.imread('/home/emilyjanedennis/Desktop/for_registration_to_lightsheet/tiffs/gridforseg.tif')
	mcc = MouseConnectivityCache(manifest_file='connectivity/mouse_connectivity_manifest.json')
	all_experiments = mcc.get_experiments(dataframe=True)

	x=int(sys.argv[1])-1

	dict_of_injs={}
	save_tiff=0
	xstart=x+1
	if len(all_experiments)>xstart+201:
		xend=xstart+201
	else:
		xend=len(all_experiments)+1

	for expid in all_experiments.id[xstart:xend]:
		x=x+1
		print('on {} id {}'.format(x,expid))
		p_d,pd_info=mcc.get_projection_density(expid)
		inj_mask,ind_info = mcc.get_injection_density(expid)
		dm,dm_info=mcc.get_data_mask(expid)

		dm[dm>0.5]=1
		inj_mask[inj_mask>0]=1

		#make a projection density that only has non-inj, valid vx
		new_pd=np.multiply(np.multiply(p_d,np.invert(inj_mask.astype('bool'))),dm)
		#save
		if save_tiff == 1:
			tif.imsave('/home/emilyjanedennis/Desktop/allens/projection_density_valid-noninj_{}.tif'.format(expid),new_pd)
			print('saved tiff')
		else:
			print('did not save tiff')
	    # add info to df
	    #for this experiment, which grids were injected?
		np.save('/home/emilyjanedennis/Desktop/allens/vector_inj_{}.npy'.format(expid),np.unique(Allen_grid_for_seg[inj_mask==False]))
		print('saved vector of inj')
	    # for this experiment, make and save a vector with all the Allen grids'info
		grid_vector=[]
		for grid_id in np.unique(Allen_grid_for_seg):
			grid_vector.append(np.sum(new_pd[Allen_grid_for_seg==grid_id]))
		np.save('/home/emilyjanedennis/Desktop/allens/vector_proj_{}.npy'.format(expid),grid_vector)
		print('saved vector of proj')
