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


tiled = len(sys.argv) > 1 and sys.argv[1] == "tiled"
print("tiled" if tiled else "not tiled")


cols=['tiled','tile_size','data_type','matrix_width','zfp_rate','cache_size','is_zfp',
	'Iteration','Time','RMSE']


default_df = pd.read_csv("matmatmult_df.csv")
fast_df = pd.read_csv("fasthash_matmatmult_df.csv")
cachesizes_df=pd.read_csv('default_cache_sizes.csv')


default_df = default_df.loc[(default_df['is_zfp']) & (default_df['data_type'] =='double') & (default_df['cache_size'] == 0) &\
	( 128 < default_df['matrix_width']) & (default_df['matrix_width'] <= 1024) & (default_df['Time'] > 0)]
default_df = default_df.groupby(['tiled','tile_size','data_type','matrix_width','zfp_rate','cache_size','is_zfp'], as_index=False)['Time'].mean()


fast_df=fast_df.loc[(fast_df['is_zfp']) & (fast_df['data_type'] =='double') &\
  ( 128 < fast_df['matrix_width']) & (fast_df['matrix_width'] <= 1024) & (fast_df['Time'] > 0)] #& (fast_df['tile_size'] == 32)]






print(default_df)
#print(fast_df)

# finds best config possible for fast_hash data
best_config_df=pd.DataFrame(columns=cols)
for matrix_width in fast_df['matrix_width'].unique():
	for zfp_rate in fast_df.loc[fast_df['matrix_width'] == matrix_width]['zfp_rate'].unique():
		subset_df=fast_df.loc[(fast_df['matrix_width'] == matrix_width) & (fast_df['zfp_rate'] == zfp_rate)]
		subset_df=subset_df.groupby(['tiled','tile_size','data_type','matrix_width','zfp_rate','cache_size','is_zfp'], as_index=False)['Time'].mean()
		#print (subset_df)
		best_config_df=best_config_df.append(subset_df.loc[subset_df['Time'].idxmin()], ignore_index=True)

#print(best_config_df)


#finds best config possible for fast_hash data with default cache size
fast_defaultcache_df=fast_df.loc[fast_df['cache_size'] == 0]
cols.append('actual_cache_size')
bettercache_df=pd.DataFrame(columns=cols)
for matrix_width in fast_defaultcache_df['matrix_width'].unique():
	for zfp_rate in fast_defaultcache_df.loc[fast_defaultcache_df['matrix_width'] == matrix_width]['zfp_rate'].unique():
		subset_df=fast_defaultcache_df.loc[(fast_defaultcache_df['matrix_width'] == matrix_width) & (fast_defaultcache_df['zfp_rate'] == zfp_rate)]
		subset_df=subset_df.groupby(['tiled','tile_size','data_type','matrix_width','zfp_rate','cache_size','is_zfp'], as_index=False)['Time'].mean()
		subset_df=subset_df.loc[subset_df['Time'].idxmin()]
		#x=cachesizes_df.loc[(cachesizes_df['matrix_wdith']==matrix_width) & (cachesizes_df['rate']==zfp_rate)]['cache_size']
		#actual_cache_size= x.values[0] if len(x) > 0 else 0
		#print(actual_cache_size)
		#subset_df['actual_cache_size']=actual_cache_size
		bettercache_df=bettercache_df.append(subset_df, ignore_index=True)

print(bettercache_df)

improvement_cols=['matrix_width','zfp_rate','original_time','tiled_fasthash_time','tile_size','cache_size']
improvement_df=pd.DataFrame(columns=improvement_cols)
for w in [256,384,512,768,1024]:
	for r in [1,2,4,8,16,32]:
		newrow={}
		newrow['matrix_width']=w
		newrow['zfp_rate']=r
		newrow['original_time']=default_df.loc[(default_df['matrix_width'] == w) & (default_df['zfp_rate'] == r)]['Time'].values[0]
		fastrow=bettercache_df.loc[(bettercache_df['matrix_width'] == w) & (bettercache_df['zfp_rate'] == r)]
		newrow['tiled_fasthash_time']=fastrow['Time'].values[0]
		newrow['tile_size']=fastrow['tile_size'].values[0]
		#newrow['cache_size']=fastrow['actual_cache_size'].values[0]
		print(newrow)
		improvement_df=improvement_df.append(newrow, ignore_index=True) 

improvement_df['speedup']=improvement_df['original_time']/improvement_df['tiled_fasthash_time']
print(improvement_df)


bar_width=.1
widths=[256,384,512,768,1024]
rates=[4,8,16,32]
index = np.arange(len(widths))
for ri,r in enumerate(rates):
	data=improvement_df.loc[improvement_df['zfp_rate']==r]
	x=data['matrix_width'].values
	y=data['speedup'].values
	plt.bar(index+bar_width*ri,y,bar_width,label=r)
plt.ylim(0,1.5)
plt.title('Speedup Using Simple Hash')
plt.axhline(y=1.0,color='k')
plt.xticks(index + bar_width, (widths))
plt.legend(title='ZFP Rate',loc='upper center',ncol=len(rates),fontsize='x-small')
plt.ylabel('Speedup')
plt.xlabel('n')
plt.tight_layout()
plt.savefig('images/fasthash_speedup.pdf')

plt.clf()
bar_width=.1
widths=[256,384,512,768,1024]
rates=[1,2,4,8,16,32]
index = np.arange(len(rates))
for wi,w in enumerate(widths):
	data=improvement_df.loc[improvement_df['matrix_width']==w]
	y=data['speedup'].values
	plt.bar(index+bar_width*wi,y,bar_width,label=w)
plt.ylim(1,1.2)
plt.xticks(index + bar_width, (rates))
plt.legend(title='n')
plt.tight_layout()
plt.savefig('images/improvement_alternate_xaxis.pdf')

exit(0)
for w in [256,384,512,768,1024]:
	ax=sns.lineplot(x='zfp_rate',y='speedup',data=improvement_df.loc[improvement_df['matrix_width']==w],label=w)
ax.get_figure().savefig('images/improvement.pdf')














	


