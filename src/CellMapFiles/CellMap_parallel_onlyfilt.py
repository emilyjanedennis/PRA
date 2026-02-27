#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CellMap
=======

This script is the main pipeline to analyze immediate early gene expression 
data from iDISCO+ cleared tissue [Renier2016]_.

See the :ref:`CellMap tutorial </CellMap.ipynb>` for a tutorial and usage.


.. image:: ../Static/cell_abstract_2016.jpg
   :target: https://doi.org/10.1016/j.cell.2020.01.028
   :width: 300

.. figure:: ../Static/CellMap_pipeline.png

  iDISCO+ and ClearMap: A Pipeline for Cell Detection, Registration, and 
  Mapping in Intact Samples Using Light Sheet Microscopy.


References
----------
.. [Renier2016] `Mapping of brain activity by automated volume analysis of immediate early genes. Renier* N, Adams* EL, Kirst* C, Wu* Z, et al. Cell. 2016 165(7):1789-802 <https://doi.org/10.1016/j.cell.2016.05.007>`_
"""
__author__    = 'Christoph Kirst <christoph.kirst.ck@gmail.com>'
__license__   = 'GPLv3 - GNU General Pulic License v3 (see LICENSE)'
__copyright__ = 'Copyright © 2020 by Christoph Kirst'
__webpage__   = 'http://idisco.info'
__download__  = 'http://www.github.com/ChristophKirst/ClearMap2'

if __name__ == "__main__":
     
  #%%############################################################################
  ### Initialization 
  ###############################################################################
  
  #%% Initialize workspace
  import sys, os, h5py
  import tifffile as tif
  import numpy as np
  import numpy.lib.recfunctions as rfn
  from datetime import datetime
  current_file_path=os.path.realpath(__file__)
  path_to_add=os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
  sys.path.append(path_to_add)
  from ClearMap.Environment import *  #analysis:ignore

  if len(sys.argv) == 2:
      directory = str(sys.argv[1])
      print('using directory: ',directory,' and expression str default: dataset.h5')
      expression_str = 'tiffs<Z,5>.tif'
      print('using expression str {}'.format(expression_str))
      expression_raw = expression_str
  else:
      print('ERROR: you must provide a directory and keyname to run this script!, you entered ',sys.argv)

  #directories and files
  subdirectory = os.path.join(directory,'tiffs')
  if not os.path.isdir(subdirectory):
      print('ERROR! tiffs must be generated BEFORE running this script')

  ws = wsp.Workspace('CellMap', directory=subdirectory);
  ws.update(raw=expression_raw)
  ws.update(stitched='stitched.npy')
  print(ws.info())
  
  #ws.debug = True
  
  resources_directory = settings.resources_path
  
  
  #%%############################################################################
  ### Data conversion
  ############################################################################### 
  
  #%% Convet raw data to npy file     
               
  thresholds = {
      'source' : 3,
      'size'   : (12,600)
      }
  
  cells.filter_cells(source = ws.filename('cells', postfix='raw'), 
                     sink = ws.filename('cells', postfix='filtered'), 
                     thresholds=thresholds);

  # save out params for reference later
  timestampstring=datetime.now().strftime("%Y%m%d")+"_"+datetime.now().strftime("%H%M%S")
  with open(os.path.join(directory,'params_{}.txt'.format(timestampstring)),"w") as file:
      file.write("cell detection parameters: \n")
      file.write(str(cell_detection_parameter))
      file.write("\n \n processing parameters: \n")
      file.write(str(processing_parameter))
      file.write("\n \n threshold parameters: \n")
      file.write(str(thresholds))
  file.close()

