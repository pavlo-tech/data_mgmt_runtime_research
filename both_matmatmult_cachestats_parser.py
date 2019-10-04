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

Dir="./old_machine_test_results/"+("tiled_" if tiled else "")+"matmatmult_cachestats"

cols=['tiled','tile_size','data_type','matrix_width','zfp_rate','hash_algorithm','cache_size',
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
	


def get_MATMATMULT_DataFrame(data_type, matrix_width, rate, cache_size, isFat, isTwo):
	if isFat and isTwo:
		raise Exception("Invalid input!")

	if isFat:
		fname=Dir+"_fat/"+data_type+"/"+str(matrix_width)+"/"+str(rate)+"/"+str(cache_size)+"/matmatmult_zfp_output.txt"
	elif isTwo:
		fname=Dir+"_twoway/"+data_type+"/"+str(matrix_width)+"/"+str(rate)+"/"+str(cache_size)+"/matmatmult_zfp_output.txt"
	else:
		fname=Dir+"/"+data_type+"/"+str(matrix_width)+"/"+str(rate)+"/"+str(cache_size)+"/matmatmult_zfp_output.txt"

	if path.exists(fname) == False or os.stat(fname).st_size == 0:
		print("SKIPPING: "+fname)
		df = pd.DataFrame(columns=cols)
	else:	
		print(fname)
		df=parse_cachestats(fname)
		df['tiled']=tiled
		df['tile_size']=(32 if tiled else 0)
		df['data_type']=data_type
		df['matrix_width']=matrix_width
		df['zfp_rate']=rate
		df['cache_size']=cache_size
		df['hash_algorithm']=('fat'if isFat else ('twoway'if isTwo else 'default'))
	return df

# create DateFrame to hold all Results
df = pd.DataFrame(columns=cols)

if tiled:
	for data_type in os.listdir(Dir+"/"):
		for matrix_width in os.listdir(Dir+"/"+data_type+"/"):
			for rate in os.listdir(Dir+"/"+data_type+"/"+ matrix_width+"/"):
				for cache_size in os.listdir(Dir+"/"+data_type+"/"+ matrix_width+"/"+rate+"/"):
					row1 = get_MATMATMULT_DataFrame(data_type, int(matrix_width), int(rate), int(cache_size), True, False)
					row2 = get_MATMATMULT_DataFrame(data_type, int(matrix_width), int(rate), int(cache_size), False, True)
					row3 = get_MATMATMULT_DataFrame(data_type, int(matrix_width), int(rate), int(cache_size), False, False)
					df = df.append(row1,ignore_index=True)
					df = df.append(row2,ignore_index=True)
					df = df.append(row3,ignore_index=True)

else:	
	for data_type in os.listdir(Dir+"/"):
		for matrix_width in os.listdir(Dir+"/"+data_type+"/"):
			for rate in os.listdir(Dir+"/"+data_type+"/"+ matrix_width+"/"):
				for cache_size in os.listdir(Dir+"/"+data_type+"/"+ matrix_width+"/"+rate+"/"):
					row1 = get_MATMATMULT_DataFrame(data_type, int(matrix_width), int(rate), int(cache_size), True, False)
					row2 = get_MATMATMULT_DataFrame(data_type, int(matrix_width), int(rate), int(cache_size), False, True)
					row3 = get_MATMATMULT_DataFrame(data_type, int(matrix_width), int(rate), int(cache_size), False, False)
					df = df.append(row1, ignore_index=True)
					df = df.append(row2, ignore_index=True)
					df = df.append(row3, ignore_index=True)

#print( df)
df['hit rate']=df['hits']/(df['hits'] + df['misses'])
df['miss rate']=df['misses']/(df['hits'] + df['misses'])
fname=("tiled_" if tiled else "")+"matmatmult_cachestats_df.csv"
print( df)
print(fname)
df.to_csv(fname)

exit()

