import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from scipy import stats
import numpy.polynomial.polynomial as poly
import VariousFunctions_FC

'''
Run water availability caclulation for Flat Creek at hourly resolution.
'''

# load hourly data and set indecies and time zones
path = '/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/meteo/'
FC_hourly = pd.read_csv(path + 'ERA_t2_hourly_GMT-8_FlatCreek.csv')
FC_hourly_pcpt = pd.read_csv(path + 'ERA_pcpt_hourly_UTC_FlatCreek.csv', usecols = ['time','pcpt'])
#set time zone (already AK time) and set index
FC_hourly.time = pd.to_datetime(FC_hourly.time)
FC_hourly = FC_hourly.set_index('time').tz_localize(None)

FC_hourly_pcpt.time = pd.to_datetime(FC_hourly_pcpt.time)
FC_hourly_pcpt = FC_hourly_pcpt.set_index('time').tz_localize('GMT').tz_convert('Etc/GMT+8')
FC_hourly_pcpt.index = FC_hourly_pcpt.index.tz_localize(None)

FC_hourly['pcpt'] = FC_hourly_pcpt.pcpt

Summer_Water = pd.DataFrame()

# Correct temperature data

# temperature de-biasing
reg_coefs = [0.01647073,  1.68824293, -0.28782617] #coefficients from correction for max temp from FlatCreekMeteo-datetimeindex.ipynb
FC_hourly['t2_debias'] = reg_coefs[0]*np.square(FC_hourly.t2) + reg_coefs[1]*FC_hourly.t2 + reg_coefs[2]
ERA_elev = 1948

#calc_elev = 2700
calc_elevations = 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700 #to cycle through all elevation bands
for e in calc_elevations:
    lapse_rate = 0.006
    FC_hourly['t2_lapse'] = FC_hourly.t2_debias + ((ERA_elev - e) * lapse_rate) #lapse rate of 0.6K per 100m as in Kääb et al., 2018
    # Hourly melt model
    df = FC_hourly
    ddf_i = 4.87/24
    ddf_s = 2.7/24
    water_hourly = VariousFunctions_FC.water_availability(df, ddf_i, ddf_s)
    print(e)
    #aggregate into original data frame
    FC_hourly['melt'] = water_hourly['melt']
    FC_hourly['tot_rain'] = water_hourly['tot_rain']
    FC_hourly['tot_snow'] = water_hourly['tot_snow']
    FC_hourly['total_water'] = FC_hourly['melt'] + FC_hourly['tot_rain']
    # #### Group by months: water
    FC_Summer = FC_hourly[(FC_hourly.index.month==4) | (FC_hourly.index.month==5) | (FC_hourly.index.month==6) | (FC_hourly.index.month==7)]
    FC_water_availability = FC_hourly.groupby(FC_hourly.index.year).total_water.max()
    FC_water_availability_summer = (FC_Summer.groupby(FC_Summer.index.year).total_water.max()
                                    - FC_Summer.groupby(FC_Summer.index.year).total_water.min())
    FC_melt_summer = (FC_Summer.groupby(FC_Summer.index.year).melt.max()
                      - FC_Summer.groupby(FC_Summer.index.year).melt.min())
    FC_summer_water_trend = VariousFunctions_FC.get_trend(FC_water_availability_summer,1)
    Summer_Water[str(e)] = FC_water_availability_summer


# Plot water availability
fig, ax = plt.subplots(figsize = (18,7))
plt.plot(FC_water_availability_summer, '.--', color = 'black', label = 'Total water', markersize=10)
plt.plot(FC_melt_summer,'.--', color = 'orange', label = 'Water from melt', markersize=10)
plt.plot((FC_Summer.groupby(FC_Summer.index.year).tot_rain.max() - FC_Summer.groupby(FC_Summer.index.year).tot_rain.min()),
         '.--', color = 'blue', label ='Water from rain', markersize=10)
plt.plot(FC_water_availability_summer.index, FC_summer_water_trend[0],'grey', label = 'Water trend')
#plt.bar(snowpack.index[1:], snowpack.winter[1:], color = 'lightblue',
#       label = 'Winter snowpack (Oct - Mar)')
plt.title('Total water availability from rain and melt at Flat Creek (April - July)', fontsize = 20)
ax.tick_params('both', labelsize = 15)
plt.xlabel('Years', fontsize = 18)
plt.ylabel('Water availability [mm]', fontsize = 18)
plt.legend(fontsize = 12)
plt.show()
#plt.savefig('Total_water_April_July.png')

# Get standard deviation from long term mean for different years
VariousFunctions_FC.get_std(FC_water_availability_summer,2013)
VariousFunctions_FC.get_std(FC_water_availability_summer,2014)
VariousFunctions_FC.get_std(FC_water_availability_summer,2015)

#Get individual values
FC_water_availability_summer[FC_water_availability_summer.index == 2015].values

#Write to file
FC_water_availability_summer.to_csv('FC_Water_Apr_Jul_2200m.csv', header = True)
FC_melt_summer.to_csv('FC_melt_apr_jul_2200m.csv', header = True)


# Check for melt in 2012
FC_hourly2012 = FC_hourly[FC_hourly.index.year == 2012]
FC_hourly201208_201209 = FC_hourly2012[FC_hourly2012.index.month == 9]

plt.plot((FC_hourly201208_201209.groupby(FC_hourly201208_201209.index.day).melt.max()
- FC_hourly201208_201209.groupby(FC_hourly201208_201209.index.day).melt.min()), '.:')
plt.show()
