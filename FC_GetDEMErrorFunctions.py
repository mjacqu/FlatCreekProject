from DEMDiff_UncertaintyEstimate import berthier_uncertainty
import matplotlib.pyplot as plt

'''
Run uncertainty estimate
'''

file = '/Users/mistral/Documents/CUBoulder/Science/Sulzer/VolumeCalculations/2014minus2012_dxdydz_StableAreaMaskBuffered.tif'
area_error, regression, figure = berthier_uncertainty(file, -9999.0, 2)

plt.show()
