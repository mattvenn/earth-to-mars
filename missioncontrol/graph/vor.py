import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import random

# make up data points
data = []
for i in range(5):
    d = { 'xy':  (random.random(), random.random()),
        'c': random.random(),
        }
    data.append(d)
points = [d['xy'] for d in data]

# compute Voronoi tesselation
vor = Voronoi(points)

# plot
voronoi_plot_2d(vor)

# colorize
for region in vor.regions:
    if not -1 in region:
        polygon = [vor.vertices[i] for i in region]
        if len(polygon):
#            point_index = vor.point_region[region]
            plt.fill(*zip(*polygon), color=(0.5,0.5,0.5))

import ipdb; ipdb.set_trace()
plt.show()
