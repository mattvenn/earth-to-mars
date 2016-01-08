import os
os.environ["DIAG_CONFIG_MODULE"] = "mc.config_real"

from mc import app
from mc.models import Sample
from mc import graphing

sample_types = app.config['SAMPLE_TYPES'].keys() 
for type in sample_types:
    print type
    graphing.update_group_graph(type)

