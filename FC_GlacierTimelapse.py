import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob
import os
import re

'''
Turn a set of .tif files into pngs with date stamped on for timelapse animation
'''

dir = os.getcwd()
lof = glob.glob(dir + "/*.tif")
lof.sort()

print(lof)

for i in range(0,len(lof)):
    date_search = re.search(r'20[0-2][0-9]-[0-1][0-9]-[0-3][0-9]',lof[i],)
    date = date_search.group(0)
    img=mpimg.imread(lof[i])
    fig = plt.figure(frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(img)
    plt.text(450, 80, date, fontsize = 16, fontweight = 'bold', color = 'cyan')
    plt.savefig('GlacierTL'+str(date), dpi=300, pad_inches = 0)
