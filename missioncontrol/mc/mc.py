# all the imports
import sqlite3
import datetime
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from initialise import initialise
import time

# configuration
DATABASE = './mc.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        initialise(db)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def add_point():
    cur = g.db.execute('select id, name, points from schools order by id desc')
    school_info = cur.fetchone()
    g.db.execute('update schools set points = ? where id = ?', [school_info['points'] + 1, school_info['id']])
    g.db.commit()

@app.route('/')
def mission_control():
    cur = g.db.execute('select id, name, points from schools order by id desc')
    school_info = cur.fetchone()
    now = datetime.datetime.now()
    end_time = datetime.datetime.now().replace(hour=16,minute=0,second=0)
    delta = end_time - now
    mins = delta.total_seconds() / 60
    hours = mins / 60
    mins = mins % 60
    secs = delta.total_seconds() % 60
    time_info = { 'now': now.strftime('%d/%m/%Y %H:%M:%S'),  'left': '%02d:%02d:%02d' % (hours, mins, secs) }
    return render_template('mission_control.html', school_info=school_info, time_info=time_info)

@app.route('/upload/sample', methods=['GET', 'POST'])
def upload_sample():
    error = None
    cur = g.db.execute('select id, name from sample_types order by id')
    sample_types = cur.fetchall()
    cur = g.db.execute('select id, name from teams order by id')
    teams = cur.fetchall()

    if request.method == 'POST':
        sample_id = int(request.form['sample_id'])
        cur = g.db.execute('select min, max from sample_types where id = ?', [sample_id])
        #TODO validate sample_id & team_id
        sample_type = cur.fetchone()
        team_id = request.form['team_id']

        try:
            value = float(request.form['value'])
        except ValueError:
            value = None

        if value is None:
            error = "sample must be a number"
        elif value > sample_type['max'] :
            error = "sample too big - largest can be %f" % sample_type['max']
        elif value < sample_type['min'] :
            error = "sample too big - smallest can be %f" % sample_type['min']
        # insert into db
        else:
            g.db.execute('insert into samples (team_id, type_id, x, y, value) values (?, ?, ?, ?, ?)',
                         [request.form['team_id'], request.form['sample_id'], request.form['x'], request.form['y'], request.form['value']])
            g.db.commit()
            add_point()
            flash('sample logged')
            return redirect(url_for('upload_sample'))

    return render_template('upload_sample.html', error=error, sample_types=sample_types, teams=teams)

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

if __name__ == '__main__':
    app.run()
