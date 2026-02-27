"""
INPUTS:
1. full path (str) to a folder containing TransformParameter files
2. tif to transform
3. full path to where you'd like a tif saved (str ending in .tif)

OUTPUTS:
1. a folder of results from transformix

"""

import itkConfig
itkConfig.LazyLoading=False
# the above is required to have elxParameterObject "work"
import itk, os, sys
import tifffile as tif
import pandas as pd
import numpy as np


if __name__ == "__main__":

    # parse inputs
    if len(sys.argv)>3:
        transform_folder = sys.argv[1]
        mv_file = sys.argv[2]
        output_file = sys.argv[3]
    else:
        print('ERROR!!! you did not enter three inputs! you only entered {}'.format(sys.argv))
        sys.exit(1)
    if not os.path.isdir(transform_folder):
        new_transform_folder = transform_folder.split('fused')[0]+'fused_12'
        if os.path.isdir(new_transform_folder):
            transform_folder = new_transform_folder
        else:
            print('first input must be a string pointing to a folder, check your entry: {}'.format(transform_folder))
            sys.exit(1)
    if ".tif" in output_file:
        if not os.path.isdir(os.path.dirname(output_file)):
            os.mkdir(os.path.dirname(output_file))
    transform_files = [os.path.join(transform_folder,file) for file in os.listdir(transform_folder) if "TransformParameters" in file]
    if len(transform_files)==0:
        print('ERROR, there are no TransformParameters files in the folder supplied! \n check the folder: {}'.format(transform_folder))

    # load transform files, make transform object
    transform_to_apply=itk.elxParameterObjectPython.elastixParameterObject_New()
    for file in transform_files:
        transform_to_apply.AddParameterFile(file)

    # load image to transform, do transformation
    mv = itk.imread(mv_file)
    result_image_transformix = itk.transformix_filter(mv, transform_to_apply)

    # save out transformed image
    tif.imsave(output_file, np.asarray(result_image_transformix).astype(np.float32))
