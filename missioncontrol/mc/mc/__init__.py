from flask import Flask, session, request
from flask.ext.sqlalchemy import SQLAlchemy
import os

from flask_admin import Admin, AdminIndexView

# configuration
config_obj = os.environ.get("DIAG_CONFIG_MODULE", "mc.config_test")

app = Flask(__name__)
app.config.from_object(config_obj)
print app.config.get('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
db.init_app(app)

# have to wait till db is instatiated to use these
import mc.views
from mc.models import Teams, School, Sample, Questions, Answers

import paho.mqtt.client as mqtt
client = mqtt.Client()
client.connect("127.0.0.1",1883,60)
client.loop_start()

from mc.admin import Reset

admin = Admin(app, name='mission control')
admin.add_view(Reset(name='Reset', url='reset'))
admin.add_view(views.SecureView(School, db.session))
admin.add_view(views.SecureView(Sample, db.session))
admin.add_view(views.SecureView(Teams, db.session))
admin.add_view(views.SecureView(Questions, db.session))
admin.add_view(views.SecureView(Answers, db.session))
