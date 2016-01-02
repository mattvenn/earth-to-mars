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
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from mc.models import Teams, School, Sample_Types, Sample

class SecureView(ModelView):
    def is_accessible(self):
        if 'logged_in' in session.keys():
            return True

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

admin = Admin(app, name='mission control')
admin.add_view(SecureView(School, db_session))
admin.add_view(SecureView(Sample, db_session))
admin.add_view(SecureView(Sample_Types, db_session))
admin.add_view(SecureView(Teams, db_session))

import mc.views

if __name__ == '__main__':
    app.run()
