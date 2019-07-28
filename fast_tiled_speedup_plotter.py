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
untiled_df = untiled_df.loc[untiled_df['Time'] >0]
tiled_df = pd.read_csv("tiled_matmatmult_df.csv")
fast_df = pd.read_csv("fast_matmatmult_df.csv")
fast_df=fast_df.loc[fast_df['is_fast'] == True]

bar_width = 0.25
colors = ["c", "y", "b", "r", "g","m"]
opacity = 1
#widths=[512, 768, 1024]
widths=[2**7, 2**8, 2**9, 2**10]
#widths=[256, 512, 1024]
rates=[1, 2, 4, 8, 16, 32]
tile_size=32
for cache_size in [0]:
	plt.clf()
	xticks=[]
	for iw, width in enumerate(widths):
		for ir, rate in enumerate(rates):
			tiled_time = tiled_df.loc[(tiled_df['data_type'] == 'double') & (tiled_df['tiled'] == True ) & (tiled_df['cache_size'] == cache_size) &\
				(tiled_df['matrix_width'] == width) & (tiled_df['zfp_rate'] == rate) &(tiled_df['tile_size'] == tile_size)]['Time'].mean()
			zfp_time = untiled_df.loc[(untiled_df['is_zfp'] == True) & (untiled_df['data_type'] == 'double') & (untiled_df['cache_size'] == cache_size) &\
        (untiled_df['matrix_width'] == width) & (untiled_df['zfp_rate'] == rate)]['Time'].mean()
			tiled_speedup=zfp_time/tiled_time

			xpos=(iw * (2*len(rates) + 1.5) + ir) * bar_width
			#print(xpos)
			plt.bar(xpos, tiled_speedup, bar_width, color=colors[ir],hatch='//')
			
		for ir, rate in enumerate(rates):
			fast_time=fast_df.loc[(fast_df['data_type']=='double') & (fast_df['cache_size']== cache_size) & (fast_df['matrix_width'] == width) &\
				(fast_df['zfp_rate'] == rate)]['Time'].mean()
			zfp_time = untiled_df.loc[(untiled_df['is_zfp'] == True) & (untiled_df['data_type'] == 'double') & (untiled_df['cache_size'] == cache_size) &\
        (untiled_df['matrix_width'] == width) & (untiled_df['zfp_rate'] == rate)]['Time'].mean()
			fast_speedup=zfp_time/fast_time
			print(str(width)+" "+str(rate)+" "+str(fast_speedup))
			xpos=(iw * (2*len(rates) +1.5 ) +len(rates) + ir) * bar_width
			plt.bar(xpos, fast_speedup, bar_width, color=colors[ir])

		xticks.append((iw * (2*len(rates) + 1.5)  + (iw+1) * (2*len(rates)) )*bar_width/2)
	plt.xticks(xticks, widths)

	plt.ylim(1, 12)
	x=plt.bar(0,0,0,color='w',edgecolor='k',hatch='//', label='Tiled')
	#y=plt.bar(0,0,0,color='w',edgecolor='k',hatch='x', label='Tiled')
	legend = [mpl.patches.Patch(color=colors[i], label=r) for i,r in enumerate(rates)]
	legend.extend([x])
	plt.legend(handles=legend, ncol=3)
	plt.ylabel('Speedup over Original ZFP')
	plt.xlabel('n')
	plt.tight_layout()
	plt.savefig("images/speedup_barchart_"+str(cache_size)+"tile_"+str(tile_size)+".pdf") 
exit()
'''
	plt.semilogy(basey=10)
	plt.ylabel('Megaflop/s')
	plt.savefig("images/barchart_"+str(cache_size)+".pdf")			
'''

