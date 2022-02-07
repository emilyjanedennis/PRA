
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
		inj_mask,ind_info = mcc.get_injection_density(expid)
		inj_mask[inj_mask>0]=1

	    #for this experiment, which grids were injected?
		np.save('/home/emilyjanedennis/Desktop/allens/vector_inj_{}.npy'.format(expid),np.unique(np.multiply(Allen_grid_for_seg,inj_mask)))
		print('saved vector of inj')
