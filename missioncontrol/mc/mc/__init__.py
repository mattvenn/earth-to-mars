from flask import Flask, session, request
from flask.ext.sqlalchemy import SQLAlchemy
import os

from flask_admin import Admin, AdminIndexView

# configuration
config_obj = os.environ.get("DIAG_CONFIG_MODULE", "mc.config_real")

app = Flask(__name__)
app.config.from_object(config_obj)
db = SQLAlchemy(app)
db.init_app(app)

# have to wait till db is instatiated to use these
import mc.views
from mc.models import Teams, School, Sample_Types, Sample

admin = Admin(app, name='mission control')
admin.add_view(views.SecureView(School, db.session))
admin.add_view(views.SecureView(Sample, db.session))
admin.add_view(views.SecureView(Sample_Types, db.session))
admin.add_view(views.SecureView(Teams, db.session))
