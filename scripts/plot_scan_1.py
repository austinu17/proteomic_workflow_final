#!/usr/bin/env python

import os
import sys
import numpy as np
import pymzml
import matplotlib
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

mzml_file = sys.argv[1]
run = pymzml.run.Reader(mzml_file)

for n, spec in enumerate(run):


    print(spec.ID)
    print(spec['ms level'])
    print(spec['scan start time'])
    print(spec['base peak intensity'])
    print(spec.mz)
    print(spec.i)

    params = spec._get_encoding_parameters('mean inverse reduced ion mobility array')
    print(spec._decode(*params))
    
    break

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# Data for three-dimensional scattered points
zdata = spec._decode(*params)
xdata = spec.mz
ydata = spec.i
ax.scatter(xdata, ydata, zdata, c=zdata, cmap='Greens');

plt.savefig("{}.{}".format(sys.argv[1],'3D_plot.pdf'))
