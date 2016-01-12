import unittest
from flask.ext.testing import TestCase
from flask import Flask
import os
import json
from mc.models import Teams, School, Sample
from mc.graphing import map_color
from init_db import populate

# use test environment
os.environ["DIAG_CONFIG_MODULE"] = "mc.config_test"

from mc import app
from mc import db
from mc.views import get_group_id, add_school_point, get_teams


class GraphingTest(unittest.TestCase):
    
    def test_mapping(self):
        assert map_color(0,0,1) == 0
        assert map_color(1,0,1) == 1
        assert map_color(0.5,0,1) == 0.5

        assert map_color(0,1,0) == 1
        assert map_color(1,1,0) == 0

        assert map_color(0,0,10) == 0
        assert map_color(1,0,10) == 0.1
        assert map_color(10,0,10) == 1

        assert map_color(-10,-10,10) == 0
        assert map_color(0,-10,10) == 0.5
        assert map_color(10,-10,10) == 1


class MCEmptyTest(TestCase):

    def create_app(self):
        return app

    def setUp(self):
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_empty_group_id(self):
        assert get_group_id() == 0

    def test_empty_answers(self):
        rv = self.client.get("/answers/1")
        assert 'find an answer to that' in rv.data

    def test_empty_questions(self):
        rv = self.client.get("/questions/1")
        assert 'find that question' in rv.data

    def test_empty_teams(self):
        assert len(get_teams()) == 0

    def test_empty_samples(self):
        rv = self.client.get("/show/samples")
        assert 'No samples here so far' in rv.data

    def test_admin_no_auth(self):
        rv = self.client.get("/admin/sample", follow_redirects=True)
        assert '<h2>Login</h2>' in rv.data

    def test_login_logout(self):
        rv = self.login(app.config['USERNAME'], app.config['PASSWORD'])
        assert 'back to mission control' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('xxxx', 'default')
        assert 'Unknown username' in rv.data
        rv = self.login(app.config['USERNAME'], 'xxxx')
        assert 'bad password' in rv.data

    def test_admin_auth(self):
        rv = self.login(app.config['USERNAME'], app.config['PASSWORD'])
        assert 'back to mission control' in rv.data
        rv = self.client.get("/admin/sample", follow_redirects=True)
        assert 'sure you want to delete' in rv.data

    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_no_photos(self):
        rv = self.client.get("/show/photos")
        assert rv.data.count('blank.png') == 30 * 20

    def test_no_photo(self):
        rv = self.client.get("/show/photo/1")
        assert 'No photo of that id' in rv.data
        

class MCPopulatedTest(TestCase):

    def create_app(self):
        return app

    def setUp(self):
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            populate()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_school_points(self):
        assert self.get_school_points() == 0
        add_school_point()
        assert self.get_school_points() == 1

    def test_get_teams(self):
        assert len(get_teams()) == 1
        assert get_teams()[0].name == 'earth'
    
    def get_school_points(self):
        school = School.query.order_by(School.timestamp.desc()).first()
        return school.points

    def test_mission_control(self):
        rv = self.client.get("/")
        assert 'Points: 0' in rv.data
        assert 'School: test' in rv.data

    def test_samples(self):
        rv = self.client.get("/show/samples")
        for s in [10,20,0.1,0.2,0.3,0.4]:
            assert '<td>%s</td>' % s in rv.data

    def test_add_sample(self):
        sample = { 'x' : None, 'y' : None, 'team': None, 'type' : None, 'value' : None }
        rv = self.client.post('/upload/sample', data=sample, follow_redirects=True)
        assert 'Not a valid choice' in rv.data
        assert 'must be between 0 and 20' in rv.data

        sample['x'] = 5
        sample['y'] = 5
        sample['team'] = 1
        rv = self.client.post('/upload/sample', data=sample, follow_redirects=True)
        assert 'class=errors' in rv.data
        sample['methane'] = 10000
        rv = self.client.post('/upload/sample', data=sample, follow_redirects=True)
        assert 'must be between 0 and 1' in rv.data

        sample['methane'] = 0.7
        sample['oxygen'] = 0.7
        sample['temperature'] = 0.7
        sample['humidity'] = 0.7
        rv = self.client.post('/upload/sample', data=sample, follow_redirects=True)
        assert 'sample logged' in rv.data

        rv = self.client.get("/")
        assert 'Points: 1' in rv.data

        rv = self.client.get("/show/samples")
        assert '0.7' in rv.data

    def test_answer_question(self):
        points = self.get_school_points()
        answer = { 'answer' : None, 'team': None }
        rv = self.client.post('/questions/1', data=answer, follow_redirects=True)
        assert 'Not a valid choice' in rv.data
        assert 'This field is required' in rv.data

        answer['team'] = 1
        answer['answer'] = 'blah'

        rv = self.client.post('/questions/1', data=answer, follow_redirects=True)
        assert 'carrots' in rv.data
        assert 'carrot.png' in rv.data
        assert self.get_school_points() == points + 1


    def test_get_sample_api(self):
        rv = self.client.get('/api/sample/100')
        assert 'no sample of that id found' in rv.data
        rv = self.client.get('/api/sample/1')
        assert json.loads(rv.data)['x'] == 10
        assert json.loads(rv.data)['y'] == 20
        assert json.loads(rv.data)['methane'] == 0.1
        assert json.loads(rv.data)['oxygen'] == 0.2
        assert json.loads(rv.data)['temperature'] == 0.3
        assert json.loads(rv.data)['humidity'] == 0.4
       
    def test_add_samples_api(self):
        points = self.get_school_points()

        rv = self.client.post('/api/sample', data=dict(
            {}), follow_redirects=True)
        assert json.loads(rv.data)['message'] == 'json needed'

        rv = self.client.get("/show/samples")
        assert 'class="samples"' in rv.data

        # could test that min and max samples work

        rv = self.client.post('/api/sample', 
            data=json.dumps({ 'team' : "1", 'x' : 1, 'y': 1, 'methane' : 0, 'oxygen' : 0, 'temperature' : 0, 'humidity' : 0 }), content_type='application/json')
        assert json.loads(rv.data)['id'] == 2
        assert json.loads(rv.data)['oxygen'] == 0

        assert self.get_school_points() == points + 1

    def test_show_graph(self):
        for type in app.config['SAMPLE_TYPES'].keys():
            rv = self.client.get("/show/graph/" + type)
            assert type in rv.data
            assert '.png' in rv.data

    """
    def test_upload_2(self):
        filename = "static/badge.png"

#        with self.app.open_resource(filename) as fp:
#        fp = self.app.open_resource(filename)
        fp = open('mc/' + filename)
        rv = self.client.post(
            "/upload/photo",
            data={'photo': (fp, 'test.png')}
        )
        assert 'Not a valid choice' in rv.data
    """

    def test_upload_photo(self):
        filename = "mc/static/badge.png"
        payload = {}
        payload['x'] = 5
        payload['y'] = 5
        payload['team'] = 1
        payload['photo'] = ( open(filename), 'test.png')

        rv = self.client.post('/upload/photo', data = payload)

        assert 'static/photos/test.png' in rv.data
       
    #https://github.com/lepture/flask-wtf/blob/master/tests/test_uploads.py
    def test_upload_missing_photo(self):
        payload = {}
        payload['x'] = 6
        payload['y'] = 6
        payload['team'] = 1

        rv = self.client.post('/upload/photo', data = payload)

        assert 'you must choose a photo' in rv.data

    def test_upload_wrong_filename(self):
        filename = "mc/static/badge.png"
        payload = {}
        payload['x'] = 6
        payload['y'] = 6
        payload['team'] = 1
        payload['photo'] = ( open(filename), 'test.pnx')


        rv = self.client.post('/upload/photo', data = payload)

        assert 'only images allowed' in rv.data


if __name__ == '__main__':
    unittest.main()
