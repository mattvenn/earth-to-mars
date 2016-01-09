SQLALCHEMY_DATABASE_URI = 'sqlite:///mc.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
MAX_X = 30
MAX_Y = 20
GRAPH_WIDTH = 800
GRAPH_HEIGHT = 400

SAMPLE_TYPES = {
    'methane': { 'min' : 0, 'max': 0.1, 'unit' : 'ppm' },
    'oxygen' : { 'min' : 0, 'max': 0.1, 'unit' : 'ppm' },
    'temperature' : { 'min' : 0, 'max': 200, 'unit' : 'K' },
    'humidity' : { 'min' : 0, 'max': 100, 'unit' : '%' },
    }
