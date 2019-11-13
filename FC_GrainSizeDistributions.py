import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
'''
Plot grain size distribution from lab analysis.

'''
in_file = '/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/SedimentLabAnanlysis.csv'
df = pd.read_csv(in_file,header=14, usecols=['Mesh','Sediment1','Sediment2','Sediment3',
                            'Sediment4','Sediment5','Sediment6']).iloc[::-1 ,:]

fntsize = 12
mrkrsize = 10
lnwidth = 2
fig = plt.figure(figsize=(10, 5))
plt.style.use('ggplot')
plt.semilogx(df.Mesh[:-2],np.cumsum(df.Sediment1[:-2]),'d:',label='Sample 1',linewidth=lnwidth,markersize=6)
plt.semilogx(df.Mesh[:-2],np.cumsum(df.Sediment3[:-2]),'*:',label='Sample 2',linewidth=lnwidth,markersize=mrkrsize)
plt.semilogx(df.Mesh[:-2],np.cumsum(df.Sediment4[:-2]),'v:',label='Sample 3',linewidth=lnwidth,markersize=8)
plt.semilogx(df.Mesh[:-2],np.cumsum(df.Sediment5[:-2]),'.:',label='Sample 4',linewidth=lnwidth,markersize=mrkrsize)
plt.semilogx(df.Mesh[:-2],np.cumsum(df.Sediment6[:-2]),'s:',label='Sample 5',linewidth=lnwidth,markersize=6)
plt.semilogx(df.Mesh[:-2],np.cumsum(df.Sediment2[:-2]),'.-',label='Sample 6',linewidth=lnwidth,markersize=mrkrsize)
plt.text(0.068,1.05,0.075, fontsize=fntsize, color='k')
plt.text(0.098,1.05,0.106, fontsize=fntsize, color='k')
plt.text(0.14,1.05,0.150, fontsize=fntsize, color='k')
plt.text(0.23,1.05,0.250, fontsize=fntsize, color='k')
plt.text(0.38,1.05,0.425, fontsize=fntsize, color='k')
plt.text(0.75,1.05,0.825, fontsize=fntsize, color='k')
plt.text(1.1,1.05,1.18, fontsize=fntsize, color='k')
plt.text(2.1,1.05,2.36, fontsize=fntsize, color='k')
#plt.text(4.3,1.05,4.75, fontsize=18, color='k')
#plt.text(5.90,1.05,6.35, fontsize=18, color='k')
ax = plt.gca()
ax.grid(which='both', axis='x', linestyle='--')
plt.xlabel('Grain size [mm]',fontsize=fntsize)
plt.ylabel('Fraction finer by weight',fontsize=fntsize)
lgd=plt.legend(loc=9,bbox_to_anchor=(1.12, 1.021),fontsize=fntsize)
plt.setp(ax.get_xticklabels(), fontsize=fntsize)
plt.setp(ax.get_yticklabels(), fontsize=fntsize)
ax.xaxis.label.set_color('black')
ax.yaxis.label.set_color('black')
ax.tick_params(axis='x', colors='k')
ax.tick_params(axis='y', colors='k')
#plt.show()
plt.savefig('/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/grainsizedist.pdf',bbox_extra_artists=(lgd,), bbox_inches='tight',pad_inches=0.4)
