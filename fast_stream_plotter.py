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


#print STREAM_df
STREAM_df=pd.read_csv("fast_STREAM_df.csv")




Max=True
#Max=False
size = 536870912 if Max else 1048576
streamd_size_B = size * 8
streamd_size_MB = streamd_size_B / (2**20)

STREAM_df['AvgBW'] = streamd_size_MB / STREAM_df['Avg time']
STREAM_df['MaxRate']=streamd_size_MB / STREAM_df['Min time']
STREAM_df['MinRate']=streamd_size_MB / STREAM_df['Max time']
df=STREAM_df.loc[(STREAM_df['is_zfp'] == True) & (STREAM_df['data_type'] == 'double')	\
& (STREAM_df['is_fast'] == False)
& (STREAM_df['zfp_rate'] <= 64) \
& (STREAM_df['stream_size']== size)]

STREAM_df=pd.read_csv("fast_STREAM_df.csv")
STREAM_df['AvgBW'] = streamd_size_MB / STREAM_df['Avg time']
STREAM_df['MaxRate']=streamd_size_MB / STREAM_df['Min time']
STREAM_df['MinRate']=streamd_size_MB / STREAM_df['Max time']
df2=STREAM_df.loc[(STREAM_df['is_zfp'] == False) & (STREAM_df['data_type'] == 'double') \
& (STREAM_df['zfp_rate'] <= 64) \
& (STREAM_df['stream_size']== size)]

STREAM_df=pd.read_csv("fast_STREAM_df.csv")
STREAM_df['AvgBW'] = streamd_size_MB / STREAM_df['Avg time']
STREAM_df['MaxRate']=streamd_size_MB / STREAM_df['Min time']
STREAM_df['MinRate']=streamd_size_MB / STREAM_df['Max time']
df3=STREAM_df.loc[(STREAM_df['is_zfp'] == True) & (STREAM_df['data_type'] == 'double')	\
& (STREAM_df['is_fast'] == True)
& (STREAM_df['zfp_rate'] <= 64) \
& (STREAM_df['stream_size']== size)]


#print df
t = df.loc[df['Function'] == 'Triad']
a = df.loc[df['Function'] == 'Add']
c = df.loc[df['Function'] == 'Copy']
s = df.loc[df['Function'] == 'Scale']

t2 = df2.loc[df2['Function'] == 'Triad']
a2 = df2.loc[df2['Function'] == 'Add']
c2 = df2.loc[df2['Function'] == 'Copy']
s2 = df2.loc[df2['Function'] == 'Scale']

t3 = df3.loc[df3['Function'] == 'Triad']
a3 = df3.loc[df3['Function'] == 'Add']
c3 = df3.loc[df3['Function'] == 'Copy']
s3 = df3.loc[df3['Function'] == 'Scale']


plt.figure()

plt.fill_between(c['zfp_rate'],c['MinRate'],c['MaxRate'],color=colors[0], alpha=.3)
plt.plot(c['zfp_rate'],streamd_size_MB/c['Avg time'],color=colors[0],label='Copy-ZFP', linestyle=':')
plt.fill_between(s['zfp_rate'],s['MinRate'],s['MaxRate'],color=colors[1], alpha=.3)
plt.plot(s['zfp_rate'],streamd_size_MB/s['Avg time'],color=colors[1],label='Scale-ZFP', linestyle=':') 
plt.fill_between(a['zfp_rate'],a['MinRate'],a['MaxRate'],color=colors[2], alpha=.3)
plt.plot(a['zfp_rate'],streamd_size_MB/a['Avg time'],color=colors[2],label='Add-ZFP', linestyle=':')
plt.fill_between(t['zfp_rate'],t['MinRate'],t['MaxRate'],color=colors[3], alpha=.3)
plt.plot(t['zfp_rate'],streamd_size_MB/t['Avg time'],color=colors[3],label='Triad-ZFP', linestyle=':')

plt.fill_between(c2['zfp_rate'],c2['MinRate'],c2['MaxRate'],color=colors[0], alpha=.3)
plt.plot(c2['zfp_rate'],streamd_size_MB/c2['Avg time'],color=colors[0],label='Copy', linestyle='-')
plt.fill_between(s2['zfp_rate'],s2['MinRate'],s2['MaxRate'],color=colors[1], alpha=.3)
plt.plot(s2['zfp_rate'],streamd_size_MB/s2['Avg time'],color=colors[1],label='Scale', linestyle='-') 
plt.fill_between(a2['zfp_rate'],a2['MinRate'],a2['MaxRate'],color=colors[2], alpha=.3)
plt.plot(a2['zfp_rate'],streamd_size_MB/a2['Avg time'],color=colors[2],label='Add', linestyle='-')
plt.fill_between(t2['zfp_rate'],t2['MinRate'],t2['MaxRate'],color=colors[3], alpha=.3)
plt.plot(t2['zfp_rate'],streamd_size_MB/t2['Avg time'],color=colors[3],label='Triad', linestyle='-')

plt.fill_between(c3['zfp_rate'],c3['MinRate'],c3['MaxRate'],color=colors[0], alpha=.3)
plt.plot(c3['zfp_rate'],streamd_size_MB/c3['Avg time'],color=colors[0],label='Copy-Fast', linestyle='-.')
plt.fill_between(s3['zfp_rate'],s3['MinRate'],s3['MaxRate'],color=colors[1], alpha=.3)
plt.plot(s3['zfp_rate'],streamd_size_MB/s3['Avg time'],color=colors[1],label='Scale-Fast', linestyle='-.') 
plt.fill_between(a3['zfp_rate'],a3['MinRate'],a3['MaxRate'],color=colors[2], alpha=.3)
plt.plot(a3['zfp_rate'],streamd_size_MB/a3['Avg time'],color=colors[2],label='Add-Fast', linestyle='-.')
plt.fill_between(t3['zfp_rate'],t3['MinRate'],t3['MaxRate'],color=colors[3], alpha=.3)
plt.plot(t3['zfp_rate'],streamd_size_MB/t3['Avg time'],color=colors[3],label='Triad-Fast', linestyle='-.')



plt.yscale('log')
plt.xlim(2, 65)
plt.ylabel("Average Bandwidth (MB/s)", weight='bold')
plt.xlabel("Bits Per Value", weight='bold')
#plt.title(str(streamd_size_MB) + " MB Stream")
plt.legend(loc='best', frameon=True, ncol=2, fontsize=12)
plt.tight_layout()

plt.savefig("images/"+("max" if Max else "min")+"_"+str(size)+"_.pdf")
plt.gcf().clear()


