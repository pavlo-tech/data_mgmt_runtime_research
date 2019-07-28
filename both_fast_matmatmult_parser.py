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


sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5, 'lines.markeredgewidth': 1., 'lines.markersize': 10})
#'''

# axis labels
import matplotlib
colors = ["b", "g", "r", "y", "m"]
font = {'family' : 'serif'}
matplotlib.rc('font', **font)
matplotlib.rcParams['ps.useafm'] = True
matplotlib.rcParams['pdf.use14corefonts'] = True

Dir="./test_results/FAST_matmatmult/"

cols=['data_type','matrix_width','zfp_rate','cache_size','is_zfp',
	'Iteration','Time','RMSE']

def get_MATMATMULT_DataFrame(data_type, matrix_width, rate, cache_size, isZFP, is_fast):
	fname=Dir+data_type+"/"+str(matrix_width)+"/"+str(rate)+"/"+str(cache_size)+"/"+(("fast_" if is_fast else "slow_") if isZFP else "")+"matmatmult_"+("zfp_" if isZFP else "")+"output.txt"

	if path.exists(fname) == False or os.stat(fname).st_size == 0:
		df = pd.DataFrame(columns=cols)
	else:	
		df = pd.read_csv(fname)
		df['data_type']=data_type
		df['matrix_width']=matrix_width
		df['zfp_rate']=rate
		df['cache_size']=cache_size
		df['is_zfp']=isZFP
		df['is_fast']=is_fast
		#print df

	return df

# create DateFrame to hold all Results
df = pd.DataFrame(columns=cols)


for data_type in os.listdir(Dir):
	for matrix_width in os.listdir(Dir+data_type+"/"):
		for rate in os.listdir(Dir+data_type+"/"+ matrix_width+"/"):
			for cache_size in os.listdir(Dir+data_type+"/"+ matrix_width+"/"+rate+"/"):
				row = get_MATMATMULT_DataFrame(data_type, int(matrix_width), int(rate), int(cache_size), False, False)
				df = df.append(row, ignore_index=True)
				row = get_MATMATMULT_DataFrame(data_type, int(matrix_width), int(rate), int(cache_size), True, False)
				df = df.append(row, ignore_index=True)
				row = get_MATMATMULT_DataFrame(data_type, int(matrix_width), int(rate), int(cache_size), True, True)
				df = df.append(row, ignore_index=True)

print( df)
df.to_csv("fast_matmatmult_df.csv")

exit()

