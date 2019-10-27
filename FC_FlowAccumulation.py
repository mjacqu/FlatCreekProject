import richdem
import matplotlib.pyplot as plt


infile = '/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/Hydrology/ifsar_merged.tif'

rd = richdem.LoadGDAL(infile, no_data = -9999)

#filled = richdem.FillDepressions(rd, in_place=False)
flow_acc = richdem.FlowAccumulation(rd, method = 'Rho8')


fig, (ax1, ax2) = plt.subplots(1,2)
ax1.imshow(flow_acc, interpolation='none', vmin = 40, vmax = 100)
ax2.imshow(rd, interpolation='none', vmin = 2000, vmax = 3000)
ax1.set_xlim([2100,3000])
ax1.set_ylim([3300,2800])
ax2.set_xlim([2100,3000])
ax2.set_ylim([3300,2800])
#ax1.colorbar()
#ax2.colorbar()
plt.show()

richdem.SaveGDAL("/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/Hydrology/Rho8_filled.tif", flow_acc)
