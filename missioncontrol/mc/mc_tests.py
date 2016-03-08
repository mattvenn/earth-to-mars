import unittest
from flask.ext.testing import TestCase
from flask import Flask
import os
import json
from mc.models import Teams, School, Sample
from mc.graphing import map_color
from init_db import populate_test

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
        assert 'Back to Mission Control' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('xxxx', 'default')
        assert 'Unknown username' in rv.data
        rv = self.login(app.config['USERNAME'], 'xxxx')
        assert 'bad password' in rv.data

    def test_admin_auth(self):
        rv = self.login(app.config['USERNAME'], app.config['PASSWORD'])
        assert 'Back to Mission Control' in rv.data
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
            populate_test()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_school_points(self):
        assert self.get_school_points() == 0
        add_school_point()
        assert self.get_school_points() == 1

    def test_get_teams(self):
        assert len(get_teams()) == 15
        assert get_teams()[0].name == 'Aurora'
    
    def get_school_points(self):
        school = School.query.order_by(School.timestamp.desc()).first()
        return school.points

    def test_mission_control(self):
        rv = self.client.get("/")
        assert '<h2>0</h2>' in rv.data
        assert '</span>test</h1>' in rv.data

    def test_samples(self):
        rv = self.client.get("/show/samples")
        for s in [10,20,0.1,0.1,0.1,0.1]:
            assert '<td>%s</td>' % s in rv.data

    def test_add_sample(self):
        sample = { 'x' : None, 'y' : None, 'team': None }
        rv = self.client.post('/upload/sample', data=sample, follow_redirects=True)
        assert 'must be between 0 and 10' in rv.data
        assert 'must be between 0 and 100' in rv.data

        sample['x'] = 5
        sample['y'] = 5
        sample['team'] = 1
        rv = self.client.post('/upload/sample', data=sample, follow_redirects=True)
        assert 'class=errors' in rv.data
        sample['methane'] = 10000
        rv = self.client.post('/upload/sample', data=sample, follow_redirects=True)
        assert 'must be between 0 and 1' in rv.data

        sample['methane'] = 0.1
        sample['temperature'] = 0.1
        sample['humidity'] = 0.1

        rv = self.client.post('/upload/sample', data=sample, follow_redirects=True)
        assert 'sample logged' in rv.data

        rv = self.client.get("/")
        assert '<h2>1</h2>' in rv.data

        rv = self.client.get("/show/samples")
        assert '0.1' in rv.data

    def test_reject_repeated_sample(self):
        sample = { 'x' : 5, 'y' : 6, 'team': 1, 'methane': 0.1, 'temperature': 0.1, 'humidity': 0.1 }
        # team 1 uploads sample
        rv = self.client.post('/upload/sample', data=sample, follow_redirects=True)
        assert 'sample logged' in rv.data

        # team 2 uploads same sample - ok
        sample['team'] = 2

        rv = self.client.post('/upload/sample', data=sample, follow_redirects=True)
        assert 'sample logged' in rv.data


        # team 1 tries to upload sample again - not ok
        sample['team'] = 1
        rv = self.client.post('/upload/sample', data=sample, follow_redirects=True)
        assert 'your team already uploaded this sample' in rv.data

    def test_answer_question(self):
        points = self.get_school_points()
        answer = { 'answer' : None, 'team': None }
        rv = self.client.post('/questions/1', data=answer, follow_redirects=True)
        assert 'This field is required' in rv.data

        answer['team'] = 1
        answer['answer'] = 'blah'

        rv = self.client.post('/questions/1', data=answer, follow_redirects=True)
        assert 'samples' in rv.data
#        assert 'carrots.png' in rv.data
        assert self.get_school_points() == points + 10


    def test_get_sample_api(self):
        rv = self.client.get('/api/sample/100')
        assert 'no sample of that id found' in rv.data
        rv = self.client.get('/api/sample/1')
        assert json.loads(rv.data)['x'] == 10
        assert json.loads(rv.data)['y'] == 20
        assert json.loads(rv.data)['methane'] == 0.1
        assert json.loads(rv.data)['temperature'] == 0.1
        assert json.loads(rv.data)['humidity'] == 0.1
       
    def test_add_samples_api(self):
        points = self.get_school_points()

        rv = self.client.post('/api/sample', data=dict(
            {}), follow_redirects=True)
        assert json.loads(rv.data)['message'] == 'json needed'

        rv = self.client.get("/show/samples")
        assert 'class="samples"' in rv.data

        # could test that min and max samples work

        rv = self.client.post('/api/sample', 
            data=json.dumps({ 'team' : "1", 'x' : 1, 'y': 1, 'methane' : 0, 'temperature' : 0, 'humidity' : 0 }), content_type='application/json')
        assert json.loads(rv.data)['id'] == 2

        assert self.get_school_points() == points + 1

    def test_reject_repeated_add_sample_api(self):
        rv = self.client.post('/api/sample', 
            data=json.dumps({ 'team' : "1", 'x' : 1, 'y': 1, 'methane' : 0, 'temperature' : 0, 'humidity' : 0 }), content_type='application/json')
        
        sample = json.loads(rv.data)
        assert sample['id'] == 2

        rv = self.client.post('/api/sample', 
            data=json.dumps({ 'team' : "1", 'x' : 1, 'y': 1, 'methane' : 0, 'temperature' : 0, 'humidity' : 0 }), content_type='application/json')

        sample = json.loads(rv.data)
        assert sample['message'] == 'invalid data'
        assert 'already uploaded' in sample['team'][0]

    def test_get_all_samples(self):
        rv = self.client.get("/api/samples")
        samples = json.loads(rv.data)['samples']
        assert len(samples) == 1
        assert samples[0]['temperature'] == 0.1
        assert samples[0]['humidity'] == 0.1

    def test_team_api(self):
        rv = self.client.get("/api/team/xx")
        assert 'no team of that name found' in rv.data

        rv = self.client.get("/api/team/aurora")
        assert json.loads(rv.data)['name'] == 'Aurora'
        assert json.loads(rv.data)['id'] == 1

        rv = self.client.get("/api/team/aUroRa")
        assert json.loads(rv.data)['name'] == 'Aurora'
        assert json.loads(rv.data)['id'] == 1
        
    def test_show_graph(self):
        for type in app.config['SAMPLE_TYPES'].keys():
            rv = self.client.get("/show/graph/" + type)
            assert type in rv.data
            assert '.png' in rv.data


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
