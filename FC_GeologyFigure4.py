import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
import VariousFunctions_FC

fc_all = pd.read_csv('/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/meteo/FC_Water_all_Elevations.csv')

#fc_all.plot(x='time', y=["2100",'2200','2300','2400', "2500", '2600', '2700'], figsize = (12,6),
#                colormap = 'gist_earth', style = '--.', linewidth = 1, markersize =4)
mean80s = fc_all['2100'][(fc_all['time'] > 1979) & (fc_all['time'] < 1990)].mean()
mean90s = fc_all['2100'][(fc_all['time'] > 1989) & (fc_all['time'] < 2000)].mean()
mean00s = fc_all['2100'][(fc_all['time'] > 1999) & (fc_all['time'] < 2010)].mean()
mean10s = fc_all['2100'][(fc_all['time'] > 2009)].mean()
mean_all = pd.DataFrame(fc_all.mean(axis = 0)[1:])
mean_all.columns = ['mean']

plt.style.use('ggplot')
fc_all.plot(x='time', y=["2100",'2300', "2500", '2700'], figsize = (12,6),
                colormap = 'copper', style = '--.', linewidth = 1, markersize =4)
plt.hlines(mean80s,1980,1989.9, color = 'grey', label = 'decadal mean')
plt.hlines(mean90s,1990,1999.9, color = 'grey')
plt.hlines(mean00s,2000,2009.9, color = 'grey')
plt.hlines(mean10s,2010,2015.9, color = 'grey')
plt.xlim([1978,2016])
plt.tick_params('both', labelsize = 18)
plt.xlabel('Year', fontsize = 20)
plt.ylabel('Water availability [mm]', fontsize = 20)
plt.legend(fontsize = 16, loc = 2)
plt.legend(title = 'Elevation [m asl]')
plt.title('Pre-detachment total liquid water availability', fontsize = 22)
plt.show()
#plt.savefig('FC_all_elevations_decadalmean.pdf')

# Analyze numbers:

elevations = 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700
year = 2015
#Print all Standard Deviations and factors by which H2O exceeds mean:
for e in elevations:
    print('elevation: '+ str(e))
    VariousFunctions_FC.get_std(fc_all, str(e), year)
    fc_all[str(e)][fc_all.time == year].values/mean_all['mean'][mean_all.index == str(e)].values


'''
# Data import for old figure with Aru and Flat Creek.
aru_water = pd.read_csv('/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/Other_ERA/Aru_5500m_apr_jul_wateravailability.csv')
aru_melt = pd.read_csv('/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/Other_ERA/Aru_5500m_apr_jul_melt.csv')
fc_water = pd.read_csv('/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/meteo/FC_water_apr_jul_2200m.csv')
fc_melt = pd.read_csv('/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/meteo/FC_melt_apr_jul_2200m.csv')

# Old plot for Aru and Flat Creek
plt.style.use('ggplot')
fig,ax = plt.subplots(figsize = (16,10))
mpl.rcParams['lines.linewidth'] = 1.8
mpl.rcParams['lines.markersize'] = 8.5
ax.plot(aru_water.year, aru_water.total_water, '.-', color = 'skyblue', label = 'Aru (total)')
ax.plot(aru_melt.year, aru_melt['melt'],'.:', color = 'skyblue', label = 'Aru (from melt)')
ax.plot(fc_water.year, fc_water.total_water, '.-', color = 'grey', label = 'Flat Creek (total)')
ax.plot(fc_melt.year, fc_melt['melt'],'.:', color = 'grey', label = 'Flat Creek (from melt)')
plt.plot([2013], [510.55928471], 'o', color = 'black', markersize = 5)
plt.plot([2015], [285.17040509], 'o', color = 'black', markersize = 5)
plt.plot([2016], [533.367536], 'o', color = 'steelblue', markersize = 5)
ax.tick_params('both', labelsize = 18)
plt.xlabel('Year', fontsize = 20)
plt.ylabel('Water availability [mm]', fontsize = 20)
ax.legend(fontsize = 16, loc = 2)
plt.ylim([0,580])
plt.title('Pre-detachment total liquid water availability', fontsize = 22)
plt.text(2016.1,540, '2016', fontsize = 16, color = 'steelblue', fontweight = 'bold')
plt.text(2015.1,290, '2015', fontsize = 16, color = 'black', fontweight = 'bold')
plt.text(2013.2,515, '2013', fontsize = 16, color = 'black', fontweight = 'bold')
plt.show()
#plt.savefig('FC_and_Aru_water_availability.png')
'''
