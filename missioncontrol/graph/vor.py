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
vor = Voronoi(points,furthest_site=False, incremental=False)

# plot
voronoi_plot_2d(vor)

# colorize
for region, num_reg in zip(vor.regions, range(len(vor.regions))):
    if not -1 in region:
        polygon = [vor.vertices[i] for i in region]
        if len(polygon):
#            point_index = vor.point_region[region]
            print vor.point_region[num_reg]
            plt.fill(*zip(*polygon), color=(0.5,0.5,0.5))

print vor.regions
print vor.point_region
print points
plt.show()
