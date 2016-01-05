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
from mc.models import Teams, School, Sample_Types, Sample, Answers, Questions

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
    time_info = { 'now': now.strftime('%d/%m/%Y %H:%M:%S'),  'left': '%02d:%02d:%02d' % (hours, mins, secs) }
    return render_template('mission_control.html', school_info=school, time_info=time_info)

# tested
@app.route('/show_samples')
def show_samples():
    samples = Sample.query.all()
    return render_template('show_samples.html', samples=samples)

# tested
@app.route('/upload/sample', methods=['GET', 'POST'])
def add_sample():
    form = SampleForm(request.form)

    if form.validate_on_submit():
        db.session.add(form.sample)
        db.session.commit()
        add_school_point()
        flash('sample logged')
        return redirect(url_for('add_sample'))
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

    db.session.add(form.sample)
    db.session.commit()
        
    return jsonify(form.sample.serialise()), 201

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
