# Flat Creek Project Code

This repository contains all code used to process data associated with the
publication: What drives large-scale glacier detachments? Insights from Flat
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
  Cotains a function that calculates empirical uncertainty estimate for DEM
  difference based on tiling method published in Berthier et al., 2018
  (https://www.the-cryosphere-discuss.net/tc-2018-152/tc-2018-152.pdf)
  The dH map is tiled into n^2 tiles with n ranging from 2 to 200.
