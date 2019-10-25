import richdem
import matplotlib.pyplot as plot


infile = '/Users/mistral/Documents/CUBoulder/Science/Sulzer/VolumeCalculations/NewProcessingSummer2018/2012_EPSG3413_crop.tif'

rd = richdem.LoadGDAL(infile, no_data = -9999)

flow_acc = richdem.FlowAccumulation(rd, method = 'Rho8')

fig, (ax1, ax2) = plt.subplots(1,2)
ax1.imshow(flow_acc, interpolation='none', vmin = 1, vmax = 20)
ax2.imshow(rd, interpolation='none', vmin = 2000, vmax = 3000)
ax1.set_xlim([1250,1800])
ax1.set_ylim([1400,900])
ax2.set_xlim([1250,1800])
ax2.set_ylim([1400,900])
#plt.colorbar()
plt.show()
