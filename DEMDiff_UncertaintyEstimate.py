import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib
import line_profiler

def berthier_uncertainty(filename, nan, resolution):
    """
    Calculates empirical uncertainty estimate for DEM difference based on tiling
    method published in Berthier et al., 2018
    (https://www.the-cryosphere-discuss.net/tc-2018-152/tc-2018-152.pdf)
    The dH map is tiled into n^2 tiles with n ranging from 2 to 200.

    Arguments:
        filename (str): Path to masked DEM difference file  of stable areas (geotiff).
        nan (float or int): Specify NaN values used in geotiff, i.e. -9999.0
        resolution (int): Resolution of geotiff.

    Returns:
        ndarray: Array of tile size and corresponding mean dH
        scipy.stats._stats_mstats_common.LinregressResult:
            Linear regression params as returned by scipy.stats.linregress()
        matplotlib.figure.Figure: Plot object of results plot
    """
    dh = np.array(Image.open(filename))
    dh[dh==nan] = np.nan

    res = resolution #resolution of DEM in m
    n_tiles = np.unique(np.round(np.e**np.arange(0.5,5.4,0.1))).astype(int)
    area_error = np.zeros([len(n_tiles),2])


    for n in range(0,len(n_tiles)):
        median = []
        row_step = np.int(np.round((dh.shape[0]/n_tiles[n])))
        col_step = np.int(np.round((dh.shape[1]/n_tiles[n])))
        area_error[n,0] = ((row_step*res) * (col_step*res))/10e6
        for i in range(0,n_tiles[n]):
            for j in range(0,n_tiles[n]):
                tile = dh[i*row_step:(i+1)*row_step,j*col_step:(j+1)*col_step]
                tile_median = np.abs(np.nanmedian(tile))
                median.append(tile_median)
        dh_error = np.nanmean(median)
        area_error[n,1] = dh_error

    #prof = line_profiler.LineProfiler()
    #prof.add_function(f)
    #run = prof.run('f()')
    #run.print_stats()

    # fit linear regression to ln(area) vs. error
    lin_regress = stats.linregress(np.log(area_error[:,0]), area_error[:,1])
    r_squared = lin_regress[2]**2


    # Plot
    f, axarr = plt.subplots(figsize=(6, 6))
    axarr.semilogx(area_error[:,0], area_error[:,1],'*')
    axarr.semilogx(area_error[:,0], lin_regress[0]*np.log(area_error[:,0])+lin_regress[1])
    plt.title('Tile size vs. error')
    plt.xlabel('Tile size [sq. km]')
    plt.ylabel('Mean absolute dH [m]')
    plt.text(0.008, max(area_error[:,1]), 'y = '+ str(lin_regress[0])+' ln(x)+'+str(lin_regress[1]))
    plt.text(0.05, max(area_error[:,1])-0.05, "$R^{2}$ = " + str(r_squared))


    return(area_error, lin_regress, f)
