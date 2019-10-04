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


sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5, 'lines.markeredgewidth': 1., 'lines.markersize': 10})
#'''

# axis labels
import matplotlib
colors = ["b", "g", "r", "y", "m"]
font = {'family' : 'serif'}
matplotlib.rc('font', **font)
matplotlib.rcParams['ps.useafm'] = True
matplotlib.rcParams['pdf.use14corefonts'] = True

Dir="./old_machine_test_results/"+("tiled_" if tiled else "")+"matmatmult/"

cols=['tiled','tile_size','data_type','matrix_width','zfp_rate','cache_size',
	'hits','misses','write backs']

def parse_cachestats(fname):
	with open(fname) as f:
		#cache R1=2096128 R2=0 RM=1024 RB=0 W1=15360 W2=0 WM=1024 WB=1024
		hits=0; misses=0; write_backs=0
		for line in f:
			if 'cache R1' in line:
				for s in line.split():
					if '=' in s:
						num = int(s.split('=')[1])
						if 'B' in s:
							write_backs += num
						elif 'M' in s:
							misses += num
						else:
							hits += num
	#if hits is 0 and misses is 0:
	#	return pd.DataFrame(columns=cols)

	return pd.DataFrame([{'hits':hits, 'misses':misses,'write backs':write_backs}])
	


def get_MATMATMULT_DataFrame(data_type, matrix_width, rate, cache_size, isZFP, tile_size):
	
	fname=Dir+(str(tile_size)+"/" if tiled else "")+data_type+"/"+str(matrix_width)+"/"+str(rate)+"/"+str(cache_size)+"/"+("tiled_" if tiled else "")+"matmatmult_"+("zfp_" if isZFP else "")+"output.txt"

	if path.exists(fname) == False or os.stat(fname).st_size == 0:
		df = pd.DataFrame(columns=cols)
	else:	
		df=parse_cachestats(fname)
		df['tiled']=tiled
		df['tile_size']=tile_size
		df['data_type']=data_type
		df['matrix_width']=matrix_width
		df['zfp_rate']=rate
		df['cache_size']=cache_size

	return df

# create DateFrame to hold all Results
df = pd.DataFrame(columns=cols)

if tiled:
	for tile_size in os.listdir(Dir):
		for data_type in os.listdir(Dir+tile_size+"/"):
			for matrix_width in os.listdir(Dir+tile_size+"/"+data_type+"/"):
				for rate in os.listdir(Dir+tile_size+"/"+data_type+"/"+ matrix_width+"/"):
					for cache_size in os.listdir(Dir+tile_size+"/"+data_type+"/"+ matrix_width+"/"+rate+"/"):
						row = get_MATMATMULT_DataFrame(data_type, int(matrix_width), int(rate), int(cache_size), True, tile_size)
						df = df.append(row,ignore_index=True)

else:	
	for data_type in os.listdir(Dir):
		for matrix_width in os.listdir(Dir+data_type+"/"):
			for rate in os.listdir(Dir+data_type+"/"+ matrix_width+"/"):
				for cache_size in os.listdir(Dir+data_type+"/"+ matrix_width+"/"+rate+"/"):
					row = get_MATMATMULT_DataFrame(data_type, int(matrix_width), int(rate), int(cache_size), True, 1)
					df = df.append(row, ignore_index=True)

#print( df)
df['hit rate']=df['hits']/(df['hits'] + df['misses'])
df['miss rate']=df['misses']/(df['hits'] + df['misses'])
print( df)
df.to_csv(("tiled_" if tiled else "")+"matmatmult_cachestats_df.csv")

exit()
