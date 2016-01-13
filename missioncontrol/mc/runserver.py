#!/usr/bin/env python
import os
os.environ["DIAG_CONFIG_MODULE"] = "mc.config_real"
from mc import app
app.run(debug=True)
