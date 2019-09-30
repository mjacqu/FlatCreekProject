import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools
import seaborn


'''
- Calculate superelevation and resulting flow velociteis using trimline elevations
    in different years from digitized trimlines.

    Velocity from superelevation:
    # u_superelev = np.sqrt(R*g*np.sin(beta))
    # u_superelev = velocity from superelevation
    # R = Radius
    # g = gravitational acceleration
    # beta = superelevation angle between the width of the two trimlines and the
        delta-H (dH, elevation difference between trimlines). Calculate as
        np.arctan(float(dH)/width)
    # Based on: https://www.researchgate.net/publication/271715192_Debris-flow_velocities_and_superelevation_in_a_curved_laboratory_channel/figures

- Calculate runup velocities of West Hill based on multiple profiles digitized
    from DEMS that reach from the river over the summit of West Hill.
'''

in_file = '/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/TerrainAnalysis/trimline_elevations.csv'
elevations = pd.read_csv(in_file, ',', header = 1 ,
                        names = ['dist_2013e','Easting_2013e', 'Northing_2013e', 'H_2013e', 'dist_2013w','Easting_2013w', 'Northing_2013w', 'H_2013w',
                                'dist_2015e','Easting_2015e', 'Northing_2015e', 'H_2015e', 'dist_2015w','Easting_2015w', 'Northing_2015w', 'H_2015w'])


# Super-elevation 2015 (take mean between boundaries 1 and 2 which correspond
# to main superelevation sites in the fiel.)
boundary1 = [1100, 1300]
boundary2 = [1300, 1500]
boundary3 = [1500, 1700]
boundary4 = [1700, 1900]
boundary5 = [1900, 2100]
superelev2015_E1 = elevations.H_2015e[(elevations.dist_2015e > boundary1[0])& (elevations.dist_2015e < boundary1[1])].mean()
superelev2015_W1 = elevations.H_2015w[(elevations.dist_2015w > boundary1[0])& (elevations.dist_2015w < boundary1[1])].mean()
superelev2015_E2 = elevations.H_2015e[(elevations.dist_2015e > boundary2[0])& (elevations.dist_2015e < boundary2[1])].mean()
superelev2015_W2 = elevations.H_2015w[(elevations.dist_2015w > boundary2[0])& (elevations.dist_2015w < boundary2[1])].mean()
superelev2015_E3 = elevations.H_2015e[(elevations.dist_2015e > boundary3[0])& (elevations.dist_2015e < boundary3[1])].mean()
superelev2015_W3 = elevations.H_2015w[(elevations.dist_2015w > boundary3[0])& (elevations.dist_2015w < boundary3[1])].mean()
superelev2015_E4 = elevations.H_2015e[(elevations.dist_2015e > boundary4[0])& (elevations.dist_2015e < boundary4[1])].mean()
superelev2015_W4 = elevations.H_2015w[(elevations.dist_2015w > boundary4[0])& (elevations.dist_2015w < boundary4[1])].mean()
superelev2015_E5 = elevations.H_2015e[(elevations.dist_2015e > boundary5[0])& (elevations.dist_2015e < boundary5[1])].mean()
superelev2015_W5 = elevations.H_2015w[(elevations.dist_2015w > boundary5[0])& (elevations.dist_2015w < boundary5[1])].mean()
superelev2015_lenE1 = len(elevations.H_2015e[(elevations.dist_2015e > boundary1[0])& (elevations.dist_2015e < boundary1[1])])
superelev2015_lenW1 = len(elevations.H_2015w[(elevations.dist_2015w > boundary1[0])& (elevations.dist_2015w < boundary1[1])])
superelev2015_lenE2 = len(elevations.H_2015e[(elevations.dist_2015e > boundary2[0])& (elevations.dist_2015e < boundary2[1])])
superelev2015_lenW2 = len(elevations.H_2015w[(elevations.dist_2015w > boundary2[0])& (elevations.dist_2015w < boundary2[1])])
superelev2015_lenE3 = len(elevations.H_2015e[(elevations.dist_2015e > boundary3[0])& (elevations.dist_2015e < boundary3[1])])
superelev2015_lenW3 = len(elevations.H_2015w[(elevations.dist_2015w > boundary3[0])& (elevations.dist_2015w < boundary3[1])])
superelev2015_lenE4 = len(elevations.H_2015e[(elevations.dist_2015e > boundary4[0])& (elevations.dist_2015e < boundary4[1])])
superelev2015_lenW4 = len(elevations.H_2015w[(elevations.dist_2015w > boundary4[0])& (elevations.dist_2015w < boundary4[1])])
superelev2015_lenE5 = len(elevations.H_2015e[(elevations.dist_2015e > boundary5[0])& (elevations.dist_2015e < boundary5[1])])
superelev2015_lenW5 = len(elevations.H_2015w[(elevations.dist_2015w > boundary5[0])& (elevations.dist_2015w < boundary5[1])])


#plot trim lines and means
fig = plt.figure(figsize = (15,3))
plt.plot(elevations.dist_2015e, elevations.H_2015e, label = '2015 East', color = 'skyblue')
plt.plot(elevations.dist_2015w, elevations.H_2015w, label = '2015 West', color = 'orange')
plt.plot(elevations.dist_2015e[(elevations.dist_2015e > boundary1[0])& (elevations.dist_2015e < boundary1[1])],
         np.ones(superelev2015_lenE1)*superelev2015_E1, 'darkblue', label = '2015 East Mean 1')
plt.plot(elevations.dist_2015w[(elevations.dist_2015w > boundary1[0])& (elevations.dist_2015w < boundary1[1])],
         np.ones(superelev2015_lenW1)*superelev2015_W1, 'red', label = '2015 West Mean 1')
plt.plot(elevations.dist_2015e[(elevations.dist_2015e > boundary2[0])& (elevations.dist_2015e < boundary2[1])],
         np.ones(superelev2015_lenE2)*superelev2015_E2, 'darkblue', label = '2015 East Mean 2')
plt.plot(elevations.dist_2015w[(elevations.dist_2015w > boundary2[0])& (elevations.dist_2015w < boundary2[1])],
         np.ones(superelev2015_lenW2)*superelev2015_W2, 'red', label = '2015 West Mean 2')
plt.plot(elevations.dist_2015e[(elevations.dist_2015e > boundary3[0])& (elevations.dist_2015e < boundary3[1])],
         np.ones(superelev2015_lenE3)*superelev2015_E3, 'darkblue', label = '2015 East Mean 1')
plt.plot(elevations.dist_2015w[(elevations.dist_2015w > boundary3[0])& (elevations.dist_2015w < boundary3[1])],
         np.ones(superelev2015_lenW3)*superelev2015_W3, 'red', label = '2015 West Mean 1')
plt.plot(elevations.dist_2015e[(elevations.dist_2015e > boundary4[0])& (elevations.dist_2015e < boundary4[1])],
         np.ones(superelev2015_lenE4)*superelev2015_E4, 'darkblue', label = '2015 East Mean 1')
plt.plot(elevations.dist_2015w[(elevations.dist_2015w > boundary4[0])& (elevations.dist_2015w < boundary4[1])],
         np.ones(superelev2015_lenW4)*superelev2015_W4, 'red', label = '2015 West Mean 1')
plt.plot(elevations.dist_2015e[(elevations.dist_2015e > boundary5[0])& (elevations.dist_2015e < boundary5[1])],
         np.ones(superelev2015_lenE5)*superelev2015_E5, 'darkblue', label = '2015 East Mean 1')
plt.plot(elevations.dist_2015w[(elevations.dist_2015w > boundary5[0])& (elevations.dist_2015w < boundary5[1])],
         np.ones(superelev2015_lenW5)*superelev2015_W5, 'red', label = '2015 West Mean 1')
plt.legend()
plt.show()

# Calculate and plot (boxplot) superelevation based on equations described above
dH = [superelev2015_E1 - superelev2015_W1, superelev2015_E2 - superelev2015_W2,
        superelev2015_E3 - superelev2015_W3, superelev2015_E4 - superelev2015_W4,
        superelev2015_E5 - superelev2015_W5]
g = 9.81 #ms^-2
C_est = [ 14.2, 11.7, 13.1, 12.1, 8.49, 5.98 ] # circumference of circles R2-R7 drawn in Google Earth and saved as kmz files
R_est = [(x*1000)/(2*np.pi) for x in C_est]
width = [760, 650, 538, 615, 886, 792]
beta = [(float(dH)/width) for dH, width in itertools.product(dH,width)] # all possible beta parameters

u_superelevation2015 = [np.sqrt(R*g*beta) for R,beta in itertools.product(R_est,beta)]

boxplot = plt.boxplot(u_superelevation2015)
[item.get_ydata() for item in boxplot['whiskers']]
plt.title('2015 Superelevation Velocities')
plt.show()

# ### Velocity from runup 2015

runup_2015 = '/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/TerrainAnalysis/runup_velocities2015.csv'

runup_2015 = pd.read_csv(runup_2015, header = 0, names = ['1','2','3','4','5','6','7','8','9','10'])
hill_height = [runup_2015.max() - runup_2015.min()]
mean_hill_height = np.mean(hill_height)
u_hill2015 = [np.sqrt(2*g*h) for h in hill_height]

boxplot = plt.boxplot(u_hill2015)
[item.get_ydata() for item in boxplot['whiskers']]
plt.title('2015 Runup Velocities')
plt.show()

# ### Velocity from runup 2013

runup_2013 = '/Users/mistral/Documents/CUBoulder/Science/Sulzer/data/TerrainAnalysis/runup_velocities2013.csv'

runup_2013 = pd.read_csv(runup_2013, header = 0, names = ['1','2','3','4','5','6','7','8','9','10'])
hill_height = [runup_2013.max() - runup_2013.min()]
mean_hill_height = np.mean(hill_height)
u_hill2013 = [np.sqrt(2*g*h) for h in hill_height]

boxplot = plt.boxplot(u_hill2013)
[item.get_ydata() for item in boxplot['whiskers']]
plt.title('2013 Runup Velocities')
plt.show()

# ### Super-elevation 2013

superelev2013_E = elevations.H_2013e[(elevations.dist_2013e > 600)& (elevations.dist_2013e < 1300)].mean()
superelev2013_W = elevations.H_2013w[(elevations.dist_2013w > 600)& (elevations.dist_2013w < 1300)].mean()
superelev2013_lenE = len(elevations.H_2013e[(elevations.dist_2013e > 600)& (elevations.dist_2013e < 1300)])
superelev2013_lenW = len(elevations.H_2013w[(elevations.dist_2013w > 600)& (elevations.dist_2013w < 1300)])


fig = plt.figure(figsize = (15,5))
plt.plot(elevations.dist_2013e, elevations.H_2013e, label = '2013 East', color = 'skyblue')
plt.plot(elevations.dist_2013w, elevations.H_2013w, label = '2013 West', color = 'orange')
plt.plot(elevations.dist_2013e[(elevations.dist_2013e > 600)& (elevations.dist_2013e < 1300)],
         np.ones(superelev2013_lenE)*superelev2013_E, 'darkblue', label = '2013 East Mean')
plt.plot(elevations.dist_2013w[(elevations.dist_2013w > 600)& (elevations.dist_2013w < 1300)],
         np.ones(superelev2013_lenW)*superelev2013_W, 'r', label = '2013 West Mean')
plt.legend()
plt.show()


# #### No superelevation in case of the 2013 flow because the "super-elevation" is opposite to the expected pattern (i.e. where it turns left at West Hill, the eastern elevation is lower).

# Velocity estimation from seismic data:
# 2013
est_time13 = [305, 280, 415, 390] #duration in seconds estimated visually from seismic data
est_dist13 = [9.26, 10.35] #estimated travel distances
seismic_vel_2013 = [(l*1000)/t for l,t in itertools.product(est_dist13,est_time13)]

# 2015
est_time15 = [290, 350] #duration in seconds estimated visually from seismic data
est_dist15 = [11.58] #estimated travel distances in km
seismic_vel_2015 = [(l*1000)/t for l,t in itertools.product(est_dist15,est_time15)]

# plot with all velocity box subplots
all_vel = {'2013 runup' : np.array(u_hill2013[0]), '2013 seismic' : np.array(seismic_vel_2013), '2015 runup' : np.array(u_hill2015[0]),
            '2015 seismic' : np.array(seismic_vel_2015), '2015 superelevation' : np.array(u_superelevation2015)}
vel_overview = pd.DataFrame({key:pd.Series(value) for key, value in all_vel.items()})

ax = plt.subplots(figsize=(8, 4))
ax = seaborn.boxplot(data=vel_overview, palette="hls")
ax = seaborn.swarmplot(data=vel_overview, color="0", alpha = '0.7')
plt.ylabel('Velocity [m/s]')
plt.show()
