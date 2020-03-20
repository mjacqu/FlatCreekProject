# Flat Creek Project Code

This repository contains all code (and then some) used to process data associated
with the publication: What drives large-scale glacier detachments? Insights from Flat
Creek Glacier, Wrangell Mountains, Alaska.

(citation: M. Jacquemart, M. Loso, M. Leopold, E. Welty, E. Berthier, J. Hansen,
  J. Sykes, K. Tiampo, What drives large-scale glacier detachments? Insights from
  Flat Creek Glacier, Wrangell Mountains, Alaska. Geology, 2020)

The following documentation contains a short description of the content of each
script:

## Aru_WaterAvailability.py
  This code uses ERA Interim climate data to run a water availability model for
  the Aru Glaciers in Tibet.

## DEMDiff_UncertaintyEstimate.py
  Contains a function that calculates empirical uncertainty estimate for DEM
  difference based on tiling method published in Berthier et al., 2018
  (https://www.the-cryosphere-discuss.net/tc-2018-152/tc-2018-152.pdf)

## FC_BulgeSize.py
  Calculate sun elevation and azimuth based on date and time of image acquisition.
  Calculate size of bulge on glacier based on digitized shadow lengths

## FC_DEM_coregistration.py
  Deprecated. Contains code to co-register DEMs based on some code from D. Shean
  (https://github.com/dshean/demcoreg/tree/master/demcoreg).
  Also contains code to estimate an elevation-dependent bias and to fit a
  polynomial function to that to correct.

## FC_ FlowAccumulation.py
  Deprecated. Attempt to compute flow accumulation in python, but was not used
  to produce results for final paper (QGIS routine used instead).

## FC_GeologyFigure4.py
  Code to generate elevation dependent water availability figure.
  (Figure 4 of Geology paper)

## FC_GetDEMErrorFunctions.py
  Run uncertainty estimate for DEM differences.

## FC_GetERA_timeseries_NetCDF.py
  Extract time-series data for individual points from downscaled Alaska ERA Interim
  data (Bieniek et al., 2015). Input file is a netCDF files.
  Code partially (mostly?) courtesy of Michael Lindgren at UAF.

## FC_GlacierTimelapse.py
  Convert set of Geotiffs into pngs with date stamped on image for timelapse animation.

## FC_GrainSizeDistributions.py
  Plot grainsize distribution from lab analysis.

## FC_GroundTemps.py
  Plot data from ground temperature measurements.

## FC_LongitudianlProfiles.py
  Plots longitudinal profiles along Flat Creek Glacier from DEMs of 2012, 2014 and 2016.

## FC_Seismicity.py
  Imports seismicity dataset (csv file, downloaded from https://earthquake.usgs.gov/earthquakes/search/)
  Calculates distances to Flat Creek and plots distance vs time with magnitudes for different EQ.

## FC_Various_AngleOfReach.py
  Plots angle of reach (Fahrböschung or Mobility Index) for 2013 and 2015 glacier detachments at Flat Creek.

## FC_VolumeCalculations.py
  Calculate volumes of different detachments of at Flat Creek. Can split erosional (negative surface change) and depositional (positive surface change) for individual budgeting.

## FC_WaterAvailabiltyModel.py
  Run water availability calculation for Flat Creek at hourly resolution.

## FC_debias_temperatures.py
  De-bias downscaled ERA interim climate data against Chisana weather station data.

## FC_velocity_estimation.py
  Calculates superelevation and resulting flow velociteis using trimline elevations in different years from digitized trimlines.
  Calculate runup velocities of West Hill based on multiple profiles digitized from DEMS that reach from the river over the summit of West Hill.

## VariousFunctions_FC.py
  Includes functions to get trends from time-series data, standard deviation of individual years relative to long term mean, and water availability calculation.

## VolumeChange.py
  Calculate volumes of change from raster data within a shapefile. Returns volume and stats.
