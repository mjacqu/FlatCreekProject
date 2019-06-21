from VolumeChange import CalculateVolumes
import numpy as np

'''
Calculate volumes of different events at Flat Creek
'''

arcticdem_res = 2
Main2013 = CalculateVolumes("MainLoss2013.shp", "2014minus2012_dxdydz.tif", arcticdem_res)
Max2013 = CalculateVolumes("MaxLoss2013.shp", "2014minus2012_dxdydz.tif", arcticdem_res)
Main2015 = CalculateVolumes("MainLoss2015.shp", "2016minus2014_dxdydz.tif", arcticdem_res)
Max2015 = CalculateVolumes("MaxLoss2015.shp", "2016minus2014_dxdydz.tif", arcticdem_res)
MainTotal = CalculateVolumes("TotalLossMain.shp", "2016minus2012.tif", arcticdem_res)
FullBasinTotal = CalculateVolumes("TotalLossFullBasin.shp", "2016minus2012.tif", arcticdem_res)
MainLoss2013 = CalculateVolumes("Deposit2013.shp", "2014minus2012_dxdydz.tif", arcticdem_res)
MainLoss2015 = CalculateVolumes("2015_NetDeposit.shp","2016minus2014_dxdydz.tif", arcticdem_res )
SplitErosionDeposition = CalculateVolumes("Erosion_deposition.shp", "2016minus2014_dxdydz.tif", arcticdem_res)
Slope = CalculateVolumes("MainLoss2015.shp", "/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/TerrainAnalysis/2012_slope.tif", arcticdem_res)

######################################################
# total ice loss based on thickness from D. Farinotti
######################################################

icethick_res = 25
thickness_raster = "../data/Farinotti_ThicknessEstimates/thickness_RGI60-01.17460_EPSG3413.tif"

TotalIce = CalculateVolumes("FullGlacierOutline.shp",thickness_raster, icethick_res)
Ice2013 = CalculateVolumes("IceLoss2013.shp", thickness_raster, icethick_res)
Ice2015 = CalculateVolumes("IceLoss2015.shp", thickness_raster, icethick_res)
MaxIce2015 = CalculateVolumes("TotalLossFullBasin.shp", thickness_raster, icethick_res)
######################################################
# Split erosion and deposition from Erosion_deposition shape file
######################################################
AllSums = np.array([d['sum'] for d in SplitErosionDeposition[1]])
All_Erosion = AllSums[AllSums < 0]
All_Deposition = AllSums[AllSums >= 0]
Total_Erosion = np.sum(All_Erosion)*(arcticdem_res**2)
Total_Deposition = np.sum(All_Deposition)*(arcticdem_res**2)

# get total area of negative pixels
AllCounts = np.array([d['count'] for d in SplitErosionDeposition[1]])
ErosionArea = (np.sum(AllCounts[AllSums < 0]))*arcticdem_res**2
