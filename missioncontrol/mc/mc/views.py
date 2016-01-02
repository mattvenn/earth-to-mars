from mc import app
import sqlite3
import datetime
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from initialise import initialise
import time

from wtforms import TextField, IntegerField, FloatField, SelectField
from wtforms import validators
from flask_wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from mc.database import db_session
from mc.models import Teams, School, Sample_Types, Sample

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

def add_school_point():
    school = School.query.order_by(School.timestamp.desc()).first()
    school.points += 1
    db_session.commit()

class SampleForm(Form):
    
    def get_sample_types():
        return Sample_Types.query.all()

    def get_teams():
        return Teams.query.all()

    type = QuerySelectField(query_factory=get_sample_types)
    team = QuerySelectField(query_factory=get_teams)
    value = FloatField('Sample Value')
    x = IntegerField('X', [validators.NumberRange(min=0, max=10)])
    y = IntegerField('Y', [validators.NumberRange(min=0, max=10)])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.sample = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        sample = Sample(self.type.data, self.team.data, self.x.data, self.y.data, self.value.data)

        if sample.value > sample.type.max:
            self.value.errors.append('has to be less than %f' % sample.type.max)
            return False
        if sample.value < sample.type.min:
            self.value.errors.append('has to be more than %f' % sample.type.min)
            return False

        self.sample = sample
        return True


@app.route('/')
def mission_control():
    school = School.query.order_by(School.timestamp.desc()).first()
    now = datetime.datetime.now()
    end_time = datetime.datetime.now().replace(hour=16,minute=0,second=0)
    delta = end_time - now
    mins = delta.total_seconds() / 60
    hours = mins / 60
    mins = mins % 60
    secs = delta.total_seconds() % 60
    time_info = { 'now': now.strftime('%d/%m/%Y %H:%M:%S'),  'left': '%02d:%02d:%02d' % (hours, mins, secs) }
    return render_template('mission_control.html', school_info=school, time_info=time_info)

@app.route('/show_samples')
def show_samples():
    samples = Sample.query.all()
    return render_template('show_samples.html', samples=samples)

@app.route('/upload/sample', methods=['GET', 'POST'])
def add_sample():
    form = SampleForm(request.form)

    if form.validate_on_submit():
        db_session.add(form.sample)
        db_session.commit()
        add_school_point()
        flash('sample logged')
        return redirect(url_for('add_sample'))
    return render_template('add_sample.html', form=form)

@app.route('/admin/add_school', methods=['POST'])
def add_school():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into schools (name) values (?)',
                 [request.form['name']])
    g.db.commit()
    flash('New school was successfully added')
    return redirect(url_for('admin'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    cur = g.db.execute('select name, points, timestamp from schools order by id ')
    schools = cur.fetchall()
    return render_template('admin.html', schools=schools)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('admin'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('admin'))

