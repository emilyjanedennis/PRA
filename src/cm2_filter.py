#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created Jan 2021

@author: ejdennis

file takes 6 arguments
1 - directory where brain(s) live
2 - brainname
3 - source value (suggest 3 if at princeton using smartspim)
4 - size 1 value (suggest 30 if at princeton using smartspim)
5 - size 2 value (suggest 120 if at princeton using smartspim)
6 - channel "cell" or "reg"
"""

import os, sys, glob, cv2
import tifffile as tif
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.colors
import warnings
warnings.filterwarnings("ignore")

from matplotlib.backends.backend_pdf import PdfPages

sys.path.append("../ClearMap2")
from ClearMap.Environment import plt, reload, settings, io, wsp, tfs, p3d, col, te, tmr, bp, ap, ano, res, elx, st, stw, clp, rnk, se, dif, skl, skp, vf, me, mr, vox, cells
#from ClearMap.Environment import cells, wsp

import ClearMap.IO.Workspace as wsp

print("sys argvs are:")
print(sys.argv)

dir = sys.argv[1]
brain = sys.argv[2]
source = int(sys.argv[3])
size1 = int(sys.argv[4])
size2 = int(sys.argv[5])
channel = sys.argv[6]

if "reg" in channel:
	ch = glob.glob(os.path.join(dir,brain,"*488"))[0].split('/')[-1]
	print("reg channel is {}".format(ch))
elif "cell" in channel:
	ch = glob.glob(os.path.join(dir,brain,"*642"))[0].split('/')[-1]
	print("cell ch is {}".format(ch))
else:
	print("ERROR: unknown channel {}".format(channel))

directory = os.path.join(dir, brain, ch)
ws = wsp.Workspace('CellMap', directory=directory);

thresholds = {
	'source' : source,
	'size'   : (size1,size2)
	}

print("PRINTING WS INFO")
ws.info()

cells.filter_cells(source = ws.filename('cells', postfix='raw'),
	sink = ws.filename('cells', postfix='filt'),
	thresholds=thresholds);

os.rename(os.path.join(directory,"cells_filt.npy"),os.path.join(directory,"{}_{}_filt.npy".format(brain,ch)))
