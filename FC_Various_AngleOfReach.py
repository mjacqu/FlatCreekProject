import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
'''
Plot angle of reach for different glacier detachement / collapse events. all
numbers taken from literature (except Flat Creek)
'''
in_file = '/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/Angle_of_reach.csv'
df = pd.read_csv(in_file, usecols=['Event','H','L','H/L','arctan_alpha'])

fig, ax = plt.subplots(figsize=(10, 6))
plt.style.use('ggplot')
mrkrsize = 12
fntsize = 12
plt.semilogx(df.L[0],df.H[0],'.',markersize=mrkrsize, label=df.Event[0])
plt.semilogx(df.L[1],df.H[1],'.',markersize=mrkrsize, label=df.Event[1])
plt.semilogx(df.L[2],df.H[2],'.',markersize=mrkrsize, label=df.Event[2])
plt.semilogx(df.L[3],df.H[3],'.',markersize=mrkrsize, label=df.Event[3])
plt.semilogx(df.L[4],df.H[4],'.',markersize=mrkrsize, label=df.Event[4])
plt.semilogx(df.L[5],df.H[5],'.',markersize=mrkrsize, label=df.Event[5])
plt.semilogx(df.L[6],df.H[6],'.',markersize=mrkrsize, label=df.Event[6])
plt.semilogx(df.L[7],df.H[7],'*',markersize=mrkrsize, label=df.Event[7])
plt.semilogx(df.L[8],df.H[8],'*',markersize=mrkrsize, label=df.Event[8])
plt.semilogx(df.L[9],df.H[9],'*',markersize=mrkrsize, label=df.Event[9])
plt.semilogx(df.L[10],df.H[10],'*',markersize=mrkrsize, label=df.Event[10])
plt.semilogx(df.L[11],df.H[11],'*',markersize=mrkrsize, label=df.Event[11])
plt.semilogx(df.L[12],df.H[12],'*',markersize=mrkrsize, label=df.Event[12])
plt.semilogx(df.L[13],df.H[13],'*',markersize=mrkrsize, label=df.Event[13])
for i, txt in enumerate(np.round(df.arctan_alpha,decimals=2)):
    ax.annotate(txt, (df.L[i]+50, df.H[i]+20), fontsize=fntsize, color='black')

lgd = plt.legend(loc=9,bbox_to_anchor=(1.12, 1.021),fontsize=fntsize)
plt.xlabel('Runout Distance [m]',fontsize=fntsize)
plt.ylabel('Fall Height [m]',fontsize=fntsize)
ax = plt.gca()
plt.setp(ax.get_xticklabels(), fontsize=fntsize)
plt.setp(ax.get_yticklabels(), fontsize=fntsize)
ax.xaxis.label.set_color('black')
ax.yaxis.label.set_color('black')
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')
#plt.show()
plt.savefig('/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/angleofreach.png',transparent=False,bbox_extra_artists=(lgd,), bbox_inches='tight')
