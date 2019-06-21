import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''
plot pre-, post 2013, and post 2015 longitudinal profiles along Flat Creek Glacier.
'''
in_file = '/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/TerrainAnalysis/profileview.csv'
data = pd.read_csv(in_file, header = None, names = ['x16', 'z16', 'x12', 'z12', 'x14', 'z14'])

fig = plt.figure(figsize=(20,8))
plt.axis('equal')
plt.style.use('ggplot')
plt.plot(data.x12, data.z12, label = 'Elevation 2012')
plt.plot(data.x14, data.z14, label = 'Elevation 2014')
plt.plot(data.x16, data.z16, color = 'k', label = 'Elevation 2016')
plt.xlabel('Distance [m]', fontsize = 24)
plt.ylabel('Elevation [m]', fontsize = 24)
plt.title('Profile view of Flat Creek failure', fontsize = 24)
ax = plt.gca()
ax.tick_params('both', labelsize = 22)
plt.legend(fontsize = 20)
plt.show()
#plt.savefig('FlatCreek_profile_view.png')
