import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''
plot pre-, post 2013, and post 2015 longitudinal profiles along Flat Creek Glacier.
'''
in_file = '/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/TerrainAnalysis/slope_profiles.csv'
data = pd.read_csv(in_file, header = 1,
    names = ['d12', 'x12', 'y12', 'z12', 'd14', 'x14','y14', 'z14', 'd16', 'x16', 'y16', 'z16'])


fig = plt.figure(figsize = (11,5))
#plt.style.use('ggplot')
plt.plot(data.d12, data.z12, label = 'Elevation 2012', color = 'purple')
plt.plot(data.d14, data.z14, label = 'Elevation 2014', color = 'darkorange')
#plt.plot(data.d15, data.z15, label = 'Elevation 2015')
plt.plot(data.d16, data.z16, color = 'dimgray', label = 'Elevation 2016')
plt.xlabel('Distance [m]', fontsize = 18)
plt.ylabel('Elevation [m]', fontsize = 18)
plt.title('Profile view of Flat Creek detachments', fontsize = 18)
plt.ylim([1900,2750])
plt.xlim([-20, 1650])
ax = plt.gca()
plt.yticks(np.arange(2000, 2800, step=200))
ax.tick_params('both', labelsize = 16)
plt.legend(fontsize = 16)
plt.grid(True, color='gainsboro', linestyle='-', linewidth=1)
plt.tight_layout()
#plt.show()
plt.savefig('FlatCreek_profile_view.pdf', format = 'pdf')
