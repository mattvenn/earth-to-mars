import unittest
from flask.ext.testing import TestCase
from flask import Flask
import os
import json
from mc.models import Teams, School, Sample_Types, Sample

# use test environment
os.environ["DIAG_CONFIG_MODULE"] = "mc.config_test"

from mc import app
from mc import db

class MCEmptyTest(TestCase):

    def create_app(self):
        return app

    def setUp(self):
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_samples(self):
        rv = self.client.get("/show_samples")
        assert 'No samples here so far' in rv.data

        rv = self.client.post('/api/sample', data=dict(
            {}), follow_redirects=True)
        assert json.loads(rv.data)['message'] == 'json needed'

"""
class MCPopulatedTest(TestCase):

    def create_app(self):
        return app

    def setUp(self):
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
            self.populate()

    def populate(self):
        team = Teams('earth')
        db.session.add(team)

        sample_type = Sample_Types('hydrogen',0,1)
        db.session.add(sample_type)

        school = School('test')
        db.session.add(school)

        sample = Sample(sample_type, team, 0, 0, 0)
        db.session.add(sample)

        db.session.commit()
        assert sample_type.id == 1
        assert team.id == 1

    def tearDown(self):
        db.session.remove()
        db.drop_all()
       
    def test_samples_api(self):
        rv = self.client.get("/show_samples")
        assert 'class=samples' in rv.data

        rv = self.client.post('/api/sample', 
            data=json.dumps({ 'team' : "1", 'type' : "1", 'x' : 1, 'y': 1, 'value' : 0 }), content_type='application/json')
        assert json.loads(rv.data)['id'] == 2
        assert json.loads(rv.data)['value'] == 0
"""

if __name__ == '__main__':
    unittest.main()
