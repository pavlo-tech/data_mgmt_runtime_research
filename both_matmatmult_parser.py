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

Dir="./test_results/"+("tiled_" if tiled else "")+"matmatmult/"

cols=['tiled','tile_size','data_type','matrix_width','zfp_rate','cache_size','is_zfp',
	'Iteration','Time','RMSE']

def get_MATMATMULT_DataFrame(data_type, matrix_width, rate, cache_size, isZFP, tile_size):
	
	fname=Dir+(str(tile_size)+"/" if tiled else "")+data_type+"/"+str(matrix_width)+"/"+str(rate)+"/"+str(cache_size)+"/"+("tiled_" if tiled else "")+"matmatmult_"+("zfp_" if isZFP else "")+"output.txt"

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
						df = df.append(get_MATMATMULT_DataFrame(data_type, int(matrix_width), int(rate), int(cache_size), False, tile_size),\
							ignore_index=True)
						df = df.append(get_MATMATMULT_DataFrame(data_type, int(matrix_width), int(rate), int(cache_size), True, tile_size),\
							ignore_index=True)

else:	
	for data_type in os.listdir(Dir):
		for matrix_width in os.listdir(Dir+data_type+"/"):
			for rate in os.listdir(Dir+data_type+"/"+ matrix_width+"/"):
				for cache_size in os.listdir(Dir+data_type+"/"+ matrix_width+"/"+rate+"/"):
					df = df.append(get_MATMATMULT_DataFrame(data_type, int(matrix_width), int(rate), int(cache_size), False, 1),\
						ignore_index=True)
					df = df.append(get_MATMATMULT_DataFrame(data_type, int(matrix_width), int(rate), int(cache_size), True, 1),\
						ignore_index=True)

print df
df.to_csv(("tiled_" if tiled else "")+"matmatmult_df.csv")

exit()

'''
Max=True
#Max=False
size = 536870912 if Max else 1048576
streamd_size_B = size * 8
streamd_size_MB = streamd_size_B / (2**20)

df=STREAM_df.loc[(STREAM_df['is_zfp']) & (STREAM_df['data_type'] == 'double')	\
& (STREAM_df['stream_size']== size)]



#print df
t = df.loc[df['Function'] == 'Triad']
a = df.loc[df['Function'] == 'Add']
c = df.loc[df['Function'] == 'Copy']
s = df.loc[df['Function'] == 'Scale']

plt.figure()
#'''
plt.plot(c['zfp_rate'],streamd_size_MB/c['Avg time'],color=colors[0],label='Copy')
plt.plot(s['zfp_rate'],streamd_size_MB/s['Avg time'],color=colors[1],label='Scale') 
plt.plot(a['zfp_rate'],streamd_size_MB/a['Avg time'],color=colors[2],label='Add')
plt.plot(t['zfp_rate'],streamd_size_MB/t['Avg time'],color=colors[3],label='Triad')
'''
plt.plot(c['zfp_rate'],c['Best Rate MB/s'],color=colors[0],label='Copy')
plt.plot(s['zfp_rate'],s['Best Rate MB/s'],color=colors[1],label='Scale') 
plt.plot(a['zfp_rate'],a['Best Rate MB/s'],color=colors[2],label='Add')
plt.plot(t['zfp_rate'],t['Best Rate MB/s'],color=colors[3],label='Triad')
'''

print c

#plt.ylim(df['Avg time'].min(), df['Avg time'].max())
#plt.semilogy()
plt.xlim(2, 520)
plt.ylabel("Average Bandwidth (MB/s)", weight='bold')
plt.xlabel("ZFP Rate", weight='bold')
plt.title(str(streamd_size_MB) + " MB Stream")
plt.legend(loc='best', frameon=True, ncol=2, fontsize=12)
#plt.legend(loc='upper center', frameon=True, ncol=2, fontsize=12)
plt.tight_layout()

plt.savefig(("max" if Max else "min")+"_all.pdf")
plt.gcf().clear()


