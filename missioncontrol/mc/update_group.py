import os
os.environ["DIAG_CONFIG_MODULE"] = "mc.config_real"
from mc import graphing

graphing.update_group_graph()

