import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

df = pd.read_csv('/Users/mistral/Documents/CUBoulder/Science/Sulzer+/data/Temperature_data/2018_2019FlatCreekTemperatures.csv',
                skiprows = 2, usecols = [1,2,3,4,5], names = (['datetime', 'temp_0cm',
                'temp_25cm', 'temp_50cm', 'temp_75cm']))

df.datetime = pd.to_datetime(df.datetime)
df = df.set_index('datetime')

fig = plt.subplots(figsize=(12,5))
plt.plot(df.temp_0cm.loc['2018-07-06 16:00:00':], color = 'cornflowerblue', label = '0 cm')
plt.plot(df.temp_25cm.loc['2018-07-06 16:00:00':], color = 'royalblue', label = '25 cm')
plt.plot(df.temp_50cm.loc['2018-07-06 16:00:00':], color = 'blue', label = '50 cm')
plt.plot(df.temp_75cm.loc['2018-07-06 16:00:00':], color = 'black', label = '75 cm')
plt.legend()
plt.xlabel('Date')
plt.ylabel('Temperature [°C]')
plt.title('Flat Creek: Temperature at distance below surface')
plt.show()
plt.savefig('/Users/mistral/Documents/CUBoulder/Science/Sulzer+/data/Temperature_data/FlatCreekTemps.pdf')
