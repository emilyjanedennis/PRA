#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
function to take an input, usually via bash or sys.argv
that is a folder of folders (e.g. /scratch/ejdennis/cm2_brains
which would contain folders like a253, e131)

if files have generic names, we replace them with specific names
regardless, if a subfolder has "*_inj_in_atl.tif" files, we take
them, make a MAX projection, and add them to our tifflist.

We then divide tifflist by the # of tifs to get an average brain

@author: ejdennis
"""

import os, cv2, shutil, sys, glob
import numpy as np
import tifffile as tif

folder = sys.argv[1]
dst = sys.argv[2]

tifflist=0
arr = []

for foldername in os.listdir(folder):
    print('foldername is {}'.format(foldername))
    # first, rename generally named files
    if os.path.exists(os.path.join(folder,foldername,"cell_inj_in_atl.tif")):
        os.rename(os.path.join(folder,foldername,"cell_inj_in_atl.tif"),os.path.join(folder,foldername,"{}_cell_inj_in_atl.tif".format(foldername)))
    if os.path.exists(os.path.join(folder,foldername,"reg_inj_in_atl.tif")):
        os.rename(os.path.join(folder,foldername,"reg_inj_in_atl.tif"),os.path.join(folder,foldername,"{}_reg_inj_in_atl.tif".format(foldername)))
    # next, get all the inj_in_atl files
    for file in os.listdir(os.path.join(folder,foldername)):
        print(file)
        if "inj_in_atl.tif" in file:
            print("using tif {}".format(os.path.join(folder,foldername,file)))
            thistif = tif.imread(os.path.join(folder,foldername,file))

            # make max projections in this folder and save as MAX_ prefix
            tif.imsave(os.path.join(folder,foldername,"MAX_sagittal_{}".format(file)),np.amax(thistif,2))
            tif.imsave(os.path.join(folder,foldername,"MAX_axial_{}".format(file)),np.amax(thistif,0))
       	    tif.imsave(os.path.join(folder,foldername,"MAX_coronal_{}".format(file)),np.amax(thistif,1))
            # if this is the first brain, make arr == this brain array
            # if not, add it to the existing array
            if len(arr)==0:
                arr = thistif.copy()
            else:
                arr=np.add(arr,thistif.copy())

# after all folders are finished, divide by the length and
# save out the metatiff to the dst
arr = np.divide(arr,len(arr))
tif.imsave(os.path.join(dst,'metatiff.tif'),arr.astype('uint16'))
