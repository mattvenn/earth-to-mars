import unittest
import time
from flask.ext.testing import TestCase
from flask import Flask
from mc.models import Teams, School, Sample, Photo, Panorama
import os
from init_db import populate_test, drop_graphs
from PIL import Image, ImageDraw, ImageFont

# use test environment
os.environ["DIAG_CONFIG_MODULE"] = "mc.config_test"

from mc import app
from mc import db
from mc.views import get_group_id, add_school_point, get_teams

class PanoramaTest(TestCase):

    def create_app(self):
        return app

    def setUp(self):
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            populate_test()
            drop_graphs()

    def test_build_panorama(self):
        h = 200
        w = 200
        payload = {}
        payload['team'] = 1

        font = ImageFont.truetype("/usr/local/lib/python2.7/dist-packages/werkzeug/debug/shared/ubuntu.ttf", 45)
        
        pan = Panorama()
#        for x, y in ((24,2),(27,2),(29,2),(29,4),(29,6),(28,8)):
        for y in range(0, app.config['MAX_Y'],2):
            for x in range(0, app.config['MAX_X'],2):
                offset = Panorama.calculate_offset(x, y)


                if offset is None:
                    continue

                img = Image.new('RGBA', (w, h), (255, 0, 0, 255))
                draw = ImageDraw.Draw(img)
                draw.text((100, 50), str(x), (0,0,0), font)
                draw.text((100, 100), str(y), (0,0,0), font)
                img.save('/tmp/test.png')
                payload['x'] = x
                payload['y'] = y
                payload['photo'] = ( open('/tmp/test.png'), 'test.png')

                rv = self.client.post('/upload/photo', data = payload)
                assert 'static/photos/test.png' in rv.data
    #            time.sleep(0.2)

class PanoramaPhotoTest(TestCase):

    def create_app(self):
        return app

    def setUp(self):
        db.init_app(self.app)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            populate_test()
            dropGraphs()

    def test_build_panorama(self):
        count = 0
        import json
        with open("test_panorama_files/mission.txt", 'r') as fh:
            for line in fh.readlines():
                data = json.loads(line)
                payload = { 'x': data['x'], 'y': data['y'], 'team' : 1 }
                payload['photo'] = ( open('test_panorama_files/%dphoto.jpg' % count), 'test.png')
                count += 1
                rv = self.client.post('/upload/photo', data = payload)

if __name__ == '__main__':
    unittest.main()
