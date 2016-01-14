#!/usr/bin/env python
import os
os.environ["DIAG_CONFIG_MODULE"] = "mc.config_real"
from mc import app
app.run('0.0.0.0', 80, debug=True)
