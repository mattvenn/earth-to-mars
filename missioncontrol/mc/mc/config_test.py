SQLALCHEMY_DATABASE_URI = 'sqlite:///mc_test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
WTF_CSRF_ENABLED = False
DEBUG = False
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
MAX_X = 30
MAX_Y = 20


SAMPLE_TYPES = {
    'methane': { 'min' : 0, 'max': 10, 'unit' : 'ppb' },
    'temperature' : { 'min' : -80, 'max': 30, 'unit' : 'C' },
    'humidity' : { 'min' : 0, 'max': 100, 'unit' : '%' },
    }
