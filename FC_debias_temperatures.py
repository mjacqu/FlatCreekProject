import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
from scipy import stats
from VariousFunctions_FC import get_trend

'''
Explore chisana snotel data and downscaled ERA interim data. De-bias ERA interim
against chisana snotel data.
'''

path = '/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/meteo/'
# import chisana snotel data
chisana = pd.read_csv(path + 'ChisanaMeteo.csv',header=None,
                      names = ['date','P_cum','T_avg','T_max','T_min','T_obs','pcpt'],na_values=['-99.900000000000006'])

#set date format and index
chisana['date'] = pd.to_datetime(chisana['date'], format='%d/%m/%y')
chisana = chisana.set_index('date')

# define detachment event dates
event_date2015 = np.datetime64('2015-07-31')
event_date2013 = np.datetime64('2013-08-05')

#range for plotting
chisana2013 = pd.date_range(start = '2013-05-01', end = '2013-10-31')
chisana2015 = pd.date_range(start = '2015-05-01', end = '2015-10-31')


# import ERA interim data for Flat Creek Glacier and Chisana
#FlatCreekERA = pd.read_csv('data-glacier.csv',',',header=1, names = ['date','T_avg','P_inc'])
#ChisanaERA = pd.read_csv('data-station.csv',',',header=1, #names = ['date','T_avg','P_inc'])
FC_daily_pcpt = pd.read_csv(path + 'pcpt_daily_GMT-8_FlatCreek.csv', index_col = 'date')
CS_daily_pcpt = pd.read_csv(path + 'pcpt_daily_GMT-8_Chisana.csv', index_col = 'date')
FC_daily_t2 = pd.read_csv(path + 't2_daily_GMT-8_FlatCreek.csv', index_col = 'date')
CS_daily_t2 = pd.read_csv(path + 't2_daily_GMT-8_Chisana.csv', index_col = 'date')

#combine data and set index
FlatCreekERA = pd.concat([FC_daily_pcpt, FC_daily_t2], axis = 1)
ERAChisana = pd.concat([CS_daily_pcpt, CS_daily_t2], axis = 1)
FlatCreekERA.index = pd.to_datetime(FlatCreekERA.index)
ERAChisana.index = pd.to_datetime(ERAChisana.index, format = '%Y-%m-%d')

# Elevation corrections
chisana_snotel_elev = 1011.9 #m
ChisanaERA_elev = 1586.5 #m
glacier_elev = 2215 #m
FlatCreekERA_elev = 1948 #m
lapse_rate = 6.0*10**(-3)  #degrees per m
Chisana_lapse = (ChisanaERA_elev-chisana_snotel_elev)*lapse_rate
FC_lapse = (FlatCreekERA_elev - glacier_elev)*lapse_rate

# Plot snotel Data and Events
fig = plt.figure(figsize=(10,5))
plt.plot(chisana['pcpt'], 'b')
plt.plot(chisana['T_avg'],'r')
plt.xlabel('Date')
plt.ylabel('Precipitation [mm]',fontsize=16)
plt.title('Chisana SNOTEL (1012 m asl)',fontsize=16)
plt.show()

fig = plt.figure(figsize=(10,5))
plt.bar(chisana.loc[chisana2013].index, chisana.loc[chisana2013].pcpt, width = 2, color = 'blue')
plt.plot(chisana.loc[chisana2013].T_max, 'r')
plt.plot(chisana.loc[chisana2013].T_min, 'orange')
plt.axvline(event_date2013, color='black')
plt.xlabel('Date', fontsize=16)
plt.ylabel('Temperature [°C]', fontsize=16)
plt.title('Summer 2013: Chisana SNOTEL (1012 m asl)', fontsize=16)
plt.show()

fig = plt.figure(figsize=(15,5))
plt.bar(chisana.loc[chisana2015].index, chisana.loc[chisana2015].pcpt, width = 2, color = 'blue')
plt.plot(chisana.loc[chisana2015].T_max,'r')
plt.plot(chisana.loc[chisana2015].T_min,'orange')
plt.axvline(event_date2015,color='black')
plt.xlabel('Date',fontsize=16)
plt.ylabel('Temperature [°C]',fontsize=16)
plt.title('Summer 2015: Chisana SNOTEL (1012 m asl)',fontsize=16)
plt.show()

################################################
#De-bias against station data. Temperature only.
################################################
# Apply lapse rate correction
FlatCreekERA['mean_lapse'] = FlatCreekERA.T_mean + FC_lapse
ERAChisana['mean_lapse'] = ERAChisana.T_mean + Chisana_lapse
FlatCreekERA['min_lapse'] = FlatCreekERA.T_min + FC_lapse
ERAChisana['min_lapse'] = ERAChisana.T_min + Chisana_lapse
FlatCreekERA['max_lapse'] = FlatCreekERA.T_max + FC_lapse
ERAChisana['max_lapse'] = ERAChisana.T_max + Chisana_lapse

#data where snotel and ERA overlaps
overlap = pd.date_range(start ='2008-07-16', end = '2015-10-29')

fig = plt.figure(figsize=(8, 8))
plt.scatter(ERAChisana.loc[overlap].T_mean, chisana.loc[overlap].T_avg, label = 'original')
plt.scatter(ERAChisana.loc[overlap].mean_lapse, chisana.loc[overlap].T_avg, label = 'Chisana lapse rate corrected')
#plt.scatter(FlatCreekERA.loc[overlap].mean_lapse, chisana.loc[overlap].T_avg, label = 'FlatCreek lapse rate corrected')
#plt.scatter(FlatCreekERA.loc[overlap].mean_lapse, ERAChisana.loc[overlap].mean_lapse, label = 'ERA-ERA')
plt.plot((-40, 40), (-40, 40),'k')
plt.xlim(-50, 20)
plt.ylim(-50, 20)
plt.xlabel('x')
plt.ylabel('y')
plt.title('ChisanaERA vs Chisana station (lapse rate corrected)')
plt.legend()
plt.show()
#plt.savefig('OriginalDataScatter.png')

# fit linear regression function to lapse-rate corrected vs. snotel data
# 1. for daily mean temperature
a = np.array(ERAChisana.loc[overlap].mean_lapse)
b = np.array(chisana.loc[overlap].T_avg)
nanidx = np.isfinite(a) & np.isfinite(b)
coefs = stats.linregress(a[nanidx], b[nanidx])
print('regression coefficients: '+ str(coefs))
plt.plot(a, b, 'o')
#plt.plot(a, coefs[2]*pow(a,2) + coefs[1]*a + coefs[0],'.') #quadratic function
plt.plot(a, coefs[0]*a + coefs[1],'.')
plt.show()

# 2. then for daily maximum temperature
a = np.array(ERAChisana.loc[overlap].max_lapse)
b = np.array(chisana.loc[overlap].T_max)
nanidx = np.isfinite(a) & np.isfinite(b)
max_coefs = stats.linregress(a[nanidx], b[nanidx])
print('regression coefficients: '+ str(max_coefs))
plt.plot(a, b, 'o')
#plt.plot(a, max_coefs[2]*pow(a,2) + max_coefs[1]*a + max_coefs[0],'.') #quadratic function
plt.plot(a, max_coefs[0]*a + max_coefs[1],'.')
plt.show()


# apply linear function derived above to lapse rate corrected data for both Chisana and Flat Creek
####### Mean Temp #########
ERAChisana['mean_debias'] = coefs[0]*ERAChisana.mean_lapse + coefs[1]
FlatCreekERA['mean_debias'] = coefs[0]*FlatCreekERA.mean_lapse + coefs[1]

# apply linear function derived above to lapse rate corrected data for both Chisana and Flat Creek
##### MAX Temp ###########
ERAChisana['max_debias'] = max_coefs[0]*ERAChisana.max_lapse + max_coefs[1]
FlatCreekERA['max_debias'] = max_coefs[0]*FlatCreekERA.max_lapse + max_coefs[1]

#ERAChisana['max_debias'] = max_coefs[2]*ERAChisana.max_lapse**2 + max_coefs[1]*ERAChisana.max_lapse + max_coefs[0]
#FlatCreekERA['max_debias'] = max_coefs[2]*FlatCreekERA.max_lapse**2 + max_coefs[1]*FlatCreekERA.max_lapse + max_coefs[0]


fig = plt.figure(figsize=(8, 8))
plt.scatter(ERAChisana.loc[overlap].max_lapse, chisana.loc[overlap].T_max, label = 'Lapse rate corrected')
plt.scatter(ERAChisana.loc[overlap].max_debias, chisana.loc[overlap].T_max, label = 'Bias corrected')
#plt.scatter(FlatCreekERA.loc[overlap].max_debias, chisana.loc[overlap].T_max,label = 'FlatCreek de-biased')
#plt.scatter(ERAChisana.loc[overlap].max_debias, FlatCreekERA.loc[overlap].max_debias, label = 'ERA-ERA')
plt.plot((-40, 40), (-40, 40),'k')
plt.xlim(-50, 20)
plt.ylim(-50, 20)
plt.xlabel('ERA')
plt.ylabel('station')
plt.title('ChisanaERA vs Chisana station')
plt.legend()
plt.show()
#plt.savefig('Temperature_corrected.png')

# Calculate Mean Annual values
ERAFlatCreek_mean_annual = FlatCreekERA.groupby([FlatCreekERA.index.year]).mean()
ERAChisana_mean_annual = ERAChisana.groupby([ERAChisana.index.year]).mean()
chisana_mean_annual = chisana.groupby([chisana.index.year]).mean()

x, y, z = ERAFlatCreek_mean_annual, ERAChisana_mean_annual, chisana_mean_annual
x.index, y.index, z.index =[pd.to_datetime(i.index, format = '%Y') for i in (x, y, z) ]

# vectors for plotting
ERA_vec = np.linspace(1,len(ERAFlatCreek_mean_annual.mean_debias.values),
                      num = len(ERAFlatCreek_mean_annual.mean_debias.values))
snotel_vec = np.linspace(1,len(chisana_mean_annual.T_avg.values),
                         num = len(chisana_mean_annual.T_avg.values))


# Mean Annual Air Temperature
FC_MAAT = stats.linregress(ERA_vec, ERAFlatCreek_mean_annual.mean_debias)
CS_MAAT = stats.linregress(ERA_vec, ERAChisana_mean_annual.mean_debias)
chisana_MAAT = stats.linregress(snotel_vec[1:-1],chisana_mean_annual.T_avg[1:-1])
print(FC_MAAT)
print(CS_MAAT)
print(chisana_MAAT)

# ERA yearly difference to mean (1979-1999)
x, y = ERAFlatCreek_mean_annual, ERAChisana_mean_annual
ERAmean_range = pd.date_range(start = '1979-01-01', end ='1981-01-01')
x.ERA_resid, y.ERA_resid = [i.mean_debias - i.loc[ERAmean_range].mean_debias.mean() for i in (x, y)]

fig = plt.figure(figsize=(10, 5))
plt.plot(x.ERA_resid, ':.', label = 'Flat Creek')
plt.plot(y.ERA_resid, ':.', label = 'Chisana')
plt.legend()
plt.show()

# Total positive degree days
chisana['pos_deg'] = chisana.T_max.gt(0)
station_Pos_Deg_Sum = chisana.groupby(chisana.index.year).pos_deg.sum()
station_Pos_Deg_Mean = station_Pos_Deg_Sum.mean()

chis_trend, chis_slope, chis_nrmse = get_trend(station_Pos_Deg_Sum[1:-1],1)

fig = plt.figure(figsize=(12,4))
plt.plot(station_Pos_Deg_Sum[1:-1],'.:r')
plt.plot(station_Pos_Deg_Sum.index[1:-1],chis_trend,'k')
plt.xlabel('Date')
plt.ylabel('Positive Degree Days Per Year',fontsize=16)
plt.title('Trend of Positive Degree Days @ Chisana Snotel',fontsize=16)
plt.show()
#plt.savefig('MAAT_trend.png',transparent=False, bbox_inches='tight',pad_inches=0.4)

FlatCreekERA['pos_deg'] = FlatCreekERA.max_debias.gt(0)
ERAChisana['pos_deg'] = ERAChisana.max_debias.gt(0)

FC_Pos_Deg_Sum = FlatCreekERA.groupby(FlatCreekERA.index.year).pos_deg.sum()
CS_Pos_Deg_Sum = ERAChisana.groupby(ERAChisana.index.year).pos_deg.sum()
FC_Pos_Deg_Mean = FC_Pos_Deg_Sum.mean()
CS_Pos_Deg_Mean = CS_Pos_Deg_Sum.mean()

FCtrend, FCslope, FCnrmse = get_trend(FC_Pos_Deg_Sum,1)
CStrend, CSslope, CSnrmse = get_trend(CS_Pos_Deg_Sum,1)

fig = plt.figure(figsize=(15,4))
plt.plot(FC_Pos_Deg_Sum-FC_Pos_Deg_Mean,'.:r', label = 'Flat Creek ERA')
#plt.plot(FC_Pos_Deg_Sum.index,FCtrend,'k')
plt.plot(CS_Pos_Deg_Sum-CS_Pos_Deg_Mean,'.:b', label = 'Chisana ERA')
#plt.plot(CS_Pos_Deg_Sum.index,CStrend,'k')
plt.plot(station_Pos_Deg_Sum[1:-1]-station_Pos_Deg_Mean,'.:g', label = 'Chisana station' )
#plt.plot(station_Pos_Deg_Sum.index[1:-1],chis_trend,'k')
plt.legend(fontsize = 16)
plt.xlabel('Year',fontsize=18)
plt.ylabel('Deviation from Mean',fontsize=18)
plt.title('Positive Degree Days (PDD)',fontsize=18)
plt.show()
#plt.savefig('PDD_trend.png',transparent=False, bbox_inches='tight',pad_inches=0.4)


# Total positive degrees (not days)
FC_ispositive = FlatCreekERA[FlatCreekERA.pos_deg == True]
CS_ispositive = ERAChisana[ERAChisana.pos_deg == True]
chisana_ispositive = chisana[chisana.pos_deg == True]

x, y = FC_ispositive, CS_ispositive

chisana_totposdeg = chisana_ispositive.groupby(chisana_ispositive.index.year).T_max.sum()
ERA_totposdeg = [i.groupby(i.index.year).max_debias.sum() for i in (x, y) ]

FCtotposdeg_trend = get_trend(ERA_totposdeg[0],1)
CStotposdeg_trend = get_trend(ERA_totposdeg[1],1)
chis_totposdeg_trend = get_trend(chisana_totposdeg[1:-1],1)

fig = plt.figure(figsize=(15,4))
plt.plot(ERA_totposdeg[0],'.:r', label = 'Flat Creek ERA')
plt.plot(ERA_totposdeg[0].index,FCtotposdeg_trend[0],'k')
#plt.plot(ERA_totposdeg[1],'.:b', label = 'Chisana ERA')
#plt.plot(CS_Pos_Deg_Sum.index,CStrend,'k')
#plt.plot(chisana_totposdeg[1:-1],'.:g', label = 'Chisana station' )
#plt.plot(station_Pos_Deg_Sum.index[1:-1],chis_trend,'k')
plt.legend(fontsize = 16)
plt.xlabel('Year',fontsize=18)
plt.ylabel('Positive degrees',fontsize=18)
plt.title('Positive Degree Content',fontsize=18)
plt.show()

'''
#deprecated
f, (ax, ax2) = plt.subplots(2, 1, sharex=True, figsize=(15,5))
#plt.plot(totposdeg[0],'.:r', label = 'ERA Flat Creek')
#plt.plot(totposdeg[0].index, FCtotposdeg_trend[0],'k')
ax.plot(chisana_totposdeg[1:-1],'.:g', label = 'Chisana Snotel')
ax.plot(chisana_totposdeg[1:-1], chis_totposdeg_trend[0],'k')
ax2.plot(totposdeg[1],'.:b', label = 'ERA Chisana')
ax2.plot(totposdeg[1].index, CStotposdeg_trend[0],'k')
ax.set_ylim(1200, 1550)  # outliers only
ax2.set_ylim(100, 400)  # most of the data

ax.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax.xaxis.tick_top()
ax.tick_params(labeltop='off')  # don't put tick labels at the top
ax2.xaxis.tick_bottom()

d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
ax.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

ax.legend(fontsize = 16)
ax2.legend(fontsize = 16)

plt.xlabel('Year', fontsize = 16)
#plt.ylabel('Total positive degrees')
plt.suptitle('Total positive degrees available', fontsize = 18)
plt.show()
#plt.savefig('TotalDegrees.png',transparent=False, bbox_inches='tight',pad_inches=0.4)
'''

# Precipitation
x, y = FlatCreekERA, ERAChisana
chisana_tot_precip = chisana.groupby(chisana.index.year).pcpt.sum()
ERA_tot_precip = [i.groupby(i.index.year).pcpt.sum() for i in (x, y) ]
FC_preciptrend = get_trend(ERA_tot_precip[0],1)
CS_preciptrend = get_trend(ERA_tot_precip[1],1)
chisana_preciptrend = get_trend(chisana_tot_precip,1)

fig = plt.figure(figsize=(20,8))
plt.style.use('ggplot')
plt.plot(ERA_tot_precip[0],'.:r', color = 'royalblue', linewidth = 3, markersize = 12, label = 'ERA Flat Creek' )
plt.plot(ERA_tot_precip[1],'.:b', color = 'orange', linewidth = 3, markersize = 14, label = 'ERA Chisana' )
plt.plot(chisana_tot_precip[1:-2],'.:g', color = 'k', linewidth = 3, markersize = 12, label = 'Chisana SNOTEL' )
ax = plt.gca()
ax.tick_params('both', labelsize = 16)
plt.legend(fontsize = 20)
plt.xlabel('year', fontsize = 24)
plt.ylabel('Precipitation [mm]', fontsize = 24)
plt.title('Total Yearly Precipitation', fontsize = 24)
plt.show()


# Liquid water availability
x, y = FC_ispositive, CS_ispositive
xx, yy = FlatCreekERA, ERAChisana
ERA_totrain = [i.groupby(i.index.year).pcpt.sum() for i in (x, y) ]
ERA_totprecip = [i.groupby(i.index.year).pcpt.sum() for i in (xx, yy) ]
chisana_totrain = chisana_ispositive.groupby(chisana_ispositive.index.year).pcpt.sum()
chisana_totprecip = chisana.groupby(chisana.index.year).pcpt.sum()
FC_summertrend = get_trend(ERA_totrain[0],1)
CS_summertrend = get_trend(ERA_totrain[1],1)
#FC_lt2000 = get_trend(totwater_posdeg[0].loc[totwater_posdeg[0].index < 2000],1)
#FC_ge2000 = get_trend(totwater_posdeg[0].loc[totwater_posdeg[0].index >= 2000],1)
#CS_lt2000 = get_trend(totwater_posdeg[1].loc[totwater_posdeg[1].index < 2000],1)
#CS_ge2000 = get_trend(totwater_posdeg[1].loc[totwater_posdeg[1].index >= 2000],1)

fig = plt.figure(figsize=(15,5))
plt.plot(ERA_totrain[0],'.:r', label = 'ERA Flat Creek Summer')
plt.plot(ERA_totrain[1],'.:', color = 'orange', label = 'ERA Chisana Summer ')
#plt.plot(totwater_posdeg[0].index[totwater_posdeg[0].index < 2000], FC_lt2000[0],'k:', label = 'ERA FC trend < 2000')
#plt.plot(totwater_posdeg[0].index[totwater_posdeg[0].index >= 2000], FC_ge2000[0],'k', label = 'ERA FC trend >= 2000')
#plt.plot(totwater_posdeg[0].index, FC_summertrend[0],'grey')
#plt.plot(totwater_posdeg[0].index[totwater_posdeg[0].index < 2000], CS_lt2000[0],'b:', label = 'ERA CS trend < 2000')
#plt.plot(totwater_posdeg[0].index[totwater_posdeg[0].index >= 2000], CS_ge2000[0],'b', label = 'ERA CS trend >= 2000')
#plt.plot(totwater_posdeg[2].iloc[1:-1],'.:', color = 'purple', label = 'Chisana Snotel Summer')
#plt.plot(totwater_negdeg[2].iloc[1:-1],'.:', color = 'green', label = 'Chisana Snotel Winter')
plt.legend()
plt.xlabel('Year', fontsize = 16)
plt.ylabel('Total liquid water in mm', fontsize = 16)
plt.title('Precipitation in the form of rain (days > 0 deg. C) [mm]', fontsize = 18)
plt.show()
#plt.savefig('SummerRain.png',transparent=False, bbox_inches='tight',pad_inches=0.4)


# Fraction Rain to total precip ratio
FC_rain_ratio = ERA_totrain[0]/ERA_totprecip[0]
CS_rain_ratio = ERA_totrain[1]/ERA_totprecip[1]
chisana_rain_ratio = chisana_totrain/chisana_totprecip

fig = plt.figure(figsize=(15,5))
plt.plot(FC_rain_ratio, 'r.:')
plt.plot(CS_rain_ratio, 'b.:')
plt.xlabel('Year', fontsize = 16)
plt.ylabel('% ', fontsize = 16)
plt.title('Percent rain of total precipitation', fontsize = 18)
plt.show()

# Monthly statistics
FC_IsJuneJuly = FlatCreekERA[(FlatCreekERA.index.month==6) | (FlatCreekERA.index.month==7)]
FC_JuneRain = FC_IsJuneJuly.groupby(FC_IsJuneJuly.index.year).pcpt.sum()
CS_IsJuneJuly = ERAChisana[(ERAChisana.index.month==6) | (ERAChisana.index.month==7)]
CS_JuneRain = CS_IsJuneJuly.groupby(CS_IsJuneJuly.index.year).pcpt.sum()
snotel_IsJuneJuly = chisana[(chisana.index.month==6) | (chisana.index.month==7)]
snotel_JuneRain = snotel_IsJuneJuly.groupby(snotel_IsJuneJuly.index.year).pcpt.sum()

fig = plt.figure(figsize=(20,8))
plt.style.use('ggplot')
plt.plot(FC_JuneRain,'.:', color = 'royalblue', linewidth = 3, markersize = 12, label = 'ERA Flat Creek' )
plt.plot(CS_JuneRain,'.:', color = 'orange', linewidth = 3, markersize = 14, label = 'ERA Chisana' )
plt.plot(snotel_JuneRain[1:-2],'.:', color = 'k', linewidth = 3, markersize = 12, label = 'Chisana SNOTEL' )
plt.xlabel('Year', fontsize = 24)
plt.ylabel('Total liquid water in mm', fontsize = 24)
plt.title('Total rain for June and July [mm]', fontsize = 24)
ax = plt.gca()
ax.tick_params('both', labelsize = 16)
plt.legend(fontsize = 20)
plt.show()
#plt.savefig('Total_Rain_June_July.png')
