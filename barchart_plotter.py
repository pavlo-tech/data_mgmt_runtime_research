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



sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5, 'lines.markeredgewidth': 1., 'lines.markersize': 10})
#'''

# axis labels
font = {'family' : 'serif'}
mpl.rc('font', **font)
mpl.rcParams['ps.useafm'] = True
mpl.rcParams['pdf.use14corefonts'] = True


cols=['tiled','tile_size','data_type','matrix_width','zfp_rate','cache_size','is_zfp',
	'Iteration','Time','RMSE']


untiled_df = pd.read_csv("matmatmult_df.csv")
untiled_df['FLOPS']= (2 * untiled_df['matrix_width']**3) / (untiled_df['Time'])
untiled_df['Megaflops']=untiled_df['FLOPS']/2**20

tiled_df = pd.read_csv("tiled_matmatmult_df.csv")
tiled_df['FLOPS']= (2 * tiled_df['matrix_width']**3) / (tiled_df['Time'])
tiled_df['Megaflops']=tiled_df['FLOPS']/2**20


bar_width = 0.25
colors = ["b", "r", "c", "m", "g"]
opacity = 1
widths=[512, 768, 1024]
#widths=[256, 512, 1024]
rates=[4, 8, 16, 32, 48]

for cache_size in [0]:
	plt.clf()
	for iw, width in enumerate(widths):
		
		#plot uncompressed nontiled
		ucBar_pos=iw*(1+ 2*len(rates)+ 2 )*bar_width
		mflops=untiled_df.loc[(untiled_df['is_zfp'] == False) & (untiled_df['data_type'] == 'double') & (untiled_df['tiled'] == False) & (untiled_df['matrix_width'] == width)]['Megaflops'].mean()
		plt.bar(ucBar_pos, mflops, bar_width, color="k")
	

		for ir, rate in enumerate(rates):
			untiled_mflops=untiled_df.loc[(untiled_df['is_zfp'] == True) & (untiled_df['data_type'] == 'double') & (untiled_df['tiled'] == False) &\
				(untiled_df['cache_size'] == cache_size) & (untiled_df['matrix_width'] == width) & (untiled_df['zfp_rate'] == rate)]['Megaflops'].mean()
			plt.bar(ucBar_pos + (ir+1)*bar_width, untiled_mflops, bar_width, color=colors[ir])
			
		for ir, rate in enumerate(rates):
			tiled_mflops=tiled_df.loc[(tiled_df['is_zfp'] == True) & (tiled_df['data_type'] == 'double') & (tiled_df['tiled'] == True ) &\
				(tiled_df['cache_size'] == cache_size) & (tiled_df['tile_size'] == 64) & (tiled_df['matrix_width'] == width) & (tiled_df['zfp_rate'] == rate)]['Megaflops'].mean()
			plt.bar(ucBar_pos +(len(rates) +ir+1)*bar_width, tiled_mflops, bar_width, color=colors[ir],hatch='//')

		plt.savefig("images/barchart_"+str(cache_size)+".pdf")			


