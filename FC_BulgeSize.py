import numpy as np
import pandas as pd
import pysolar
import datetime
import math
import json
import Taan_fjord_helpers
import matplotlib.pyplot as plt

path = '/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/BulgeSize/ShadowLengths2011_189.4083az.geojson'

#Flat Creek Location
lat = 61.642563
lon = -141.554821

# Image 1: Planet 2011-09-08
date1 = datetime.datetime(2011, 9, 8, 21, 55, 20, tzinfo = datetime.timezone.utc)
im1_elev = pysolar.solar.get_altitude(lat,lon,date1)
im1_azimuth = pysolar.solar.get_azimuth(lat,lon,date1)
print(im1_elev, im1_azimuth)
im1_md_elev = 33.83808 # elevation from image meta data
im1_md_azimuth = 189.3034 # azimuth from image meta data

# Image 2: Planet 2012-08-15
date2 = datetime.datetime(2012, 8, 15, 21, 54, 46, tzinfo = datetime.timezone.utc)
im2_elev = pysolar.solar.get_altitude(lat,lon,date2)
im2_azimuth = pysolar.solar.get_azimuth(lat,lon,date2)
print(im2_elev, im2_azimuth)
m2_md_elev = 42.08575 # elevation from image meta data
im2_md_azimuth = 187.78853 # azimuth from image meta data

# Image 3: Ikonos 2009-07-13

# Read GeoJson with digitized shadow lengths and turn into pandas dataframe with
# id, length, stard and end coordinates.

with open(path) as f:
    data = json.load(f)

shadows = pd.DataFrame()

for feature in data['features']:
    id = feature['properties']['id']
    length = feature['properties']['Length']
    start_x = feature['geometry']['coordinates'][0][0]
    start_y = feature['geometry']['coordinates'][0][1]
    end = feature['geometry']['coordinates'][1]
    line = {'id': [id], 'length':[length], 'start_x': [start_x], 'start_y': [start_y], 'end':[end]}
    df = pd.DataFrame(line)
    shadows = shadows.append(df,ignore_index=True)

shadows.head()

# Extract local slope:
altitudes = []
for l in range(0, shadows.shape[0]):
    row, col, alt = Taan_fjord_helpers.median_of_square('/Users/mistral/Documents/CUBoulder/Science/Sulzer/VolumeCalculations/2012.tif',
    [shadows.start_x[l], shadows.start_y[l]], 'EPSG:3338', 5)
    altitudes.append(alt)

shadows['altitude'] = altitudes

incidence_angle = im1_md_elev
bulge_height = []
for l in range(0, shadows.shape[0]):
    h = np.tan(math.radians(incidence_angle)) * shadows.length[l]
    bulge_height.append(h)

shadows['bulge_elevation'] = bulge_height + shadows.altitude

shadows = shadows.sort_values(by=['id'])
plt.plot(shadows.start_x-shadows.start_x[0], shadows.bulge_elevation, '--.')
plt.show()
