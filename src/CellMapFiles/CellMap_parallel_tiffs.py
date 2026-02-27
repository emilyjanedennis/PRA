#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

if __name__ == "__main__":
     
  
  #%% Initialize workspace
  import sys, os, zarr, h5py
  import tifffile as tif
  import numpy as np

  if len(sys.argv) <3:
      print('ERROR: you entered {} and we require three strings: a directory, expression_raw string, and chunk name'.format(len(sys.argv)))
  else:
      directory = str(sys.argv[1]); print('using directory: ',directory)
      expression_raw = str(sys.argv[2]); print('using expression str',expression_raw)
      keyval = str(sys.argv[3]);print('using chunk ',keyval,' for vals ',int(keyval)*100)
      keyintval = int(keyval)*100

  #directories and files
  subdirectory = os.path.join(directory,'tiffs')
  print(os.path.isdir(subdirectory))

  if not os.path.isdir(subdirectory):
      try:
          os.mkdir(subdirectory)
      except:
          if os.path.isdir(subdirectory):
              print('tried making directory, but failed, likely made by another process')
          else:
              print('tried making direcotry {}, failed, unsure why'.format(subdirectory))
              sys.exit(1)
  # get the number of tiffs (z planes) for each key
  if str.split(expression_raw,'.')[1] == 'h5':
      print('converting h5 to tiffs for processing')
      with h5py.File(os.path.join(directory,expression_raw),'r') as infile:
          shapeval=0
          shapelist=[0]
          keylist=[key for key in infile.keys() if 's' in key]
          for key in keylist:
              dset=infile['t00000'][key]['0']['cells']
              dtype=dset.dtype
              shapeval+=int(dset.shape[0])
              shapelist.append(shapeval)

          # we want to start the tiff number
          start=shapelist[keyintval]
          dset = infile['t00000'][keyval]['0']['cells']
          print('on key ',keyval)
          for dsetstart in range(0,dset.shape[0]):
                  if start%1000==0:
                      print('on tiff',start)
                  if not os.path.isfile(os.path.join(subdirectory,f"tiffs{start:05d}.tif")):
                  #if not os.path.isfile(os.path.join(subdirectory,f"{keyval}_tiffs{start:05d}.tif")):
                      tif.imsave(os.path.join(subdirectory,f"tiffs{start:05d}.tif"),np.squeeze(dset[dsetstart:dsetstart+1]))
                  start+=1
  elif str.split(expression_raw,'.')[1] == 'zarr':
          z1=zarr.open_array(os.path.join(directory,expression_raw,'0'),'r')
          for val in np.arange(keyintval,keyintval+100):
              if os.path.isfile(os.path.join(subdirectory,f"tiffs{val:05d}.tif")):
                  os.remove(os.path.join(subdirectory,f"tiffs{val:05d}.tif"))
              tif.imsave(os.path.join(subdirectory,f"tiffs{val:05d}.tif"),np.squeeze(z1[:,:,val,:,:]))
              print('max ',np.max(np.squeeze(z1[:,:,val,:,:])))
          print('done with tiffs {} to {}'.format(keyintval,keyintval+100))
  else:
      print('{} did not end in zarr nor h5, do not know how to process. edit ClearMap2/ClearMap/Scripts/CellMap_parallel_tiffs.py to fix'.format(expression_raw))
