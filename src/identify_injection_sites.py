#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: ejdennis
"""

import os, cv2, shutil, sys
import numpy as np
import tifffile as tif
import SimpleITK as sitk
import multiprocessing as mp
from skimage.transform import resize
sys.path.append("utils")
from utils.registration import transformix_command_line_call


def optimize_inj_detect(src, threshold=3, filter_kernel = (3,3,3), dst=False,
                        num_sites_to_keep=1):
    """Function to test detection parameters
    
    "dst": (optional) path+extension to save image
    
    """
    if type(src) == str: 
        src = tif.imread(src)
    arr = find_site(src, thresh=threshold, 
          filter_kernel=filter_kernel, num_sites_to_keep=num_sites_to_keep)*255
    fig = plt.figure()
    fig.add_subplot(1,2,1)
    plt.imshow(np.max(arr, axis=0));  plt.axis("off")
    fig.add_subplot(1,2,2)
    plt.imshow(np.max(src, axis=0), cmap="jet");  plt.axis("off")
    
    if dst: plt.savefig(dst, dpi=300)
    
    return arr


def find_site(im, thresh=10, filter_kernel=(5,5,5), num_sites_to_keep=1):
    """Find a connected area of high intensity, using a basic filter + threshold + connected components approach
    
    by: bdeverett

    Parameters
    ----------
    img : np.ndarray
        3D stack in which to find site (technically need not be 3D, so long as filter parameter is 
        adjusted accordingly)
    thresh: float
        threshold for site-of-interest intensity, in number of standard deviations above the mean
    filter_kernel: tuple
        kernel for filtering of image before thresholding
    num_sites_to_keep: int, number of injection sites to keep, useful if multiple distinct sites
    
    Returns
    --------
    bool array of volume where coordinates where detected
    """
    from scipy.ndimage.filters import gaussian_filter as gfilt
    from scipy.ndimage import label
    if type(im) == str: im = tifffile.imread(im)

    filtered = gfilt(im, filter_kernel)
    thresholded = filtered > filtered.mean() + thresh*filtered.std() 
    labelled,nlab = label(thresholded)

    if nlab == 0:
        raise Exception("Site not detected, try a lower threshold?")
    elif nlab == 1:
        return labelled.astype(bool)
    elif num_sites_to_keep == 1:
        sizes = [np.sum(labelled==i) for i in range(1,nlab+1)]
        return labelled == np.argmax(sizes)+1
    else:
        sizes = [np.sum(labelled==i) for i in range(1,nlab+1)]
        vals = [i+1 for i in np.argsort(sizes)[-num_sites_to_keep:][::-1]]
        return np.in1d(labelled, vals).reshape(labelled.shape)


def get_inj_flexibly(filename):
    src_tif = tif.imread(filename).swapaxes(0,2)#load axial image
    try:
        arr = optimize_inj_detect(src_tif, threshold=10, filter_kernel = (5,5,5), num_sites_to_keep=1)
    except:
        print('failed with threshold 10, kernel 5s, trying with 3t/50sk')
        try:
            arr = optimize_inj_detect(src_tif, threshold=3, filter_kernel = (50,50,50), num_sites_to_keep=1)
        except:
            print('failed with threshold 3, filters 50s, trying with 2t/50sk')
            arr = optimize_inj_detect(src_tif, threshold=2, filter_kernel=(50,50,50), num_sites_to_keep=1)
    return arr

if __name__ == "__main__":

    # inputs should be just a folder that has elastix, cell__downsized_for_atlas.tif and reg__downsized_for_atlas.tif
    # also should be able to save out to another place

    print('printing sys.argvs: stepid, src, dst')
    print(sys.argv)
    stepid = str(sys.argv[1])
    src=str(sys.argv[2]) #folder to main image folder
    dst = str(sys.argv[3])
   
    # first, find the reg__ and cell__ files
    if os.path.exists(os.path.join(src,'reg__downsized_for_atlas.tif')):
        output_src = src
    elif os.path.exists(os.path.join(os.path.dirname(src),'reg__downsized_for_atlas.tif')):
        output_src = os.path.dirname(src)
    else:
        output_src = os.path.dirname(os.path.dirname(src))
    print("src is {}".format(output_src))

    reg_filename = os.path.join(output_src,"reg__downsized_for_atlas.tif")
    reg_inj_filename = os.path.join(dst,"reg_inj_site.tif")
    reg_transformix_folder = os.path.join(dst,"reg_inj_in_atl")
    cell_filename = os.path.join(output_src,"cell__downsized_for_atlas.tif")
    cell_inj_filename = os.path.join(dst,"cell_in_reg_inj_site.tif")
    cell_transformix_folder = os.path.join(dst,"cell_inj_in_atl")

    if int(stepid)==0:
        # make tiffs that contain the most likely inj sites in registration volume for reg and cell if it exists
        arr = get_inj_flexibly(reg_filename)
        tif.imsave(reg_inj_filename,arr.swapaxes(0,2).astype('uint8'))
        print('saved tiff of inj in reg at {}'.format(dst))
        if os.path.exists(cell_filename):
       	    arr = get_inj_flexibly(cell_filename)
            tif.imsave(cell_ing_filename,arr.swapaxes(0,2).astype('uint8'))
            print('saved tiff of inj in cell registered to reg at {}'.format(dst))

    if int(stepid)==1:
        # next, find the elastix files
        elsrc=os.path.join(os.path.dirname(src),"elastix")
        
        # now take the transform files from reg -> atl
        transformfolder = os.path.join(elsrc,"reg_to_atl")
        transformfiles=[]
        for file in transformfolder:
            if "TransformParam" in file:
                transformfiles.append(os.path.join(transformfolder, file))

        # now use transformix
        if ~os.path.dir(reg_transformix_folder):
            os.mkdir(reg_transformix_folder)
        transformix_command_line_call(reg_in_filename, reg_transformix_folder, transformfiles[-1])

        if os.path.exists(cell_filename):
            if ~os.path.dir(cell_transformix_folder):
                os.mkdir(cell_transformix_folder)
            transformix_command_line_call(cell_in_filename,cell_transformix_folder,transformfiles[-1])
            #do for cell too
    
