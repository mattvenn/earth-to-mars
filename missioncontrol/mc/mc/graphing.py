import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi
import numpy as np
import math
from mc import app
from mc import db
from mc.models import Sample, GroupGraph

def map_color(value, min, max):
    # Figure out how 'wide' each range is
    sample_span = max - min
    out_span = 1

    # Convert the left range into a 0-1 range (float)
    scaled = float(value - min) / float(sample_span)
    return scaled

# this copied from /usr/lib/python2.7/dist-packages/scipy/spatial
# so I can avoid plotting the points
def voronoi_plot_2d(vor, ax=None):
    # add these 2 lines (provided by a scipy decorator) to get ax
    fig = plt.figure()
    ax = fig.gca()
    if vor.points.shape[1] != 2:
        raise ValueError("Voronoi diagram is not 2-D")

    ax.plot(vor.points[:,0], vor.points[:,1],'.')
    #ax.plot(vor.vertices[:,0], vor.vertices[:,1])

    for simplex in vor.ridge_vertices:
        simplex = np.asarray(simplex)
        if np.all(simplex >= 0):
            ax.plot(vor.vertices[simplex,0], vor.vertices[simplex,1], 'k-')

    ptp_bound = vor.points.ptp(axis=0)

    center = vor.points.mean(axis=0)
    for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
        simplex = np.asarray(simplex)
        if np.any(simplex < 0):
            i = simplex[simplex >= 0][0]  # finite end Voronoi vertex

            t = vor.points[pointidx[1]] - vor.points[pointidx[0]]  # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[pointidx].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[i] + direction * ptp_bound.max()

            ax.plot([vor.vertices[i,0], far_point[0]],
                    [vor.vertices[i,1], far_point[1]], 'k--')

    # don't adjust bounds!
    #_adjust_bounds(ax, vor.points)

    return ax.figure

def update_group_graph():
    maxx = app.config['MAX_X']
    maxy = app.config['MAX_Y']
    group = GroupGraph()
    db.session.add(group)

    samples = Sample.query.all()

    for name in app.config['SAMPLE_TYPES'].keys():
        app.logger.info("updating %s group graph using %d samples id %d" % (name, len(samples), group.id))
        config = app.config['SAMPLE_TYPES'][name]

        start_data = [ 
            Sample(x=-100, y=-100),
            Sample(x=maxx+100, y=-100),
            Sample(x=maxx+100, y=maxy+100),
            # 100.1 because of a bug
            Sample(x=-100, y=maxy+100.1), 
        ]


        # later on we need to get the value of each sample...
        all_samples = [ { 'xy': (s.x, s.y), 'value': s.__getattribute__(name) } for s in start_data + samples ]
        # but voronoi needs a list of tuples
        points = [ s['xy'] for s in all_samples ]

        vor = Voronoi(points)
        fig = voronoi_plot_2d(vor)

        # limits
        #plt.axis('equal')
        plt.xlim(0,maxx)
        plt.ylim(0,maxy)

        # colorize
        for region, num_reg in zip(vor.regions, range(len(vor.regions))):
            if not -1 in region:
                polygon = [vor.vertices[i] for i in region]
                if len(polygon):
                    pr = list(vor.point_region)
                    p = pr.index(num_reg)
                    color = 1 - map_color(all_samples[p]['value'], config['min'], config['max'])
                    plt.fill(*zip(*polygon), color=(color, color, color))
                        

        plt.savefig(get_group_graph_name(name, group.id))
        plt.close()

    db.session.commit()

def get_group_graph_name(name, group_id):
    return app.static_folder + "/graphs/" + name + "_group_%d.png" % group_id

def submit_graph(sample):
    maxx = app.config['MAX_X']
    maxy = app.config['MAX_Y']

    plt.scatter(sample.x, sample.y, marker = 'o', c=0.5, s = 200, alpha=0.5)
    plt.xlim(0,maxx)
    plt.ylim(0,maxy)

    app.logger.info("updated submit graph")
    plt.savefig(app.static_folder + "/graphs/after_submit_%d.png" % sample.id)
    plt.close()
