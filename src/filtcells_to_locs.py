#!/usr/bin/env python3
"""
created 20250204
@author emilyjanedennis
PURPOSE
INPUTS
OPTIONAL INPUTS
OUTPUTS
"""

import os,sys,h5py
import numpy as np
import pandas as pd

if __name__ == "__main__":


	#first, deal with inputs
	if len(sys.argv) < 2:
		print('this requires at minimum one input: a full path to a folder with a tiffs/cells_filtered.py file. \n you entered {}'.format(sys.argv))
	else:
		filepath=os.path.join(sys.argv[1],"tiffs/cells_filtered.npy")
		print('working on {}'.format(filepath))

	try:
		cells = np.load(filepath)
	except:
		if os.path.isfile(sys.argv[1]):
			print('cannot open file, check filepath: {}'.format(filepath))
		else:
			print('full path does not lead to a file, check filepath: {}'.format(filepath))
			sys.exit(1)

	print('max dims are: {}x {}y {}z'.format(np.max(cells['x']),np.max(cells['y']),np.max(cells['z'])))
	df_cells = pd.DataFrame(cells[['x','y','z']])
	print('done making dataframe of length {}'.format(len(df_cells)))
	directory=os.path.dirname(os.path.dirname(filepath))
	outputdir = os.path.join(directory,'outputs')
	if not os.path.isdir(outputdir):
		os.mkdir(outputdir)
		print('made output dir')
	output_file = os.path.join(outputdir,'filtered_cells.csv')
	print('trying to save as output file {}'.format(output_file))
	df_cells.to_csv(output_file,header=False,index=False)
