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


cols=['tiled','tile_size','data_type','matrix_width','zfp_rate','cache_size','is_zfp',
	'Iteration','Time','RMSE']

df = pd.read_csv(("tiled_" if tiled else "")+"matmatmult_df.csv")

# RUNTIME VS PS for rate w/ reasonably low rmse (below 48)
# 1. characterize default performance
# 2. tuning determine run with lowest execution on a per accuracy basis
# 3. determine performance difference between 1 and 2.
# Need Paper-Ready Figures by Monday.


width=2048 #[1024, 128, 1536, 2048, 256, 32, 384, 512, 576, 768]  

uncompressed_df = df.loc[(df['is_zfp'] == False) & (df['data_type'] == 'double') & (df['matrix_width'] <= width)]
#print(uncompressed_df)
fig = sns.lineplot(x='matrix_width', y='Time', data=uncompressed_df, ci='sd')
plt.tight_layout()
#fig.get_figure().savefig("images/"+str(width)+("_tiled_uncompressed.pdf" if tiled else "_uncompressed.pdf"))
fig.get_figure().savefig("images/"+("tiled_uncompressed.pdf" if tiled else "uncompressed.pdf"))
plt.clf()

#rate = 64#[1, 16, 2,  32/ 4/  48/ 64/ 8/


for rate in df['zfp_rate'].unique():
	plt.clf()
	#default_df = df.loc[(df['is_zfp'] == True) & (df['data_type'] == 'double') & (df['matrix_width'] == width) &\
	default_df = df.loc[(df['is_zfp'] == True) & (df['data_type'] == 'double') & (df['matrix_width'] <= width) &\
		(df['zfp_rate'] == rate) & (df['cache_size'] == 0)]
	#print(default_df)
	fig = sns.lineplot(x='matrix_width', y='Time', data=default_df, ci='sd')
	plt.tight_layout()
	#fig.get_figure().savefig("images/"+str(width)+("_tiled_" if tiled else "_")+str(rate)+".pdf")
	fig.get_figure().savefig("images/"+("tiled_" if tiled else "")+str(rate)+".pdf")

rate=1
for width in df['matrix_width'].unique():
	plt.clf()
	best_df=df.loc[(df['is_zfp'] == True) & (df['data_type'] == 'double') & (df['matrix_width'] == width) &\
    (df['zfp_rate'] == rate)]
	#print(best_df)
	fig = sns.lineplot(x='cache_size', y='Time', data=best_df, ci='sd')
	plt.tight_layout()
	fig.get_figure().savefig("images/"+("tiled_" if tiled else "")+str(width)+"_"+str(rate)+".pdf")
	


'''
Max=True
#Max=False
size = 536870912 if Max else 1048576
streamd_size_B = size * 8
streamd_size_MB = streamd_size_B / (2**20)

df=STREAM_df.loc[(STREAM_df['is_zfp']) & (STREAM_df['data_type'] == 'double')	\
& (STREAM_df['stream_size']== size)]
'''

'''

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

'''
