import os, rasterio
import xarray as xr
from shapely.geometry import Point
import numpy as np
import pandas as pd
import geopandas as gpd
import glob

'''
Extract time-series data for individual points from downscaled Alaska ERA Interim
data (Bieniek et al., 2015). Input file is a netCDF files.
Code partially (mostly?) courtesy of Michael Lindgren at UAF.
'''


def extract_loc_profile(path_to_file, lat, lon, variable, loc_name):

    '''
    path_to_file = path to file (string)
    lat = latitude of point of interest (float)
    lon = longitude of point of interest (float)
    variable = name of dataset variable, i.e. pcpt, t2 etc. (string)
    loc_name = Location name, i.e. Fairbanks, Columbia Glacier, (string)
    '''

    # read in a NetCDF dataset using xarray
    ds = xr.open_dataset( path_to_file )

    # point location in EPSG:4326 -- WGS84 latlon -- Flat Creek Glacier
    lon,lat = ( lon, lat )

    # some constant metadata about the WRF grid
    res = 20000 # 20km resolution both directions
    x0,y0 = np.array( ds.xc.min()-(res/2.)), np.array(ds.yc.max()+(res/2.) ) # origin point upper-left corner from centroid
    wrf_crs = '+units=m +proj=stere +lat_ts=64.0 +lon_0=-152.0 +lat_0=90.0 +x_0=0 +y_0=0 +a=6370000 +b=6370000'
    a = rasterio.transform.from_origin( x0, y0, res, res ) # build affine transform using rasterio mechanics

    # make the point location in to a geopandas GeoDataFrame -- there are ways to do this with pyproj, but I like this approach
    shp = gpd.GeoDataFrame({'id':[1], 'name':[loc_name], 'geometry':[Point(lon,lat)]}, crs={'init':'epsg:4326'}, geometry='geometry' )

    # reproject that point shapefile to the wrf crs
    shp_wrf = shp.to_crs( wrf_crs )

    # now lets pull out the x,y from that point object in the reprojected shapefile
    xy, = shp_wrf.geometry.tolist()
    x = xy.x
    y = xy.y

    # now we can use the affine transform with these x/y values to find where in space we land
    col, row = ~a * (x, y)
    col, row = [ int(i) for i in [col, row] ] # truncate to integer

    # now using that info we can pull a profile from the NetCDF using NumPy ndarray indexing.
    profile = ds[variable][:,row,col]

    # then you can turn it into a pandas object (a series in this case) with this
    #series = profile.to_pandas().head()

    # or to a pandas dataframe (with all of the coordinate information) like this
    df = profile.to_dataframe()

    return(df,x,y,col,row)



files = glob.glob('t2*')
#print(files)

time_series = pd.DataFrame([])
#print(time_series)

#FC coordinates -141.557730, 61.640682
#Chisana coordinates -142.042191,62.068633

for infile in files:
	print(infile)
	df,x,y,col,row = extract_loc_profile(infile, 62.068633, -142.042191, 't2', 'Chisana')
	#print(df,x,y,col,row)
	time_series = time_series.append(df)
	#print(time_series)

time_series = time_series.sort_index(axis = 0)
time_series.to_csv('./ERA_t2_hourly_UTC_Chisana.csv')
