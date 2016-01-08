import os
os.environ["DIAG_CONFIG_MODULE"] = "mc.config_real"

from mc import app
from mc.models import Sample, Sample_Types
from mc import graphing

print Sample_Types.query.all()

for sample_type in Sample_Types.query.all():
    print sample_type
    graphing.update_group_graph(sample_type)

