import numpy as np
import os
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


sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5, 'lines.markeredgewidth': 1., 'lines.markersize': 10})
#'''

# axis labels
import matplotlib
colors = ["b", "g", "r", "y", "m"]
font = {'family' : 'serif'}
matplotlib.rc('font', **font)
matplotlib.rcParams['ps.useafm'] = True
matplotlib.rcParams['pdf.use14corefonts'] = True


cols=['data_type','stream_size','zfp_rate','cache_size','is_zfp',
	'Function','Best Rate MB/s', 'Avg time', 'Min time','Max time']


def get_STREAM_DataFrame(data_type, stream_size, rate, cache_size, isZFP):

	stream_fname="./test_results/STREAM/"+data_type+"/"+ \
		str(stream_size)+"/"+str(rate)+"/"+str(cache_size)+"/stream_output.txt"
	zfp_fname="./test_results/STREAM/"+data_type+"/"+ \
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
				row.extend(re.findall(r"[A-Za-z]+", line))
				row.extend(map(float,re.findall(r"[\d\.]+", line)))
				
				new_row=pd.DataFrame([row],columns=cols)

				df=df.append(new_row,ignore_index=True)

	return df

# create DateFrame to hold all of STREAM Results
STREAM_df = pd.DataFrame(columns=cols)

for data_type in os.listdir("./test_results/STREAM/"):
	for stream_size in os.listdir("./test_results/STREAM/"+data_type+"/"):
		for rate in os.listdir("./test_results/STREAM/"+data_type+"/"+ str(stream_size)+"/"):

			cache_size=0

			STREAM_df = \
				STREAM_df.append(get_STREAM_DataFrame(data_type, int(stream_size), int(rate), int(cache_size), False),\
					ignore_index=True)
			STREAM_df = \
				STREAM_df.append(get_STREAM_DataFrame(data_type, int(stream_size), int(rate), int(cache_size), True),\
					ignore_index=True)

#print STREAM_df
STREAM_df.to_csv("new_STREAM_df.csv")


Max=True
#Max=False
size = 536870912 if Max else 1048576
streamd_size_B = size * 8
streamd_size_MB = streamd_size_B / (2**20)

df=STREAM_df.loc[(STREAM_df['is_zfp']) & (STREAM_df['data_type'] == 'double')	\
& (STREAM_df['stream_size']== size)]



#print df
t = df.loc[df['Function'] == 'Triad']
a = df.loc[df['Function'] == 'Add']
c = df.loc[df['Function'] == 'Copy']
s = df.loc[df['Function'] == 'Scale']

plt.figure()
#'''
plt.plot(c['zfp_rate'],streamd_size_MB/c['Avg time'],color=colors[0],label='Copy')
plt.plot(s['zfp_rate'],streamd_size_MB/s['Avg time'],color=colors[1],label='Scale') 
plt.plot(a['zfp_rate'],streamd_size_MB/a['Avg time'],color=colors[2],label='Add')
plt.plot(t['zfp_rate'],streamd_size_MB/t['Avg time'],color=colors[3],label='Triad')
'''
plt.plot(c['zfp_rate'],c['Best Rate MB/s'],color=colors[0],label='Copy')
plt.plot(s['zfp_rate'],s['Best Rate MB/s'],color=colors[1],label='Scale') 
plt.plot(a['zfp_rate'],a['Best Rate MB/s'],color=colors[2],label='Add')
plt.plot(t['zfp_rate'],t['Best Rate MB/s'],color=colors[3],label='Triad')
'''

print c

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


