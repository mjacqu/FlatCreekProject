import numpy as np
import pandas as pd
from PIL import Image
import coreglib #from https://github.com/dshean/demcoreg/tree/master/demcoreg
import matplotlib.pyplot as plt
from scipy import stats

'''
Coregister two DEMs using the approach defined by Nuuth and Kääb, 2011.
Do iteratively.
'''
# define current ul and lr coordinates of DEM (gdalinfo)
ulx = -3120657.000
uly = 364089.000
lrx = -3102213.000
lry = 349321.000

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
DH_shifted = np.array(Image.open("/Users/mistral/Documents/CUBoulder/Science/Sulzer/VolumeCalculations/2016minus2014_dxdy_StableAreamask.tif"))
H_shifted = np.array(Image.open("/Users/mistral/Documents/CUBoulder/Science/Sulzer/VolumeCalculations/20160313_dxdy_StableAreaMask.tif"))

# 2014_2012
DH_shifted = np.array(Image.open("/Users/mistral/Documents/CUBoulder/Science/Sulzer/VolumeCalculations/2014minus2012_StableAreamask.tif"))
H_shifted = np.array(Image.open("/Users/mistral/Documents/CUBoulder/Science/Sulzer/VolumeCalculations/20141012_StableAreaMask.tif"))

DH_shifted[DH_shifted == -9999] = np.nan
H_shifted[H_shifted == -9999] = np.nan

dh_shifted = pd.Series(DH_shifted.flatten())
h_shifted = pd.Series(H_shifted.flatten())

nan_mask = ~np.isnan(dh_shifted) & ~np.isnan(h_shifted)

#bin values
bin_values = np.arange(start=1000, stop=3300, step=50)
bin_means = np.zeros(len(bin_values)-1)
for i in range(0,len(bin_values)-1):
    bin_means[i] = (bin_values[i] + bin_values[i+1])/2

boxes = []
for i in range (0,len(bin_values)-1):
    h_mask = (h_shifted >= bin_values[i]) & (h_shifted < bin_values[i+1])
    box = (dh_shifted[h_mask][nan_mask]).values
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
