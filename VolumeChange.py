from rasterstats import zonal_stats

def CalculateVolumes(shapefile,raster,resolution, stats="mean min max sum count"):
    """
    Calculate volumes of change in a raster within a shapefile.
    Returns Volume and stats

    shapefile = path to shapefile (str)
    raster = path to rasters (str)
    resolution = resolution of raster in meters (int)
    stats = statistics to return. Default is mean min max sum count
    """

    statistics = zonal_stats(shapefile,raster,stats=stats)
    vol = statistics[0]["sum"]*(resolution**2)
    return (vol,statistics)
