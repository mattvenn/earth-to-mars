SQLALCHEMY_DATABASE_URI = 'sqlite:///mc.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'curi0sity'
PANORAMA = 'panorama.jpg'
PANORAMA_H = 80
PANORAMA_W = 1050
PANORAMA_MIN_D = 7
MAX_X = 30
MAX_Y = 20

# when the timer ends
END_HOUR = 15
END_MIN = 15

SAMPLE_TYPES = {
    'methane': { 'min' : 0, 'max': 10, 'unit' : 'ppb' },
    'temperature' : { 'min' : -80, 'max': 30, 'unit' : 'C' },
    'humidity' : { 'min' : 0, 'max': 100, 'unit' : '%' },
    }
