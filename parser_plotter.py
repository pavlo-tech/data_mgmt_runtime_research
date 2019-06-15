import numpy as np
import os
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import re

'''
import seaborn as sns
sns.set()
sns.set_style("whitegrid", {'axes.grid' : True})
sns.set_color_codes()
#sns.set_style("white")


sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5, 'lines.markeredgewidth': 1., 'lines.markersize': 10})
'''

# axis labels
import matplotlib
color = ["b", "g", "r", "y", "m"]
font = {'family' : 'serif'}
matplotlib.rc('font', **font)
matplotlib.rcParams['ps.useafm'] = True
matplotlib.rcParams['pdf.use14corefonts'] = True


cols=['data_type','stream_size','zfp_rate','cache_size','is_zfp',
	'Function','Best Rate MB/s', 'Avg time', 'Min time','Max time']


def get_STREAM_DataFrame(data_type, stream_size, rate, cache_size, isZFP):

	stream_fname="./old_test_results/STREAM/"+data_type+"/"+ \
		str(stream_size)+"/"+str(rate)+"/"+str(cache_size)+"/stream_output.txt"
	zfp_fname="./old_test_results/STREAM/"+data_type+"/"+ \
		str(stream_size)+"/"+str(rate)+"/"+str(cache_size)+"/zfp_output.txt"


	df = pd.DataFrame(columns=cols)

	at_grid=False
	with open(zfp_fname if isZFP else stream_fname) as f:
		for line in f.readlines():
			if "Function" in line:
				at_grid = True
				ct=0

			elif at_grid and ct < 4:
				ct += 1

				row=[data_type,stream_size,rate,cache_size,isZFP]
				row.extend(re.findall(r"[A-Za-z]+|[\d\.]+", line))
				new_row=pd.DataFrame([row],columns=cols)

				df=df.append(new_row,ignore_index=True)

	return df

# create DateFrame to hold all of STREAM Results
STREAM_df = pd.DataFrame(columns=cols)

for data_type in os.listdir("./old_test_results/STREAM/"):
	for stream_size in os.listdir("./old_test_results/STREAM/"+data_type+"/"):
		for rate in os.listdir("./old_test_results/STREAM/"+data_type+"/"+ str(stream_size)+"/"):

			cache_size=0

			STREAM_df = \
				STREAM_df.append(get_STREAM_DataFrame(data_type, stream_size, rate, cache_size, False),ignore_index=True)
			STREAM_df = \
				STREAM_df.append(get_STREAM_DataFrame(data_type, stream_size, rate, cache_size, True),ignore_index=True)

#print STREAM_df
STREAM_df.to_csv("STREAM_df.csv")



