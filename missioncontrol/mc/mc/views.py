from mc import app
from mc import db
from sqlalchemy.exc import IntegrityError
import datetime
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify
from contextlib import closing
from flask_admin.contrib.sqla import ModelView
import time

from wtforms import TextField, IntegerField, FloatField, SelectField, PasswordField
from wtforms import validators
from flask_wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from mc.models import Teams, School, Sample, Answers, Questions, GroupGraph
from graphing import submit_graph, update_group_graph

class SecureView(ModelView):
    def is_accessible(self):
        if 'logged_in' in session.keys():
            return True

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

# tested
def add_school_point():
    school = School.query.order_by(School.timestamp.desc()).first()
    school.points += 1
    db.session.commit()

class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if self.username.data != app.config['USERNAME']:
            self.username.errors.append('Unknown username')
            return False

        if self.password.data != app.config['PASSWORD']:
            self.password.errors.append('bad password')
            return False

        return True

class AnswerForm(Form):
    def get_teams():
        return Teams.query.all()

    team = QuerySelectField(query_factory=get_teams)
    answer = TextField('Answer', [validators.Required()])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        self.answer = Answers(None, self.answer.data, self.team.data)
        return True

class SampleForm(Form):
    
    def get_teams():
        return Teams.query.all()

    team = QuerySelectField(query_factory=get_teams)
    types = app.config['SAMPLE_TYPES']

    methane = FloatField('Methane', [validators.NumberRange(min=types['methane']['min'], max=types['methane']['max'])])
    oxygen = FloatField('Oxygen', [validators.NumberRange(min=types['oxygen']['min'], max=types['oxygen']['max'])])
    temperature = FloatField('Temperature', [validators.NumberRange(min=types['temperature']['min'], max=types['temperature']['max'])])
    humidity = FloatField('Humidity', [validators.NumberRange(min=types['humidity']['min'], max=types['humidity']['max'])])

    maxx = app.config['MAX_X']
    maxy = app.config['MAX_Y']

    x = IntegerField('X', [validators.NumberRange(min=0, max=maxx)])
    y = IntegerField('Y', [validators.NumberRange(min=0, max=maxy)])


# tested
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
    group_id = GroupGraph.query.all()[-1].id
    time_info = { 'now': now.strftime('%d/%m/%Y %H:%M:%S'),  'left': '%02d:%02d:%02d' % (hours, mins, secs) }
    return render_template('mission_control.html', school_info=school, time_info=time_info, group_id=group_id)

# tested
@app.route('/show_samples')
def show_samples():
    samples = Sample.query.all()
    return render_template('show_samples.html', samples=samples)

@app.route('/show_group_graph/<type>')
def show_group_graph(type):
    group_id = GroupGraph.query.all()[-1].id
    return render_template('show_group_graph.html', type=type, group_id=group_id)

@app.route('/upload/sample', methods=['GET', 'POST'])
def add_sample():
    form = SampleForm(request.form)

    if form.validate_on_submit():
        sample = Sample()
        form.populate_obj(sample)
        db.session.add(sample)
        db.session.commit()
        add_school_point()
        submit_graph(sample) #  make a graph
        #update_group_graph(form.sample)
        flash('sample logged')
        return render_template('sample_submitted.html', sample=sample)
    return render_template('add_sample.html', form=form)

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

# tested
@app.route('/api/sample/<int:sample_id>', methods=['GET'])
def api_get_sample(sample_id):
    sample = Sample.query.get(sample_id)
    if not sample:
        raise InvalidUsage("no sample of that id found")
    return jsonify(sample.serialise())

# tested
@app.route('/api/sample', methods=['POST'])
def api_add_sample():
    if not request.json:
        raise InvalidUsage("json needed")

    form = SampleForm(data = request.get_json())
    form.csrf_enabled = False
    if not form.validate():
        raise InvalidUsage("invalid data", payload=form.errors)

    sample = Sample()
    form.populate_obj(sample)
    db.session.add(sample)
    db.session.commit()
    #update_group_graph(form.sample)
    add_school_point()
        
    return jsonify(sample.serialise()), 201

# tested
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['logged_in'] = True
        return redirect('/admin')
    return render_template('login.html', form=form)

# tested
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('mission_control'))

# tested
@app.route('/answers/<int:question_id>')
def answers(question_id):
    question = Questions.query.get(question_id)
    return render_template('answer.html', question=question)

# tested
@app.route('/questions/<int:question_id>', methods=['GET', 'POST'])
def questions(question_id):
    form = AnswerForm(request.form)
    question = Questions.query.get(question_id)

    if form.validate_on_submit():
        form.answer.question = question
        db.session.add(form.answer)
        db.session.commit()
        add_school_point()
        flash('answer logged')
        return redirect(url_for('answers', question_id=question_id))

    return render_template('question.html', question=question, form=form)
