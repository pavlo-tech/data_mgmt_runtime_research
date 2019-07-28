import numpy as np
import os
import sys
import pandas as pd



#fixed datatype, tilesize, and cachesize
cols=['matrix_width','zfp_rate','hitrate_improvement', 'missrate_reduction']

tiled_df=pd.read_csv("tiled_matmatmult_cachestats_df.csv")
tiled_df=tiled_df.loc[(tiled_df['tile_size']==32) & (tiled_df['cache_size']==0)]

untiled_df=pd.read_csv("matmatmult_cachestats_df.csv")
untiled_df=untiled_df.loc[(untiled_df['cache_size']==0)]

print(tiled_df)
print(untiled_df)

#computes best possible cache_size for each configuration

improve_df=pd.DataFrame(columns=cols)
for matrix_width in tiled_df['matrix_width'].unique():
	for zfp_rate in tiled_df['zfp_rate'].unique():
		tiled=tiled_df.loc[(tiled_df['matrix_width'] == matrix_width) & (tiled_df['zfp_rate'] ==  zfp_rate)]
		untiled=untiled_df.loc[(untiled_df['matrix_width'] == matrix_width) & (untiled_df['zfp_rate'] ==  zfp_rate)]

		thr=tiled['hit rate'].values[0]
		tmr=tiled['miss rate'].values[0]
		uhr=untiled['hit rate'].values[0]
		umr=untiled['miss rate'].values[0]


		improve_df= improve_df.append([{'matrix_width':matrix_width,'zfp_rate':zfp_rate,\
			'hitrate_improvement': 100*(thr - uhr) / uhr,\
			'missrate_reduction':100*(umr - tmr) / umr}], ignore_index=True)
print(improve_df)
improve_df.to_csv("hit_miss_improvement_df.csv")
'''
#q = df.loc[(df['is_zfp'] == True) & (df['data_type'] == 'double') & (df['matrix_width'] == 2048) & (df['zfp_rate'] == 8)]
#print(q)

# RUNTIME VS PS for rate w/ reasonably low rmse (below 48)
# 1. characterize default performance
# 2. tuning determine run with lowest execution on a per accuracy basis
# 3. determine performance difference between 1 and 2.
# Need Paper-Ready Figures by Monday.
'''



	


