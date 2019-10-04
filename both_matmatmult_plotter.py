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

sns.set_context("notebook", font_scale=1.25, rc={"lines.linewidth": 2.5, 'lines.markeredgewidth': 1., 'lines.markersize': 10})
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
df['FLOPS']= (2 * df['matrix_width']**3) / (df['Time'])
df['Megaflops']=df['FLOPS']/2**20

# RUNTIME VS PS for rate w/ reasonably low rmse (below 48)
# 1. characterize default performance
# 2. tuning determine run with lowest execution on a per accuracy basis
# 3. determine performance difference between 1 and 2.
# Need Paper-Ready Figures by Monday.

width=1024 #[1024, 128, 1536, 2048, 256, 32, 384, 512, 576, 768]  
#rate = 64#[1, 16, 2,  32/ 4/  48/ 64/ 8/

if tiled:
	df= pd.read_csv("tiled_matmatmult_df.csv")
	df['FLOPS']= (2 * df['matrix_width']**3) / (df['Time'])
	df['Megaflops']=df['FLOPS']/2**20
	df=df.loc[(df['tile_size']==32) & (df['is_zfp'] == True) & (df['data_type'] == 'double')]
	#print(df)
	default_cache_df = pd.read_csv('default_cache_sizes.csv')	

	for width in [1024]:
		plt.clf()
		#for rate in df['zfp_rate'].unique():
		for rate in [4, 8, 16, 32]:
			best_df=df.loc[(df['is_zfp'] == True) & (df['data_type'] == 'double') & (df['matrix_width'] == width) &\
    		(df['zfp_rate'] == rate)]#& (df['cache_size'] >= 2**13)]
			#print(best_df)
			default_cache_size=default_cache_df.loc[(default_cache_df['matrix_wdith'] == width) & (default_cache_df['rate']==4)]['cache_size']
			default_cache_flops=df.loc[(df['is_zfp'] == True) & (df['data_type'] == 'double') & (df['matrix_width'] == width) &(df['zfp_rate'] == rate)& (df['cache_size'] == default_cache_size.values[0])]['Megaflops'].mean()
			if rate==4:
				print(best_df['Megaflops'].max())
			#print(default_cache_flops)
			#best_df['cache_size_kb']=best_df['cache_size']/2**10
			fig = sns.lineplot(x='cache_size', y='Megaflops', data=best_df, ci='sd', label="Rate = "+str(rate))
			#plt.scatter(default_cache_size, default_cache_flops, marker='x', s=100,edgecolors='w')
		plt.axvline(x=default_cache_size.values[0], color='k', linestyle='--', label='Default Cache Size')

		#plt.ylim(10,50)
		ax = plt.gca()
		ax.set_xscale('log', basex=2)	
		plt.legend()
		plt.title("Performance vs Cache Size\n(n="+str(width)+")")
		plt.ylabel('MegaFlop/s')
		plt.xlabel('Direct Mapped Cache Size (Bytes)')
		plt.tight_layout()
		#fig.get_figure().savefig("images/fasthash_FLOPS_v_cacheSize_Width_"+str(width)+".pdf")
		fig.get_figure().savefig("images/tiled_FLOPS_v_cacheSize_Width_"+str(width)+".pdf")

else:
	uncompressed_df = df.loc[(df['is_zfp'] == False) & (df['data_type'] == 'double') & (df['matrix_width'] <= width)]
	#print(uncompressed_df)
	fig = sns.lineplot(x='matrix_width', y='FLOPS', data=uncompressed_df, ci='sd')
	plt.tight_layout()
	#fig.get_figure().savefig("images/"+str(width)+("_tiled_uncompressed.pdf" if tiled else "_uncompressed.pdf"))
	fig.get_figure().savefig("images/uncompressed.pdf")
	plt.clf()


	for rate in df['zfp_rate'].unique():
		plt.clf()
		#default_df = df.loc[(df['is_zfp'] == True) & (df['data_type'] == 'double') & (df['matrix_width'] == width) &\
		default_df = df.loc[(df['is_zfp'] == True) & (df['data_type'] == 'double') & (df['matrix_width'] <= width) &\
		(df['zfp_rate'] == rate) & (df['cache_size'] == 0)]
		#print(default_df)
		fig = sns.lineplot(x='matrix_width', y='FLOPS', data=default_df, ci='sd')
		plt.tight_layout()
		#fig.get_figure().savefig("images/"+str(width)+("_tiled_" if tiled else "_")+str(rate)+".pdf")
		fig.get_figure().savefig("images/"+("tiled_" if tiled else "")+str(rate)+".pdf")

	#df = pd.read_csv("fasthash_matmatmult_df.csv")
	#df['FLOPS']= (2 * df['matrix_width']**3) / (df['Time'])
	#df['Megaflops']=df['FLOPS']/2**20
	default_cache_df = pd.read_csv('default_cache_sizes.csv')	
	for width in default_cache_df.loc[(default_cache_df['matrix_wdith'] >32)]['matrix_wdith'].unique():
		plt.clf()
		#for rate in df['zfp_rate'].unique():
		for rate in [4, 8, 16, 32, 48]:
			best_df=df.loc[(df['is_zfp'] == True) & (df['data_type'] == 'double') & (df['matrix_width'] == width) &\
    		(df['zfp_rate'] == rate)& (df['cache_size'] >= 2**13)]
			#print(best_df)
			best_df['cache_size_kb']=best_df['cache_size']/2**10
			df['cache_size_kb']=df['cache_size']/2**10

			default_cache_size=default_cache_df.loc[(default_cache_df['matrix_wdith'] == width) & (default_cache_df['rate']==4)]['cache_size']/2**10
			default_cache_flops=df.loc[(df['is_zfp'] == True) & (df['data_type'] == 'double') & (df['matrix_width'] == width) &(df['zfp_rate'] == rate)& (df['cache_size_kb'] == default_cache_size.values[0])]['Megaflops'].mean()
			
			#if width == 1024:
			for cs in best_df['cache_size'].unique():
				x=best_df.loc[best_df['cache_size']==cs]['Megaflops'].mean()
				if x-default_cache_flops > 0:
					#print(x)
					#print("width="+str(width)+"  rate="+str(rate)+" cs="+str(cs/2**10)+" Mflop improvement(%)="+str((x-default_cache_flops)/default_cache_flops))
					print("width="+str(width)+"  rate="+str(rate)+" cs="+str(cs/2**10)+" Mflops="+str(x))
			fig = sns.lineplot(x='cache_size_kb', y='Megaflops', data=best_df, ci='sd', label="Rate = "+str(rate))
			#plt.scatter(default_cache_size, default_cache_flops, marker='x', s=100,edgecolors='w')
		plt.axvline(x=default_cache_size.values[0], color='k', linestyle='--', label='Default Cache Size')

		#plt.ylim(10,50)
		ax = plt.gca()
		ax.set_xscale('log', basex=2)	
		#plt.legend(title="ZFP Rate")
		plt.legend()
		plt.title("Performance vs Cache Size\n(n="+str(width)+")")
		plt.ylabel('MegaFlop/s')
		plt.xlabel('Direct Mapped Cache Size (Kilobytes)')
		plt.tight_layout()
		#fig.get_figure().savefig("images/fasthash_FLOPS_v_cacheSize_Width_"+str(width)+".pdf")
		fig.get_figure().savefig("images/FLOPS_v_cacheSize_Width_"+str(width)+".pdf")
	



untiled_df = pd.read_csv("matmatmult_df.csv")
untiled_df['FLOPS']= (2 * untiled_df['matrix_width']**3) / (untiled_df['Time'])
untiled_df['Megaflops']=untiled_df['FLOPS']/2**20

tiled_df = pd.read_csv("tiled_matmatmult_df.csv")
tiled_df['FLOPS']= (2 * tiled_df['matrix_width']**3) / (tiled_df['Time'])
tiled_df['Megaflops']=tiled_df['FLOPS']/2**20


bar_width = 0.25
colors = ["b", "r", "c", "m", "g"]
opacity = 1
#widths=[512, 768, 1024]
widths=[256, 512, 1024]
rates=[4, 8, 16, 32, 48]
'''
for cache_size in untiled_df['cache_size'].unique():
	plt.clf()
	for iw, width in enumerate(widths):
		
		#plot uncompressed nontiled
		ucBar_pos=iw*(1+ 2*len(rates))*bar_width
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
'''

