import numpy as np
import os
import sys
import pandas as pd


tiled = len(sys.argv) > 1 and sys.argv[1] == "tiled"
print("tiled" if tiled else "not tiled")


cols=['tiled','tile_size','data_type','matrix_width','zfp_rate','cache_size','is_zfp',
	'Iteration','Time','RMSE']

df = pd.read_csv(("tiled_" if tiled else "")+"matmatmult_df.csv")

q = df.loc[(df['is_zfp'] == True) & (df['data_type'] == 'double') & (df['matrix_width'] == 2048) & (df['zfp_rate'] == 8)]

print(q)

# RUNTIME VS PS for rate w/ reasonably low rmse (below 48)
# 1. characterize default performance
# 2. tuning determine run with lowest execution on a per accuracy basis
# 3. determine performance difference between 1 and 2.
# Need Paper-Ready Figures by Monday.




	


