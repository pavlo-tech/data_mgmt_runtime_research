import numpy as np
import os
import sys
import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
sns.set_style("whitegrid", {'axes.grid' : True})
sns.set_color_codes()
sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5, 'lines.markeredgewidth': 1., 'lines.markersize': 10})
font = {'family' : 'serif'}
mpl.rc('font', **font)
mpl.rcParams['ps.useafm'] = True
mpl.rcParams['pdf.use14corefonts'] = True




cols=['tiled','tile_size','data_type','matrix_width','zfp_rate','cache_size','is_zfp',
	'Iteration','Time','RMSE']


default_df = pd.read_csv("tiled_matmatmult_df.csv")
fast_df = pd.read_csv("twoway_tiled_matmatmult_df.csv")
cachesizes_df=pd.read_csv('default_cache_sizes.csv')


default_df = default_df.loc[\
	(default_df['is_zfp']) &\
	(default_df['data_type'] =='double') &\
	(default_df['cache_size'] == 0) &\
	( 128 < default_df['matrix_width']) & (default_df['matrix_width'] <= 1024) &\
	(default_df['Time'] > 0) &\
	(default_df['tile_size']==32)]

#print(default_df)
default_df = default_df.groupby(['tiled','tile_size','data_type','matrix_width','zfp_rate','cache_size','is_zfp'], as_index=False)['Time'].mean()


fast_df=fast_df.loc[\
	(fast_df['is_zfp']) &\
	(fast_df['data_type'] =='double') &\
	(fast_df['cache_size'] == 0) &\
  ( 128 < fast_df['matrix_width']) & (fast_df['matrix_width'] <= 1024) &\
	(fast_df['Time'] > 0) &\
	(fast_df['tile_size'] == 32)]



#print(fast_df)
widths=[256,384,512,1024]
#widths=[1024]
rates=[4,8,16,32]



cols.append('actual_cache_size')
bettercache_df=pd.DataFrame(columns=cols)
for matrix_width in widths:
	for zfp_rate in rates:
		subset_df=fast_df.loc[(fast_df['matrix_width'] == matrix_width) & (fast_df['zfp_rate'] == zfp_rate)]
		subset_df=subset_df.groupby(['tiled','tile_size','data_type','matrix_width','zfp_rate','cache_size','is_zfp'], as_index=False)['Time'].mean()
		#print(subset_df)
		subset_df=subset_df.loc[subset_df['Time'].idxmin()]
		bettercache_df=bettercache_df.append(subset_df, ignore_index=True)

#print(bettercache_df)

improvement_cols=['matrix_width','zfp_rate','original_time','tiled_fasthash_time','tile_size','cache_size']
improvement_df=pd.DataFrame(columns=improvement_cols)
for w in widths:
	for r in rates:
		newrow={}
		newrow['matrix_width']=w
		newrow['zfp_rate']=r
		newrow['original_time']=default_df.loc[(default_df['matrix_width'] == w) & (default_df['zfp_rate'] == r)]['Time'].values[0]
		fastrow=bettercache_df.loc[(bettercache_df['matrix_width'] == w) & (bettercache_df['zfp_rate'] == r)]
		newrow['tiled_fasthash_time']=fastrow['Time'].values[0]
		newrow['tile_size']=fastrow['tile_size'].values[0]
		newrow['cache_size']=fastrow['actual_cache_size'].values[0]
		#print(newrow)
		improvement_df=improvement_df.append(newrow, ignore_index=True) 

improvement_df['speedup']=improvement_df['original_time']/improvement_df['tiled_fasthash_time']
#print(improvement_df)


bar_width=.1
widths=[256,384,512,1024]
rates=[4,8,16,32]
print("speedup="+str(np.mean(improvement_df['speedup'])))
index = np.arange(len(widths))
for ri,r in enumerate(rates):
	data=improvement_df.loc[improvement_df['zfp_rate']==r]
	x=data['matrix_width'].values
	y=data['speedup'].values
	plt.bar(index+bar_width*ri,y,bar_width,label=r)
plt.ylim(0.9,1.1)
plt.title('Speedup Using Two-way Skew-Associative Cache')
plt.axhline(y=1.0,color='k')
plt.xticks(index + bar_width, (widths))
plt.legend(title='ZFP Rate',loc='upper center',ncol=len(rates),fontsize='x-small')
plt.ylabel('Speedup')
plt.xlabel('n')
plt.tight_layout()
plt.savefig('images/tiled_twoway_speedup.pdf')

