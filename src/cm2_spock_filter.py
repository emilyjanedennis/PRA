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

import os
import sys
import tifffile as tif
import matplotlib.pyplot as plt
import numpy as np
import cv2
import pandas as pd
import matplotlib.colors

from matplotlib.backends.backend_pdf import PdfPages

sys.path.append("../ClearMap2")
from ClearMap.Environment import plt, reload, settings, io, wsp, tfs, p3d, col, te, tmr, bp, ap, ano, res, elx, st, stw, clp, rnk, se, dif, skl, skp, vf, me, mr, vox, cells

import ClearMap.IO.Workspace as wsp

dir = sys.argv[1]
brain = sys.argv[2]
source = int(sys.argv[3])
size1 = int(sys.argv[4])
size2 = int(sys.argv[5])
channel = sys.argv[6]

directory = os.path.join(dir, brain, channel)
ws = wsp.Workspace('CellMap', directory=directory);
thresholds = {
	'source' : source,
	'size'   : (size1,size2)
	}
cells.filter_cells(source = ws.filename('cells', postfix='raw'),
	sink = ws.filename('cells', postfix='{}_{}_filtered'.format(brain,channel)),
	thresholds=thresholds);
