import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from scipy import stats
import numpy.polynomial.polynomial as poly
import VariousFunctions_FC

'''
Run water availability caclulation for ARU at hourly resolution.
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


# Correct temperature data
ERA_elev = 1948
calc_elev = 2200
lapse_rate = 0.006
FC_hourly['t2_lapse'] = FC_hourly.t2  + ((ERA_elev - calc_elev) * lapse_rate) #lapse rate of 0.6K per 100m as in Kääb et al., 2018

# temperature de-biasing
reg_coefs = [1.4781479 , 1.8307034 , 0.02481807] #coefficients from correction for max temp from FlatCreekMeteo-datetimeindex.ipynb
FC_hourly['t2_debias'] = reg_coefs[2]*FC_hourly.t2_lapse**2 + reg_coefs[1]*FC_hourly.t2_lapse + reg_coefs[0]

# Hourly melt model
df = FC_hourly
ddf_i = 4.87/24
ddf_s = 2.7/24
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


#aggregate in data frame
FC_hourly['melt'] = melt
FC_hourly['tot_rain'] = total_rain
FC_hourly['tot_snow'] = total_snow
FC_hourly['total_water'] = FC_hourly['melt'] + FC_hourly['tot_rain']

# #### Group by months: water
FC_Summer = FC_hourly[(FC_hourly.index.month==4) | (FC_hourly.index.month==5) | (FC_hourly.index.month==6) | (FC_hourly.index.month==7)]
FC_water_availability = FC_hourly.groupby(FC_hourly.index.year).total_water.max()
FC_water_availability_summer = (FC_Summer.groupby(FC_Summer.index.year).total_water.max()
                                - FC_Summer.groupby(FC_Summer.index.year).total_water.min())
FC_melt_summer = (FC_Summer.groupby(FC_Summer.index.year).melt.max()
                  - FC_Summer.groupby(FC_Summer.index.year).melt.min())

FC_summer_water_trend = get_trend(FC_water_availability_summer,1)


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
get_std(FC_water_availability_summer,2013)
get_std(FC_water_availability_summer,2014)
get_std(FC_water_availability_summer,2015)

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
