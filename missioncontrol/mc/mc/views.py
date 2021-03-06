from mc import app
from mc import db
from sqlalchemy.exc import IntegrityError
import datetime
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify, make_response, send_file
from contextlib import closing
from flask_admin.contrib.sqla import ModelView
import time

from wtforms import TextAreaField, TextField, IntegerField, FloatField, SelectField, PasswordField

from wtforms import validators
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired

from wtforms.ext.sqlalchemy.fields import QuerySelectField
from mc.models import Teams, School, Sample, Answers, Questions, GroupGraph, Photo, Panorama
from graphing import submit_graph, update_group_graph, get_group_graph_name
from werkzeug import secure_filename
import os

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
def get_teams():
    return Teams.query.all()

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

    team = QuerySelectField(query_factory=get_teams, allow_blank=True, blank_text=u'Please choose')
    answer = TextAreaField('Answer', [validators.Required()])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if not self.team.data:
            self.team.errors.append('choose a team')
            return False

        self.answer = Answers(None, self.answer.data, self.team.data)
        return True


    
class PhotoForm(Form):
    
    team = QuerySelectField(query_factory=get_teams, allow_blank=True, blank_text=u'Please choose')

    maxx = app.config['MAX_X']
    maxy = app.config['MAX_Y']

    x = IntegerField('X', [validators.NumberRange(min=0, max=maxx - 1)])
    y = IntegerField('Y', [validators.NumberRange(min=0, max=maxy - 1)])

    photo = FileField('Image', validators=[
            FileRequired(message="you must choose a photo"),
            FileAllowed(['jpg', 'png'], message='only images allowed')
            ])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if not self.team.data:
            self.team.errors.append('choose a team')
            return False

        return True

class SampleForm(Form):
    
    team = QuerySelectField(query_factory=get_teams, allow_blank=True, blank_text=u'Please choose')
    types = app.config['SAMPLE_TYPES']

    methane = FloatField('Methane', [validators.NumberRange(min=types['methane']['min'], max=types['methane']['max'])])
    temperature = FloatField('Temperature', [validators.NumberRange(min=types['temperature']['min'], max=types['temperature']['max'])])
    humidity = FloatField('Humidity', [validators.NumberRange(min=types['humidity']['min'], max=types['humidity']['max'])])

    maxx = app.config['MAX_X']
    maxy = app.config['MAX_Y']

    x = IntegerField('X', [validators.NumberRange(min=0, max=maxx - 1)])
    y = IntegerField('Y', [validators.NumberRange(min=0, max=maxy - 1)])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if not self.team.data:
            self.team.errors.append('choose a team')
            return False

        if Sample.query.filter(Sample.x == self.x.data, Sample.y == self.y.data, Sample.team == self.team.data).first():

            self.team.errors.append('your team already uploaded this sample')
            return False
        return True

# tested
def add_school_point(points=1):
    school = School.query.order_by(School.timestamp.desc()).first()
    if school is not None:
        school.points += points 
        db.session.commit()

# tested
def get_group_id():
    try:
        group_id = GroupGraph.query.all()[-1].id
    except IndexError:
        group_id = 0
    return group_id

# tested
@app.route('/')
def mission_control():
    school = School.query.order_by(School.timestamp.desc()).first()
    now = datetime.datetime.now()
    end_hour = app.config['END_HOUR']
    end_min = app.config['END_MIN']
    end_time = datetime.datetime.now().replace(hour=end_hour,minute=end_min,second=0)
    delta = end_time - now
    mins = delta.total_seconds() / 60
    hours = mins / 60
    mins = mins % 60
    secs = delta.total_seconds() % 60
    time_info = { 'now': now.strftime('%H:%M'),  'left': '%02d:%02d' % (hours, mins) }

    pan = Panorama.query.first()
    pan_info = { 'name': pan.get_pan_name(), 'num': pan.get_num_photos() }
    return render_template('mission_control.html', school_info=school, time_info=time_info, pan_info=pan_info, group_id=get_group_id())

# tested
@app.route('/show/samples')
def show_samples():
    samples = Sample.query.all()
    return render_template('show_samples.html', samples=samples)

# tested
@app.route('/show/graph/<type>')
def show_group_graph(type):
    return render_template('show_group_graph.html', type=type, group_id=get_group_id())

# tested
@app.route('/upload/sample', methods=['GET', 'POST'])
def add_sample():
    form = SampleForm()

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

def make_csv(head, list):
    import StringIO
    import csv
    si = StringIO.StringIO()
    cw = csv.writer(si)
    cw.writerow(head)
    for i in list:
        cw.writerow(i.get_csv())
    return si

def make_csv_response(head, list, name):
    si = make_csv(head, list)
    response = make_response(si.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=%s" % name
    return response

@app.route('/api/questions')
def api_get_questions():
    questions = Questions.query.all()
    head = Questions.get_csv_head()
    return make_csv_response(head, questions,'questions.csv')


@app.route('/api/answers')
def api_get_answers():
    answers = Answers.query.all()
    head = Answers.get_csv_head()
    return make_csv_response(head, answers,'answers.csv')

# build an archive of all the cool data and zip it
@app.route('/api/zipped-data')
def zipped_data():
    import zipfile
    import io
    import json
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:

        for name in app.config['SAMPLE_TYPES'].keys():
            graph_name = get_group_graph_name(name, get_group_id())
            zf.write(graph_name, name + '.png')

        answers = Answers.query.all()
        head = Answers.get_csv_head()
        answers_csv = make_csv(head, answers)
        zf.writestr('answers.csv', answers_csv.getvalue())

        questions = Questions.query.all()
        head = Questions.get_csv_head()
        questions_csv = make_csv(head, questions)
        zf.writestr('questions.csv', questions_csv.getvalue())

        samples = Sample.query.all()
        data = { 'samples' : [sample.serialise() for sample in samples]}
        zf.writestr('samples.json', json.dumps(data))

    memory_file.seek(0)
    return send_file(memory_file, attachment_filename='missioncontrol.zip', as_attachment=True)

# tested
@app.route('/api/team/<name>')
def api_get_team_by_name(name):
    name = name.lower()
    teams = get_teams()
    for team in teams:
        if team.name.lower() == name:
            return jsonify(team.serialise())

    raise InvalidUsage("no team of that name found")

# tested
@app.route('/api/samples')
def api_get_all_samples():
    samples = Sample.query.all()
    data = { 'samples' : [sample.serialise() for sample in samples]}
    return jsonify(data)

# tested
@app.route('/api/sample/<int:sample_id>')
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
        flash('You were logged in')
        return redirect('/admin')
    return render_template('login.html', form=form)

# tested
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect('/admin')

# tested
@app.route('/answers/<int:question_id>')
def answers(question_id):
    question = Questions.query.get(question_id)
    return render_template('answer.html', question=question)

# tested
@app.route('/questions/<int:question_id>', methods=['GET', 'POST'])
def questions(question_id):
    form = AnswerForm()
    question = Questions.query.get(question_id)

    if form.validate_on_submit():
        form.answer.question = question
        db.session.add(form.answer)
        db.session.commit()
        add_school_point(10)
        flash('answer logged')
        return redirect(url_for('answers', question_id=question_id))

    return render_template('question.html', question=question, form=form)

@app.route('/upload/photo', methods=['GET', 'POST'])
def add_photo():
    form = PhotoForm()
    if form.validate_on_submit():
        filename = secure_filename(form.photo.data.filename)
        form.photo.data.save(os.path.join(app.static_folder, 'photos', filename))

        photo = Photo()
        form.populate_obj(photo)
        photo.image_path = filename
        db.session.add(photo)
        db.session.commit()
        pan = Panorama.query.first()
        pan.add_to_panorama(photo)
        add_school_point()

        return render_template('photo_submitted.html', photo=photo)

    return render_template('add_photo.html', form=form)


