import numpy as np
import time
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import random

"""
# make up data points
data = []
for i in range(25):
    d = { 'xy':  (random.random(), random.random()),
        'c': random.random(),
        }
    data.append(d)
"""
import pickle
with open('data.pkl' ) as fh:
    data = pickle.load(fh)

points = [d['xy'] for d in data]

# compute Voronoi tesselation
vor = Voronoi(points)


# plot
#voronoi_plot_2d(vor)
plt.xlim(vor.min_bound[0] - 0.1, vor.max_bound[0] + 0.1)
plt.ylim(vor.min_bound[1] - 0.1, vor.max_bound[1] + 0.1)

# colorize
for region, num_reg in zip(vor.regions, range(len(vor.regions))):
    if not -1 in region:
        polygon = [vor.vertices[i] for i in region]
        if len(polygon):
#            point_index = vor.point_region[region]
            pr = list(vor.point_region)
            p = pr.index(num_reg)
            color = data[p]['c']
            plt.fill(*zip(*polygon), color=color)

plt.show()
