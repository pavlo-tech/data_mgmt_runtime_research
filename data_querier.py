import numpy as np
import os
import sys
import pandas as pd


tiled = len(sys.argv) > 1 and sys.argv[1] == "tiled"
print("tiled" if tiled else "not tiled")


cols=['tiled','tile_size','data_type','matrix_width','zfp_rate','cache_size','is_zfp',
	'Iteration','Time','RMSE']

df = pd.read_csv(("tiled_" if tiled else "")+"matmatmult_df.csv")



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

print(best_runs_df)

#q = df.loc[(df['is_zfp'] == True) & (df['data_type'] == 'double') & (df['matrix_width'] == 2048) & (df['zfp_rate'] == 8)]
#print(q)

# RUNTIME VS PS for rate w/ reasonably low rmse (below 48)
# 1. characterize default performance
# 2. tuning determine run with lowest execution on a per accuracy basis
# 3. determine performance difference between 1 and 2.
# Need Paper-Ready Figures by Monday.




	


