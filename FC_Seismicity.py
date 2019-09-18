import pandas as pd
from geopy import distance
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates
from datetime import datetime

'''
Import seismicity dataset (csv file, downloaded from https://earthquake.usgs.gov/earthquakes/search/)
Calculate distances to Flat Creek
Plot distance vs time with magnitudes for different EQ.
'''

#in_file = '/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/seismicity/FC_EQcatalog.csv'
in_file = '/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/seismicity/Mag4-8Max1000km.csv'
data = pd.read_csv(in_file, parse_dates=['time'])
#data.pytime = [x.to_pydatetime() for x in data.time]

FC_coords = (61.641155, -141.557528)

#calulate distance of each event to Flat Creek
distances = np.zeros(len(data))
for i in range (0,len(data)):
    distances[i] = distance.distance(FC_coords,(data.latitude[i],data.longitude[i])).km

data['distance'] = distances

#plot overview figure
fig, ax = plt.subplots(figsize=(15,7))
ax.scatter(list(data.time), data.distance, s = data.mag, alpha = 0, label = 'Magnitude')
ax.scatter(list(data.time.loc[data.mag < 2]), data.distance.loc[data.mag < 2], s = 10*data.mag.loc[data.mag < 2], color = 'yellow', alpha = 1, linewidths = 2, edgecolors = 'k', label = 'M < 2')
ax.scatter(list(data.time.loc[(data.mag >=2) & (data.mag < 3)]), data.distance.loc[(data.mag >=2) & (data.mag < 3)], color = 'orange', s = 30*data.mag.loc[(data.mag >=2) & (data.mag < 3)], alpha = 1, linewidths = 2, edgecolors = 'k', label = '2<= M < 3')
ax.scatter(list(data.time.loc[(data.mag >=3) & (data.mag < 4)]), data.distance.loc[(data.mag >=3) & (data.mag < 4)], color = 'red', s = 50*data.mag.loc[(data.mag >=3) & (data.mag < 4)], alpha = 1, linewidths = 2, edgecolors = 'k', label = '3<= M < 4')
ax.scatter(list(data.time.loc[data.mag > 4]), data.distance.loc[data.mag > 4], s = 70*data.mag.loc[data.mag > 4], color = 'purple', alpha = 1, linewidths = 2, edgecolors = 'k', label = 'M > 4')
ax.axvline(datetime.strptime('2015-07-30 01:25:03', '%Y-%m-%d %H:%M:%S'), color='black')
ax.axvline(datetime.strptime('2013-08-05 18:59:36', '%Y-%m-%d %H:%M:%S'), color='black')
plt.legend(fontsize = 14)
plt.xlabel('Time [UTC]', fontsize = 16)
plt.ylabel('Distance from Flat Creek Glacier [km]', fontsize = 16)
ax.tick_params('both', labelsize = 16)
plt.title('Seismicity near Flat Creek', fontsize = 18)
plt.show()
#plt.savefig('AllSeismicity.png')

#Plot zoomed in versions of above plot
zoom_start = datetime.strptime('2015-07-31', '%Y-%m-%d')
zoom_end = datetime.strptime('2015-08-06', '%Y-%m-%d')

fig, ax = plt.subplots(figsize=(15,7))
ax.scatter(list(data.time), data.distance, s = data.mag, alpha = 0, label = 'Magnitude')
ax.scatter(list(data.time.loc[data.mag < 2]), data.distance.loc[data.mag < 2], s = 10*data.mag.loc[data.mag < 2], color = 'yellow', alpha = 1, linewidths = 2, edgecolors = 'k', label = 'M < 2')
ax.scatter(list(data.time.loc[(data.mag >=2) & (data.mag < 3)]), data.distance.loc[(data.mag >=2) & (data.mag < 3)], color = 'orange', s = 30*data.mag.loc[(data.mag >=2) & (data.mag < 3)], alpha = 1, linewidths = 2, edgecolors = 'k', label = '2<= M < 3')
ax.scatter(list(data.time.loc[(data.mag >=3) & (data.mag < 4)]), data.distance.loc[(data.mag >=3) & (data.mag < 4)], color = 'red', s = 50*data.mag.loc[(data.mag >=3) & (data.mag < 4)], alpha = 1, linewidths = 2, edgecolors = 'k', label = '3<= M < 4')
ax.scatter(list(data.time.loc[data.mag > 4]), data.distance.loc[data.mag > 4], s = 70*data.mag.loc[data.mag > 4], color = 'purple', alpha = 1, linewidths = 2, edgecolors = 'k', label = 'M > 4')
ax.axvline(datetime.strptime('2015-07-31 18:59:36', '%Y-%m-%d %H:%M:%S'), color='black')
ax.set_xlim([zoom_start, zoom_end])
plt.legend(fontsize = 14)
plt.xlabel('Time [UTC]', fontsize = 16)
plt.ylabel('Distance from Flat Creek Glacier [km]', fontsize = 16)
ax.tick_params('both', labelsize = 16)
plt.title('Seismicity near Flat Creek 2013-07-31 to 2013-08-06', fontsize = 18)
plt.show()
#plt.savefig('Seismicity2013.png')
