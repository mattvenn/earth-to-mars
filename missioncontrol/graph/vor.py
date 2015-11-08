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

for p_num in range(3,len(points)):
    print("frame %03d of %d" % (p_num, len(points)))
    # compute Voronoi tesselation
    vor = Voronoi(points[0:p_num])

    #fig = plt.figure()
    fig = voronoi_plot_2d(vor)

    # limits
    plt.xlim(0,640)
    plt.ylim(0,400)

    # colorize
    for region, num_reg in zip(vor.regions, range(len(vor.regions))):
        if not -1 in region:
            polygon = [vor.vertices[i] for i in region]
            if len(polygon):
                pr = list(vor.point_region)
                p = pr.index(num_reg)
                color = data[p]['c']
                plt.fill(*zip(*polygon), color=color)

    #plt.show()
    fig.savefig("frames/%04d.png" % p_num)
    plt.close(fig)

"""
mencoder mf://*.png -mf w=640:h=400:fps=5:type=png -ovc lavc -lavcopts vcodec=mpeg4:mbd=2:trell -oac copy -o output.avi
"""
