#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time, glob, json, math, warnings, csv
import tifffile as tif
import numpy as np
import pandas as pd
from allensdk.core.mouse_connectivity_cache import MouseConnectivityCache
from allensdk.api.queries.ontologies_api import OntologiesApi

from itertools import chain

mcc = MouseConnectivityCache(manifest_file='connectivity/mouse_connectivity_manifest.json')
all_experiments = mcc.get_experiments(dataframe=True, cre=False)

tiffdir ='/home/emilyjanedennis/Desktop/for_registration_to_lightsheet/tiffs'
labelsdir = '/home/emilyjanedennis/Desktop/for_registration_to_lightsheet/labels'

df_30=pd.read_csv(os.path.join(labelsdir,'grid_with_vx.csv'))
matlas_30_in_allen=tif.imread(os.path.join(tiffdir,'matlas_30_grid_in_Allen_template_sagittal.tif'))
matlas_30_in_allen=np.moveaxis(matlas_30_in_allen,0,-1)
df_sigma=pd.read_csv(os.path.join(labelsdir,'SIGMA_with_voxels.csv'))
sigma_in_allen=tif.imread(os.path.join(tiffdir,'SIGMA_sagittal_ann_in_Allen_template_sagittal.tif'))
sigma_in_allen=np.moveaxis(sigma_in_allen,0,-1)
df_allen=pd.read_csv(os.path.join(labelsdir,'allen_with_voxels.csv'))
allen_anns=tif.imread(os.path.join(tiffdir,'Allen_annot.tif'))

n=420
df_30=pd.read_csv('/home/emilyjanedennis/Desktop/df_30.csv')
df_sigma=pd.read_csv('/home/emilyjanedennis/Desktop/df_sigma.csv')
df_allen=pd.read_csv('/home/emilyjanedennis/Desktop/df_allen.csv')


for exp_id in all_experiments.id[n:]:
    # get projden
    n+=1
    print(exp_id)
    projden, pd_info = mcc.get_projection_density(exp_id)
    dm, dm_info = mcc.get_data_mask(exp_id)
    projden=np.multiply(projden,dm)
    maxvals=[]
    for idx in df_30.index:
        try:
            maxvals.append(np.max(projden[matlas_30_in_allen==df_30.grid_id[idx]]))
        except:
            maxvals.append(0)
    df_30.insert(n,str(exp_id),maxvals)
    maxvals=[]
    for idx in df_sigma.index:
        try:
            maxvals.append(np.max(projden[sigma_in_allen==df_sigma.ID[idx]]))
        except:
            maxvals.append(0)
    df_sigma.insert(n,str(exp_id),maxvals)
    maxvals=[]
    for idx in df_allen.index:
        try:
            maxvals.append(np.max(projden[allen_anns==df_allen.id[idx]]))
        except:
            maxvals.append(0)

    df_allen.insert(n,str(exp_id),maxvals)

    if n==2 or n%20 == 0:
        print('interim save at n={} and expid={}'.format(n,exp_id))
        df_30.to_csv('/home/emilyjanedennis/Desktop/df_30.csv')
        df_sigma.to_csv('/home/emilyjanedennis/Desktop/df_sigma.csv')
        df_allen.to_csv('/home/emilyjanedennis/Desktop/df_allen.csv')
df_30.to_csv('/home/emilyjanedennis/Desktop/df_30.csv')
df_sigma.to_csv('/home/emilyjanedennis/Desktop/df_sigma.csv')
df_allen.to_csv('/home/emilyjanedennis/Desktop/df_allen.csv')

