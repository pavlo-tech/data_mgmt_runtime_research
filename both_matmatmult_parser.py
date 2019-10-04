import numpy as np
import os
import sys
from os import path
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import re

#'''
import seaborn as sns
sns.set()
sns.set_style("whitegrid", {'axes.grid' : True})
sns.set_color_codes()
#sns.set_style("white")

tiled = len(sys.argv) > 1 and sys.argv[1] == "tiled"
print("tiled" if tiled else "not tiled")

fast=len(sys.argv) > 2 and sys.argv[2] == "FAST"
print("FAST_HASH" if fast else "not fast")

twoway=len(sys.argv) > 2 and sys.argv[2] == "TWOWAY"
print("TWOWAY" if twoway else "not twoway")

fat=len(sys.argv) > 2 and sys.argv[2] == "FAT"
print("FAST_AND_TWOWAY" if fat else "not fast and twoway")

sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5, 'lines.markeredgewidth': 1., 'lines.markersize': 10})
#'''

# axis labels
import matplotlib
colors = ["b", "g", "r", "y", "m"]
font = {'family' : 'serif'}
matplotlib.rc('font', **font)
matplotlib.rcParams['ps.useafm'] = True
matplotlib.rcParams['pdf.use14corefonts'] = True

Dir="./test_results/"+("tiled_" if tiled else "")+"matmatmult/"+("FAST_HASH/" if fast else ("TWOWAY/" if twoway else("FAST_AND_TWOWAY/"if fat else"DEFAULT/")))

cols=['tiled','tile_size','data_type','matrix_width','zfp_rate','cache_size','is_zfp',
	'Iteration','Time','RMSE']

def get_MATMATMULT_DataFrame(data_type, matrix_width, rate, cache_size, isZFP, tile_size):
	
	fname=Dir+(str(tile_size)+"/" if tiled else "")+data_type+"/"+str(matrix_width)+"/"+str(rate)+"/"+str(cache_size)+"/"+("tiled_" if tiled else "")+"matmatmult_"+("zfp_" if isZFP else "")+"output.txt"

	print(fname)
	if path.exists(fname) == False or os.stat(fname).st_size == 0:
		df = pd.DataFrame(columns=cols)
	else:	
		df = pd.read_csv(fname)
		df['tiled']=tiled
		df['tile_size']=tile_size
		df['data_type']=data_type
		df['matrix_width']=matrix_width
		df['zfp_rate']=rate
		df['cache_size']=cache_size
		df['is_zfp']=isZFP
		#print df

	return df

# create DateFrame to hold all Results
df = pd.DataFrame(columns=cols)

if tiled:
	for tile_size in os.listdir(Dir):
		for data_type in os.listdir(Dir+tile_size+"/"):
			for matrix_width in os.listdir(Dir+tile_size+"/"+data_type+"/"):
				for rate in os.listdir(Dir+tile_size+"/"+data_type+"/"+ matrix_width+"/"):
					for cache_size in os.listdir(Dir+tile_size+"/"+data_type+"/"+ matrix_width+"/"+rate+"/"):
						row = get_MATMATMULT_DataFrame(data_type, int(matrix_width), int(rate), int(cache_size), False, tile_size)
						df = df.append(row,ignore_index=True)
						row = get_MATMATMULT_DataFrame(data_type, int(matrix_width), int(rate), int(cache_size), True, tile_size)
						df = df.append(row,ignore_index=True)

else:	
	for data_type in os.listdir(Dir):
		for matrix_width in os.listdir(Dir+data_type+"/"):
			for rate in os.listdir(Dir+data_type+"/"+ matrix_width+"/"):
				for cache_size in os.listdir(Dir+data_type+"/"+ matrix_width+"/"+rate+"/"):
					#print(Dir+data_type+"/"+ matrix_width+"/"+rate+"/"+cache_size)
					row = get_MATMATMULT_DataFrame(data_type, int(matrix_width), int(rate), int(cache_size), False, 1)
					df = df.append(row, ignore_index=True)
					row = get_MATMATMULT_DataFrame(data_type, int(matrix_width), int(rate), int(cache_size), True, 1)
					df = df.append(row, ignore_index=True)

print( df)
fname=("fasthash_" if fast else ("twoway_" if twoway else("fat_"if fat else"")))+("tiled_" if tiled else "")+"matmatmult_df.csv"
print(fname)
df.to_csv(fname)

exit()

