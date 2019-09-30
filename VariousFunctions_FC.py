import numpy as np
from scipy import stats


def get_trend(x,deg):
    """
    find trend in time series
    x = variable
    deg = polynomial order (1 for linear)
    """
    idx = np.isfinite(x.index) & np.isfinite(x)
    coefficients, residuals, _, _, _ = np.polyfit(range(len(x.index[idx])), x, deg, full = True)
    mse = residuals[0]/(len(x.index))
    nrmse = np.sqrt(mse)/(x.max() - x.min())
    print('Computed trend:')
    print('Slope ' + str(coefficients[0]))
    print('NRMSE: ' + str(nrmse))
    slope = (coefficients[0])
    trend = [coefficients[0]*x + coefficients[1] for x in range(0,len(x.index))]
    return (trend, slope, nrmse)

def get_std(df, year):
    summer_mean = np.mean(df)
    summer_std = np.std(df)
    summer_max = df[df.index == year].values
    summer_outlier = summer_max - summer_mean
    anomaly = (summer_outlier/summer_std)
    print(anomaly)

def water_availability(df, ddf_i, ddf_s):
    total_snow = np.zeros(len(df))
    melt = np.zeros(len(df))
    total_rain = np.zeros(len(df))
    for i in range(0, len(df)):
        if df.index[i].month == 9 and df.index[i].day == 30 and df.index[i].hour == 0:
            print('Resetting values at the end of WY ' + str(df.index[i].year))
            total_snow[i] = 0
            melt[i] = 0
            total_rain[i] = 0
        else:
            # if temps are negative, accumulate snow, melt and rain stay unchanged
            if df.t2_debias[i] <= 0:
                total_snow[i] = total_snow[i-1] + df.pcpt[i]
                melt[i] = melt[i-1]
                total_rain[i] = total_rain[i-1]
            # if temps are positive:
            else:
                # add precip:
                total_rain[i] = total_rain[i-1] + df.pcpt[i]
                # start melting using different melt factors for snow and ice:
                if total_snow[i-1] > 0:
                    #check if enough snow to melt
                    max_snow_melt = df.t2_debias[i]*ddf_s
                    if max_snow_melt < total_snow[i-1]:
                        total_snow[i] = total_snow[i-1] - max_snow_melt
                        melt[i] = melt[i-1] + df.t2_debias[i] * ddf_s
                    else:
                        total_snow[i] = 0
                        melt[i] = melt[i-1] + total_snow[i-1] + (df.t2_debias[i]*ddf_s-total_snow[i-1])*(ddf_i/ddf_s)
                else:
                    total_snow[i] = 0
                    melt[i] = melt[i-1] + df.t2_debias[i]*ddf_i
    return df.index, melt, total_rain, total_snow
