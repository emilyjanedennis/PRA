
import os, sys, shutil, zarr
import numpy as np

if __name__ == "__main__":

  #%%############################################################################
  ### Initialization
  ###############################################################################

  #%% Initialize workspace

  if len(sys.argv) == 2:
    directory = sys.argv[1]
    zarrdir = os.path.join(directory,'fused.zarr')

    if not os.path.exists(os.path.join(directory,'tiffs','stitched.npy')):
        if not os.path.isdir(directory):
            print('ERROR directory is not a real directory, check your path: {}'.format(directory))
            sys.exit(1)
        print('using directory {}'.format(directory))
        failures=0
        if not os.path.isdir(zarrdir):
            print('ERROR directory does not contain fused.zarr, check your path! {}'.format(zarrdir))
            sys.exit(1)
        else:
            print('opening zarr')
            z1=zarr.open_array(os.path.join(directory,'fused.zarr','0'),'r')
            zlen = z1.shape[2]
            for i in np.arange(0,zlen):
                if not os.path.isfile(os.path.join(directory,'tiffs',f"tiffs{i:05d}.tif")):
                    print('ERROR: failed to find tiff num {}!'.format(i))
                    failures+=1
        if failures>0:
            sys.exit(1)
        else:
            print('found all expected tiffs! deleting zarr if it exists')
            if os.path.isdir(zarrdir):
	            subdirectory = shutil.rmtree(zarrdir)
    else:
        print('stitched.npy already exists! if you want to replace this, delete and re-run, else skipping this step')
