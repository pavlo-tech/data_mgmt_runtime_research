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
STREAM_df=pd.read_csv("STREAM_df.csv")




Max=True
#Max=False
size = 536870912 if Max else 1048576
streamd_size_B = size * 8
streamd_size_MB = streamd_size_B / (2**20)

STREAM_df['AvgBW'] = streamd_size_MB / STREAM_df['Avg time']
STREAM_df['MaxRate']=streamd_size_MB / STREAM_df['Min time']
STREAM_df['MinRate']=streamd_size_MB / STREAM_df['Max time']

df=STREAM_df.loc[(STREAM_df['is_zfp'] == True) & (STREAM_df['data_type'] == 'double')	\
& (STREAM_df['zfp_rate'] <= 64) \
& (STREAM_df['stream_size']== size)]

STREAM_df=pd.read_csv("STREAM_df.csv")
STREAM_df['AvgBW'] = streamd_size_MB / STREAM_df['Avg time']
STREAM_df['MaxRate']=streamd_size_MB / STREAM_df['Min time']
STREAM_df['MinRate']=streamd_size_MB / STREAM_df['Max time']
df2=STREAM_df.loc[(STREAM_df['is_zfp'] == False) & (STREAM_df['data_type'] == 'double') \
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



plt.figure()

plt.plot(c['zfp_rate'],streamd_size_MB/c['Avg time'],color=colors[0],label='Copy-ZFP', linestyle=':')
y=streamd_size_MB/c.loc[c['zfp_rate'] == 4]['Avg time'].values[0]
plt.plot([1,2,4], [y,y,y], color=colors[0], linestyle=':')

plt.plot(s['zfp_rate'],streamd_size_MB/s['Avg time'],color=colors[1],label='Scale-ZFP', linestyle=':') 
y=streamd_size_MB/s.loc[s['zfp_rate'] == 4]['Avg time'].values[0]
plt.plot([1,2,4],[y,y,y],color=colors[1], linestyle=':') 

plt.plot(a['zfp_rate'],streamd_size_MB/a['Avg time'],color=colors[2],label='Add-ZFP', linestyle=':')
y=streamd_size_MB/a.loc[a['zfp_rate'] == 4]['Avg time'].values[0]
plt.plot([1,2,4],[y,y,y],color=colors[2], linestyle=':')

plt.plot(t['zfp_rate'],streamd_size_MB/t['Avg time'],color=colors[3],label='Triad-ZFP', linestyle=':')
y=streamd_size_MB/t.loc[t['zfp_rate'] == 4]['Avg time'].values[0]
plt.plot([1,2,4],[y,y,y],color=colors[3], linestyle=':')

plt.plot(c2['zfp_rate'],streamd_size_MB/c2['Avg time'],color=colors[0],label='Copy', linestyle='-')
y=streamd_size_MB/c2.loc[c2['zfp_rate'] == 4]['Avg time'].values[0]
plt.plot([1,2,4],[y,y,y],color=colors[0], linestyle='-')

plt.plot(s2['zfp_rate'],streamd_size_MB/s2['Avg time'],color=colors[1],label='Scale', linestyle='-') 
y=streamd_size_MB/s2.loc[s2['zfp_rate'] == 4]['Avg time'].values[0]
plt.plot([1,2,4],[y,y,y],color=colors[1], linestyle='-') 

plt.plot(a2['zfp_rate'],streamd_size_MB/a2['Avg time'],color=colors[2],label='Add', linestyle='-')
y=streamd_size_MB/a2.loc[a2['zfp_rate'] == 4]['Avg time'].values[0]
plt.plot([1,2,4],[y,y,y],color=colors[2], linestyle='-')

plt.plot(t2['zfp_rate'],streamd_size_MB/t2['Avg time'],color=colors[3],label='Triad', linestyle='-')
y=streamd_size_MB/t2.loc[t2['zfp_rate'] == 4]['Avg time'].values[0]
plt.plot([1,2,4],[y,y,y],color=colors[3], linestyle='-')


plt.semilogy(basey=10)
#plt.yscale('log')
xax=[2**i for i in range(0,7)]
plt.xticks(xax, [str(x) for x in xax])

plt.ylabel("Average Bandwidth (MB/s)", weight='bold')
plt.xlabel("Bits Per Value", weight='bold')
#plt.title(str(streamd_size_MB) + " MB Stream")
plt.legend(loc='center', frameon=True, ncol=3, fontsize=14)
plt.tight_layout()

plt.savefig(("max" if Max else "min")+"_"+str(size)+"_.pdf")
plt.gcf().clear()


