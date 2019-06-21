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
