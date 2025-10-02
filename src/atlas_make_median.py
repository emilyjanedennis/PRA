"""
Created on Sat Nov 16 13:49:34 2019
@author: wanglab
heavily edited by ejd 20251002
"""

import os
import tifffile as tif
import numpy as np
import sys
import datetime

def load_memmap_arr(pth, mode="r", dtype = "uint16", shape = False):
    """
    Function to load memmaped array.

    Inputs
    -----------
    pth: path to array
    mode: (defaults to r)
    +------+-------------------------------------------------------------+
    | "r"  | Open existing file for reading only.                        |
    +------+-------------------------------------------------------------+
    | "r+" | Open existing file for reading and writing.                 |
    +------+-------------------------------------------------------------+
    | "w+" | Create or overwrite existing file for reading and writing.  |
    +------+-------------------------------------------------------------+
    | "c"  | Copy-on-write: assignments affect data in memory, but       |
    |      | changes are not saved to disk.  The file on disk is         |
    |      | read-only.                                                  |
    dtype: digit type
    shape: (tuple) shape when initializing the memory map array

    Returns
    -----------
    arr
    """
    if shape:
        assert mode =="w+", "Do not pass a shape input into this function unless initializing a new array"
        arr = np.lib.format.open_memmap(pth, dtype = dtype, mode = mode, shape = shape)
    else:
        arr = np.lib.format.open_memmap(pth, dtype = dtype, mode = mode)
    return arr

if __name__ == "__main__":

    #INPUTS
    # brainslist - list of strings, all full paths to tif files
    # outputdir - a string leading to a directory where we should save the data
    # final tiff name OPTIONAL

    # first let's process and check the inputs
    if len(sys.argv) < 3:
        print('this script requires at minimum two inputs: ["a list of full paths to images"] and an ouutput directory')
        sys.exit(1)
    elif len(sys.argv[1])<2:
        print('ERROR this script requires at minimum two full paths to images, you provided {}'.format(sys.argv[1]))
        sys.exit(1)
    else:
        brainlist=eval(sys.argv[1])
        print('brainlist is {}'.format(brainlist))
        for brain in brainlist:
            if not os.path.isfile(brain):
                print('ERROR, you must provide full paths to images, this path does not point to a real file \n {}'.format(brain))
                sys.exit(1)
            else:
                print('using brain {}'.format(brain))
        outputdir = sys.argv[2]
        if not os.path.isdir(outputdir):
            os.mkdir(outputdir)
            print('made outputdir')
        print('using outputdir: {}'.format(outputdir))
    if len(sys.argv) == 4:
        output_tiff = sys.argv[3]
        if not output_tiff[-4:]=='.tif':
            print('ERROR the output tiff string provided did not end in .tif, using default')
            output_tiff = 'result.tiff'
    else:
        output_tiff = 'result.tif'
    full_output_tiff = os.path.join(outputdir,output_tiff)

    print('will save to this file: {}'.format(full_output_tiff))

    sys.stdout.write("Collecting data and generating memory mapped array")
    sys.stdout.flush()


    vol = tif.imread(brainlist[0])
    z,y,x = vol.shape
    dtype = vol.dtype

    #init array
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    arr = load_memmap_arr(os.path.join(outputdir,'alltiffstogether_{}.npy'.format(timestamp)), mode="w+", shape = (len(brainlist),z,y,x), dtype = dtype)

    #load
    for i, brain in enumerate(brainlist):
        arr[i] = tif.imread(brain)
        print(np.max(arr[i]))
        arr[arr>65000]=0
        arr.flush()
    sys.stdout.write("...completed\nTaking median and saving as {}".format(output_tiff))
    sys.stdout.flush()

    #median volume
    vol = np.median(arr, axis=0)
    tif.imsave(full_output_tiff, vol.astype(dtype))
    sys.stdout.write("...completed")
    sys.stdout.flush()
