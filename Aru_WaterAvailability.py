import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import VariousFunctions_FC

'''
Run water avaiability model for Aru on ERA Interim time series.
'''

#load files
temp_file = '/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/Other_ERA/AruERA_t2.csv'
precip_file = '/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/Other_ERA/AruERA_pcpt.csv'
t2 = pd.read_csv(temp_file, header = None, names = (['datetime', 'T_K']), index_col = 'datetime')
pcpt = pd.read_csv(precip_file, header = None, names = (['datetime', 'pcpt']), index_col = 'datetime')

#set datetime index
t2.index = pd.to_datetime(t2.index, format = '%Y%m%d%H%S', utc = True)
pcpt.index = pd.to_datetime(pcpt.index, format = '%Y%m%d%H%S', utc = True)


# Modify datasets to be in degrees C and to ignore negative precip, apply
# lapse-rate correction to temperature.

#Aru: ERA_elev = 5100, calc elev = [5100,5800]
#Kolka: ERA_elev = 3300, calc elev = [3000,3300]
#Lenas: ERA_elev = 3200, calc elev = [3600,3800]
ERA_elev = 5100
calc_elev = 5400
lapse_rate = 0.006
t2['T_C'] = t2.T_K - 273.15 + ((ERA_elev - calc_elev) * lapse_rate) #lapse rate of 0.6K per 100m as in Kääb et al., 2018
pcpt.pcpt[pcpt.pcpt < 0] = 0
pcpt.pcpt = pcpt.pcpt*4 #based on same procedure as done by Kääb et al., 2018

# Generate daily mean and daily maximum temperature.
t2_daily = pd.DataFrame()
t2_daily['T_mean'] = t2.groupby(t2.index.date).T_C.mean()
t2_daily['T_max'] = t2.groupby(t2.index.date).T_C.max()
t2_daily.index = pd.to_datetime(t2_daily.index)

# Generate yearly mean temperature
t2_yearly = pd.DataFrame()
t2_yearly['T_mean'] = t2_daily.groupby(t2_daily.index.year).T_mean.mean()

'''
#Plot if desired
fig = plt.figure(figsize=(15,8))
plt.plot(t2_yearly.T_mean, '--*')
plt.title('Mean Annual Air Temperature', fontsize = 16)
plt.xlabel('Year', fontsize = 16)
plt.ylabel('Temperature', fontsize = 16)
plt.show()
'''

# Generate positive degree days
t2_daily['pos_deg'] = t2_daily.T_max.gt(0)
t2_yearly['pos_deg_count'] = t2_daily.groupby(t2_daily.index.year).pos_deg.sum()

'''
#Plot if desired
fig = plt.figure(figsize=(15,8))
plt.plot(t2_yearly.pos_deg_count, '*--')
plt.title('positive degree days', fontsize = 16)
plt.xlabel('Year', fontsize = 16)
plt.ylabel('# of days', fontsize = 16)
plt.show()
'''

# Generate positive degree content
Aru_ispositive = t2_daily[t2_daily.pos_deg == True]
t2_yearly['totposdeg'] = Aru_ispositive.groupby(Aru_ispositive.index.year).T_max.sum()

'''
fig = plt.figure(figsize=(15,8))
plt.plot(t2_yearly.totposdeg, '--*')
plt.title('Total Positive Degree content', fontsize = 16)
plt.xlabel('Year', fontsize = 16)
plt.ylabel('Total Temperature Content [°C]', fontsize = 16)
plt.show()
'''

# Generate Total daily precip
pcpt_daily = pd.DataFrame()
pcpt_daily['total'] = pcpt.groupby(pcpt.index.date).pcpt.sum()
pcpt_daily.index = pd.to_datetime(pcpt_daily.index)

# Generate total yearly precip
pcpt_yearly = pd.DataFrame()
pcpt_yearly['total'] = pcpt_daily.groupby(pcpt_daily.index.year).total.sum()

'''
fig = plt.figure(figsize=(15,8))
plt.plot(pcpt_yearly.total, '--*')
plt.title('Total Yearly Precip', fontsize = 16)
plt.xlabel('Year', fontsize = 16)
plt.ylabel('Precip [m]', fontsize = 16)
plt.show()
'''

# Prepare degree-day melt model
df = pd.DataFrame()
df['pcpt'] = pcpt_daily.total*100
pcpt_daily.index = pd.to_datetime(pcpt_daily.index)
df['t2_debias'] = t2_daily.T_mean

#Used degree day factors
#Aru ddf_i = 1, ddf_s = 2 (as per Kääb et al., 2018)
#Kolka ddf_i = 8, ddf_s = 5 (experimental)
#Lenas ddf_i = 4.5, ddf_s = 3.5 (experimental)
ddf_i = 1
ddf_s = 2
total_snow = np.zeros(len(df))
melt = np.zeros(len(df))
total_rain = np.zeros(len(df))
for i in range(0, len(df)):
    if df.index[i].month == 9 and df.index[i].day == 30: #reset at end of water year
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
df['melt'] = melt
df['rain'] = total_rain
df['snow'] = total_snow
df['total_water'] = df['melt'] + df['rain']

#Group by months
Aru_summer = df[ (df.index.month==4) |
                (df.index.month==5) | (df.index.month==6) |
                (df.index.month==7) | (df.index.month==8) | (df.index.month==9)]
Aru_water_availability = df.groupby(df.index.year).total_water.max()
Aru_water_availability_summer = (Aru_summer.groupby(Aru_summer.index.year).total_water.max()
                                - Aru_summer.groupby(Aru_summer.index.year).total_water.min())
Aru_melt_summer = (Aru_summer.groupby(Aru_summer.index.year).melt.max()
                   - Aru_summer.groupby(Aru_summer.index.year).melt.min())
Aru_rain_summer = (Aru_summer.groupby(Aru_summer.index.year).rain.max()
                   - Aru_summer.groupby(Aru_summer.index.year).rain.min())

# investigate trend
Aru_summer_water_trend = get_trend(Aru_water_availability_summer,1)

#plotting
g, ax = plt.subplots(figsize = (15,7))
#plt.plot(Aru_water_availability)
plt.plot(Aru_water_availability_summer, '.--', color = 'black', label = 'Total water', markersize=10)
plt.plot(Aru_melt_summer,'.--', color = 'orange', label = 'Water from melt', markersize=10)
#plt.plot(Aru_rain_summer,'.--', color = 'blue', label ='Water from rain', markersize=10)
plt.plot(Aru_water_availability_summer.index, Aru_summer_water_trend[0],'grey', label = 'Water trend')
#plt.bar(snowpack.index[1:], snowpack.winter[1:], color = 'lightblue',
#       label = 'Winter snowpack (Oct - Mar)')
plt.title('Total water availability from rain and melt at Aru (April - July)', fontsize = 20)
ax.tick_params('both', labelsize = 15)
plt.xlabel('Years', fontsize = 18)
plt.ylabel('Water availability [mm]', fontsize = 18)
plt.legend(fontsize = 12)
plt.show()
#plt.savefig('Total_water_April_July.png')


# Summer water deviation from long term mean
get_std(Aru_water_availability,2016)

## write to file
Aru_water_availability_summer.to_csv('Aru_5500m_apr_jul_wateravailability.csv', header = True)
Aru_melt_summer.to_csv('Aru_5500m_apr_jul_melt.csv', header = True)
