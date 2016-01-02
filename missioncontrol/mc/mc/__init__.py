# all the imports
import sqlite3
import datetime
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from initialise import initialise
import time
from flask_wtf import Form
from wtforms import TextField, IntegerField, FloatField, SelectField
from wtforms import validators
from mc.database import db_session


# configuration
DATABASE = './mc.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from mc.models import Teams, School, Sample_Types, Sample

admin = Admin(app, name='mc', template_mode='bootstrap3')
admin.add_view(ModelView(School, db_session))
admin.add_view(ModelView(Sample, db_session))
admin.add_view(ModelView(Sample_Types, db_session))
admin.add_view(ModelView(Teams, db_session))

import mc.views

if __name__ == '__main__':
    app.run()
