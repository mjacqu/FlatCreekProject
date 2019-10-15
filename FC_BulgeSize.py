import numpy as np
import pandas as pd
import pysolar
import datetime
import math
import json
import Taan_fjord_helpers
import matplotlib.pyplot as plt

bulge2011 = '/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/BulgeSize/ShadowLengths2011_189.4083az.geojson'
bulge2011_adj = '/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/BulgeSize/ShadowLengths2011_189.4083az_adjusted.geojson'
bulge2009 = '/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/BulgeSize/ShadowLengths2009_168.28az.geojson'
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
date3 = datetime.datetime(2009, 7, 13, 20, 59, 31, tzinfo = datetime.timezone.utc)
im3_elev = pysolar.solar.get_altitude(lat,lon,date3)
im3_azimuth = pysolar.solar.get_azimuth(lat,lon,date3)
print(im3_elev, im3_azimuth)
im3_md_elev = 49.59662 # elevation from image meta data
im3_md_azimuth = 167.9135 # azimuth from image meta data

# Read GeoJson with digitized shadow lengths and turn into pandas dataframe with
# id, length, start and end coordinates. Pixel size is in meters
def calculate_bulge_elevation(shadow_lengths, sun_elevation, pixel_size):
    with open(shadow_lengths) as f:
        data = json.load(f)
    #make shadows dataframe
    shadows = pd.DataFrame()
    # extract values from geojson
    for feature in data['features']:
        id = feature['properties']['id']
        length = feature['properties']['Length']
        start_x = feature['geometry']['coordinates'][0][0]
        start_y = feature['geometry']['coordinates'][0][1]
        end_x = feature['geometry']['coordinates'][1][0]
        end_y = feature['geometry']['coordinates'][1][1]
        #constrain uncertainty by adding/subtracting 2*pixel_size to/from length
        p2p = length+(2*pixel_size) #plus two pixels
        m2p = length-(2*pixel_size) #minus two pixels
        line = {'id': [id], 'length':[length], 'start_x': [start_x], 'start_y': [start_y],
        'end_x':[end_x], 'end_y':[end_y], 'p2p':[p2p], 'm2p':[m2p]}
        df = pd.DataFrame(line)
        shadows = shadows.append(df,ignore_index=True)
    # print shadows head
    shadows.head()
    # Extract local elevation:
    altitudes = []
    for l in range(0, shadows.shape[0]):
        row, col, alt = Taan_fjord_helpers.median_of_square('/Users/mistral/Documents/CUBoulder/Science/Sulzer/VolumeCalculations/NewProcessingSummer2018/2012_Howat_dxdydz.tif',
        [shadows.start_x[l], shadows.start_y[l]], 'EPSG:3338', pixel_size)
        altitudes.append(alt)
    #append elevations to shadows dataframe
    shadows['altitude'] = altitudes
    #calculate heights
    incidence_angle = sun_elevation
    bulge_height = []
    bulge_height_min = []
    bulge_height_max = []
    for l in range(0, shadows.shape[0]):
        h = np.tan(math.radians(incidence_angle)) * shadows.length[l]
        h_min = np.tan(math.radians(incidence_angle)) * shadows.m2p[l]
        h_max = np.tan(math.radians(incidence_angle)) * shadows.p2p[l]
        bulge_height.append(h)
        bulge_height_min.append(h_min)
        bulge_height_max.append(h_max)
    #add bulge height starting point altitude
    shadows['bulge_elevation'] = bulge_height + shadows.altitude
    shadows['bulge_elevation_min'] = bulge_height_min + shadows.altitude
    shadows['bulge_elevation_max'] = bulge_height_max + shadows.altitude
    shadows = shadows.sort_values(by=['id'])
    return(shadows)

bulge_elevation_2009 = calculate_bulge_elevation(bulge2009, im3_elev, 2)
bulge_elevation_2011 = calculate_bulge_elevation(bulge2011, im1_elev, 5)
bulge_elevation_2011_adj = calculate_bulge_elevation(bulge2011_adj, im1_elev,5)


plt.plot(bulge_elevation_2009.end_x, bulge_elevation_2009.bulge_elevation, label = '2009')
plt.fill_between(bulge_elevation_2009.end_x, bulge_elevation_2009.bulge_elevation_min,
    bulge_elevation_2009.bulge_elevation_max, alpha = 0.2)
plt.plot(bulge_elevation_2011.end_x, bulge_elevation_2011.bulge_elevation, label = '2011')
plt.fill_between(bulge_elevation_2011.end_x, bulge_elevation_2011.bulge_elevation_min,
    bulge_elevation_2011.bulge_elevation_max, alpha = 0.2)
plt.ylim([2100,2300])
plt.xlabel('x [UTM]')
plt.ylabel('Elevation [m asl]')
plt.legend()
plt.show()
