import numpy as np
import os
import sys
from os import path
import pandas as pd
import re

# file paths in form of:
# test_results/spmv/DEFAULT/double/ASIC_680k/8/0/zfp_output.txt 


Dir='./test_results/spmv/'

cols=['cache_policy','data_type','matrix_name','zfp_rate','cache_size','is_zfp', 'Iteration','Time','Norm']

def get_DataFrame(cache_policy,data_type, matrix_name, rate, cache_size, isZFP):
	
	fname=Dir+cache_policy+'/'+ data_type+'/'+matrix_name+'/'+str(rate)+"/"+str(cache_size)+"/"+("zfp_output.txt" if isZFP else "output.txt")

	if path.exists(fname) == False or os.stat(fname).st_size == 0:
		print(fname)
		df = pd.DataFrame(columns=cols)
	else:	
		df = pd.read_csv(fname)
		df['cache_policy']=cache_policy
		df['data_type']=data_type
		df['matrix_name']=matrix_name
		df['zfp_rate']=rate
		df['cache_size']=cache_size
		df['is_zfp']=isZFP
		#print df

	return df

# create DateFrame to hold all Results
df = pd.DataFrame(columns=cols)

for cache_policy in os.listdir(Dir):
	for data_type in os.listdir(Dir+cache_policy+'/'):
		for matrix in os.listdir(Dir+cache_policy+'/'+data_type+'/'):
			for rate in os.listdir(Dir+cache_policy+'/'+data_type+'/'+ matrix+'/'):
				for cache_size in os.listdir(Dir+cache_policy+'/'+data_type+'/'+ matrix+'/'+rate+'/'):
					#print(Dir+data_type+"/"+ matrix_width+"/"+rate+"/"+cache_size)
					row = get_DataFrame(cache_policy, data_type, matrix, int(rate), int(cache_size), False)
					df = df.append(row, ignore_index=True)
					row = get_DataFrame(cache_policy, data_type, matrix, int(rate), int(cache_size), True)
					df = df.append(row, ignore_index=True)

print( df)
fname="spmv_df.csv"
print(fname)
df.to_csv(fname)

exit()

