import numpy as np
import os
import sys
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

#read in and prep data
fname=("tiled_" if tiled else "")+"matmatmult_cachestats_df.csv"
df = pd.read_csv(fname)
widths=[254,512,1024]
rates=[4,8,16,32]
cache_sizes=[2048,4096,8192,16384]
colors=['r','c','g','b']
df=df.loc[(254 <= df['matrix_width']) & (df['matrix_width']<=1024)]

index = np.arange(len(widths))
if tiled:
	df=df.loc[df['tile_size']==32]


# visualize
df=df.loc[df['matrix_width']==1024]
default=df.loc[df['hash_algorithm'] == 'default']
fat=df.loc[df['hash_algorithm'] == 'fat']
twoway=df.loc[df['hash_algorithm'] == 'twoway']

#cs,dt,mw,ts constant
print("ZFP Rate,Default Hash Hit-Rate,Two-way Hit-Rate,Fast And Two-Way Hit-Rate")
for rate in rates:
	default_hr=default.loc[default['zfp_rate']==rate]['hit rate'].values[0]*100
	twoway_hr=twoway.loc[twoway['zfp_rate']==rate]['hit rate'].values[0]*100
	fat_hr=fat.loc[fat['zfp_rate']==rate]['hit rate'].values[0]*100
	print(str(rate)+","+str(default_hr)+","+str(twoway_hr)+","+str(fat_hr))
exit()


