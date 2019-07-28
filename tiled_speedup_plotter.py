import numpy as np
import os
import sys
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import re
import seaborn as sns


sns.set()
sns.set_style("whitegrid", {'axes.grid' : True})
sns.set_color_codes()
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5, 'lines.markeredgewidth': 1., 'lines.markersize': 10})
colors = ["b", "g", "r", "y", "m"]
font = {'family' : 'serif'}
mpl.rc('font', **font)
mpl.rcParams['ps.useafm'] = True
mpl.rcParams['pdf.use14corefonts'] = True



cols=['tiled','tile_size','data_type','matrix_width','zfp_rate','cache_size','is_zfp',
	'Iteration','Time','RMSE']


df = pd.read_csv("tiled_matmatmult_df.csv")
df['FLOPS']= (2 * df['matrix_width']**3) / (df['Time'])
df['Megaflops']=df['FLOPS']/2**20



#computes best possible cache_size for each configuration
zfp_df = df.loc[(df['is_zfp'] == True) & (df['data_type'] == 'double') & (df['matrix_width'] <= 2048) & (df['Time'] > 0)]
best_runs_df=pd.DataFrame(columns=['tile_size','matrix_width','zfp_rate','cache_size','Time'])
for tile_size in zfp_df['tile_size'].unique():
	for matrix_width in zfp_df['matrix_width'].unique():
		for zfp_rate in zfp_df['zfp_rate'].unique():
			index = zfp_df.loc[(tile_size == zfp_df['tile_size']) & (matrix_width == zfp_df['matrix_width']) & (zfp_rate == zfp_df['zfp_rate'])]
			index = index.groupby(['tile_size','matrix_width','zfp_rate','cache_size'], as_index=False)['Time'].mean()
			min_time=index['Time'].min()
			best_run=index.loc[index['Time'] == min_time]
			best_runs_df=best_runs_df.append(best_run, ignore_index=True)
#print(best_runs_df)
best_unique_times_df = best_runs_df[['tile_size','matrix_width','zfp_rate','Time']].drop_duplicates()
#print(best_unique_times_df)


# get timing for all values with default cache size
df = pd.read_csv("matmatmult_df.csv")
df['FLOPS']= (2 * df['matrix_width']**3) / (df['Time'])
df['Megaflops']=df['FLOPS']/2**20
zeroCache_times_df=df.loc[(df['is_zfp'] == True) & (df['data_type'] == 'double') & (df['matrix_width'] <= 2048) & (df['Time'] > 0) & (df['cache_size'] == 0)][['tile_size','matrix_width','zfp_rate','Time']]
zeroCache_times_df=zeroCache_times_df.groupby(['tile_size','matrix_width','zfp_rate'], as_index=False)['Time'].mean()
#print(zeroCache_times_df)


# i will need to figure out these later, for now I loop
#allVals = pd.concat([best_unique_times_df,zeroCache_times_df],join='inner',join_axes=['tile_size','matrix_width','zfp_rate'])
#allVals = pd.merge(best_unique_times_df,zeroCache_times_df,how='left',left_on=['tile_size','matrix_width','zfp_rate','Time'], right_on=['tile_size','matrix_width','zfp_rate','Time'])
allVals = pd.DataFrame(columns=['tile_size','matrix_width','zfp_rate','Best Time', 'Default Cache Time'])
for index, row in best_unique_times_df.iterrows():
	if zeroCache_times_df[(zeroCache_times_df['matrix_width'] == row['matrix_width']) & (zeroCache_times_df['zfp_rate'] == row['zfp_rate'])]['Time'].empty is False:
		allVals = allVals.append({
			'tile_size':row['tile_size'],
			'matrix_width':row['matrix_width'],
			'zfp_rate':row['zfp_rate'],
			'Best Time':row['Time'],
			'Default Cache Time':zeroCache_times_df[(zeroCache_times_df['matrix_width'] == row['matrix_width']) & (zeroCache_times_df['zfp_rate'] == row['zfp_rate'])]['Time'].values[0]
		},ignore_index=True)
allVals['Speedup'] = allVals['Default Cache Time'] / allVals['Best Time']
print(allVals)

for tile_size in [16,32]:#allVals['tile_size'].unique():
	plt.clf()
	#for rate in [4, 8, 16, 32, 48]:
	for rate in [1, 2, 4, 8, 16, 32, 48]:
		data=allVals[(allVals['zfp_rate'] == rate) & (allVals['matrix_width'] <= 2000) & (allVals['tile_size'] == tile_size)]
		#print(data)

		sns.lineplot(x='matrix_width',y='Speedup',data=data, ci='sd', label=str(rate))
	plt.semilogx(basex=2)
	plt.ylabel('Speedup over Default ZFP')
	plt.xlabel('n')
	plt.tight_layout()
	plt.savefig("images/tiled"+str(tile_size)+"_Speedup.pdf")

#q = df.loc[(df['is_zfp'] == True) & (df['data_type'] == 'double') & (df['matrix_width'] == 2048) & (df['zfp_rate'] == 8)]
#print(q)

# RUNTIME VS PS for rate w/ reasonably low rmse (below 48)
# 1. characterize default performance
# 2. tuning determine run with lowest execution on a per accuracy basis
# 3. determine performance difference between 1 and 2.
# Need Paper-Ready Figures by Monday.




	


