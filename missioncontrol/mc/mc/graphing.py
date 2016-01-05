import matplotlib.pyplot as plt
import math
from mc import app
from mc.models import Sample_Types, Sample

def update_group_graph(sample):
    maxx = app.config['MAX_X']
    maxy = app.config['MAX_Y']

    plt.xlim(0,maxx)
    plt.ylim(0,maxy)

    samples = Sample.query.filter(Sample.type == sample.type).all()
    app.logger.info("updating group graph for %s, using %d samples" % (sample, len(samples)))

    for sample in samples:
        area = math.pi * (25 * sample.value / sample.type.max)**2
        plt.scatter(sample.x, sample.y, s=area, c=20, alpha=0.5)

    plt.savefig(app.static_folder + "/" + str(sample.type) + "group.png")
    plt.close()
        
def submit_graph(sample):
    maxx = app.config['MAX_X']
    maxy = app.config['MAX_Y']

    plt.scatter(sample.x, sample.y, marker = 'o', c=0.5, s = 200, alpha=0.5)
    plt.xlim(0,maxx)
    plt.ylim(0,maxy)

    if sample.x < maxx/2:
        xtext = maxx/4
    else:
        xtext = -maxx/4
    if sample.y < maxy/2:
        ytext = maxy/4
    else:
        ytext = -maxy/4

    text = "%s\n%f" % (sample.type, sample.value)
    plt.annotate(text, xy =(sample.x, sample.y), xytext = (xtext,ytext),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
    app.logger.info("updated submit graph")
    plt.savefig(app.static_folder + "/after_submit_%d.png" % sample.id)
    plt.close()
