import numpy as np
import pandas as pd
from PIL import Image
import coreglib #from https://github.com/dshean/demcoreg/tree/master/demcoreg
import matplotlib.pyplot as plt
from scipy import stats
import richdem
from osgeo import gdal
import os
'''
Coregister two DEMs using the approach defined by Nuuth and Kääb, 2011.
Do iteratively.
'''
# define current ul and lr coordinates of DEM (gdalinfo)
ulx = -3120657.000
uly = 364089.000
lrx = -3102213.000
lry = 349321.000

rd = richdem.LoadGDAL("/Users/mistral/Documents/CUBoulder/Science/Sulzer/VolumeCalculations/NewProcessingSummer2018/20141012.tif",
                no_data = 3.40282e+38)


file = "/Users/mistral/Documents/CUBoulder/Science/Sulzer/VolumeCalculations/NewProcessingSummer2018/20141012.tif"
ds = gdal.Open(file)
band = ds.GetRasterBand(1)
arr = band.ReadAsArray()
[cols, rows] = arr.shape

plt.imshow(arr, interpolation='none', vmin = 1000, vmax = 4000)
plt.colorbar()
plt.show()

gt = ds.GetGeoTransform()

outFileName = '/Users/mistral/Documents/CUBoulder/Science/Sulzer/VolumeCalculations/NewProcessingSummer2018/shiftedDEM.tif'
driver = gdal.GetDriverByName("GTiff")
outdata = driver.Create(outFileName, rows, cols, 1, gdal.GDT_Float32)
outdata.SetGeoTransform([-3120647.0, 2.0, 0.0, 364099.0, 0.0, -2.0])##change geotransform
#outdata.SetGeoTransform(ds.GetGeoTransform())##sets same geotransform as input
outdata.SetProjection(ds.GetProjection())##sets same projection as input
outdata.GetRasterBand(1).WriteArray(arr)
outdata.GetRasterBand(1).SetNoDataValue(-3.40282e+38)##if you want these values transparent
#stop here and use outdata as the shifted DEM to use in new iteration
newband = outdata.GetRasterBand(1)
newarray = newband.ReadAsArray()

#For saving final, shifted DEM use the following, together with lines above:
outdata.FlushCache() ##saves to disk!!
outdata = None
band=None
ds=None


#import datasets where unstable areas are masked out
DH = np.array(Image.open("/Users/mistral/Documents/CUBoulder/Science/Sulzer/VolumeCalculations/2014minus2012_StableAreamask.tif"))
SLOPE = np.array(Image.open("/Users/mistral/Documents/CUBoulder/Science/Sulzer/VolumeCalculations/2016_slope_StableAreaMask.tif"))
ASPECT = np.array(Image.open("/Users/mistral/Documents/CUBoulder/Science/Sulzer/VolumeCalculations/2016_aspect_StableAreaMask.tif"))

DH[DH == -9999] = np.nan
SLOPE[SLOPE == -9999] = np.nan
ASPECT[ASPECT == -9999] = np.nan

dh = pd.Series(DH.flatten())
slope = pd.Series(SLOPE.flatten())
aspect = pd.Series(ASPECT.flatten())

#apply Nuth and Kääb Offset estimation
fit , f = coreglib.compute_offset_nuth(dh,slope,aspect)

#convert to dx dy
dx = np.sin(fit[1])*fit[0]
dy = np.cos(fit[1])*fit[0]

# compute new ul and lr coordinates
n_ulx = ulx + dx
n_uly = uly + dy
n_lrx = lrx + dx
n_lry = lry + dy

print(n_ulx, n_uly)
print(n_lrx, n_lry)

'''
Plot dh of dxdy shifted difference raster against evlevation to see if there
is an elevation bias (from snow or the like)

'''
# 2016_2014
fp = '/Users/mistral/Documents/CUBoulder/Science/Sulzer/VolumeCalculations/NewProcessingSummer2018'
f_DH = "201909_2015minus2014_StableAreamask.tif"
f_H = "20150908.tif"

DH = np.array(Image.open(os.path.join(fp, f_DH)))
H = np.array(Image.open(os.path.join(fp, f_H)))

DH[DH == -9999] = np.nan
H[H == -9999] = np.nan

dh = pd.Series(DH.flatten())
h = pd.Series(H.flatten())

nan_mask = ~np.isnan(dh) & ~np.isnan(h)

#bin values
bin_values = np.arange(start=1000, stop=3300, step=50)
bin_means = np.zeros(len(bin_values)-1)
for i in range(0,len(bin_values)-1):
    bin_means[i] = (bin_values[i] + bin_values[i+1])/2

boxes = []
for i in range (0,len(bin_values)-1):
    h_mask = (h >= bin_values[i]) & (h < bin_values[i+1])
    box = (dh[h_mask][nan_mask]).values
    boxes.append(box)


boxes_median = np.zeros(len(boxes))
for i in range (0, len(boxes)):
    boxes_median[i] = np.median(boxes[i])

#fit functions to box_means

z1 = np.polyfit(bin_means,boxes_median,1)
p1 = np.poly1d(z1)

z3 = np.polyfit(bin_means,boxes_median,3)
p3 = np.poly1d(z3)

z5 = np.polyfit(bin_means,boxes_median,5)
p5 = np.poly1d(z5)

#plot
fig = plt.figure(figsize=(15,6))
plt.boxplot(boxes, showfliers = False)
plt.plot(p5(bin_means),'g')
plt.ylim([-8,8])
plt.xlabel('Elevation bins [50m]', fontsize = 18)
plt.ylabel('dh [m]', fontsize = 18)
plt.show()
#plt.savefig('Elevation_correction.png')
