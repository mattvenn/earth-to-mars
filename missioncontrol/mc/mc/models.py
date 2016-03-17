from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from mc import db
from mc import app
from PIL import Image

class Questions(db.Model):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    question = Column(Text(), nullable=False)
    answer = Column(Text(), nullable=False)
    image_path = Column(String(50))

    def __init__(self, question=None, answer=None, image_path=None):
        self.question = question
        self.answer = answer
        self.image_path = image_path

    def __repr__(self):
        return self.question

    @staticmethod
    def get_csv_head():
        return "id", "question", "answer"

    def get_csv(self):
        return self.id, self.question, self.answer

class Answers(db.Model):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    answer = Column(Text(), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    team = relationship("Teams")
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    question = relationship("Questions")

    def __init__(self, question=None, answer=None, team=None):
        self.answer = answer
        self.team = team
        self.question = question

    @staticmethod
    def get_csv_head():
        return "id","question_id","team","answer"

    def get_csv(self):
        return self.id, self.question.id, self.team, self.answer.encode('utf8')

class Teams(db.Model):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return self.name

    def serialise(self):
        return {
            'id' : self.id,
            'name' : self.name,
            }

class School(db.Model):
    __tablename__ = 'schools'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    points = Column(Integer, nullable=False)

    def __init__(self, name=None, points=0):
        self.name = name
        self.points = points

    def __repr__(self):
        return self.name

class GroupGraph(db.Model):
    __tablename__ = 'groupgraph'
    id = Column(Integer, primary_key=True)

class Panorama(db.Model):
    __tablename__ = 'panorama'
    id = Column(Integer, primary_key=True)
    pan_id = Column(Integer, default=0)

    def __init__(self):
        if self.pan_id is None:
            self.pan_id = 0
            self.init()

    def get_pan_name(self):
        return "panorama%d.jpg" % self.pan_id

    def get_num_photos(self):
        return self.pan_id

    def init(self):
        w = app.config['PANORAMA_W']
        h = app.config['PANORAMA_H']
        background = Image.new('RGBA', (w, h), (255, 255, 255, 255))
        dir = app.static_folder + "/photos/"
        background.save(dir + self.get_pan_name())

    def add_to_panorama(self, photo):
        dir = app.static_folder + "/photos/"
        background = Image.open(dir + self.get_pan_name(), 'r')

        # resize image
        img = Image.open(dir + photo.image_path)
        img_w, img_h = img.size
        thumb_h = app.config['PANORAMA_H']
        thumb_w = img_w / (img_h / thumb_h)
        img.thumbnail((thumb_w, thumb_h) , Image.ANTIALIAS)

        # get panorama position
        offset = Panorama.calculate_offset(photo.x, photo.y)
        if offset is None:
            return False

        max_x = app.config['MAX_X']
        max_y = app.config['MAX_Y']
        total_pos = max_x * 2 + max_y * 2
        offset_px = offset * (app.config['PANORAMA_W'] / total_pos)
        print("(%2d, %2d) offset = %d/%d => %d/%d" % (photo.x, photo.y, offset, total_pos, offset_px, app.config['PANORAMA_W']))

        # open mask
        mask = Image.open(app.static_folder + "/alpha.jpg", 'r')
        mask = mask.resize(img.size)

        # paste the thumbnail in with the mask
        background.paste(img, (offset_px, 0), mask)

        # save panorama
        self.pan_id += 1
        db.session.commit()
        background.save(dir + self.get_pan_name())

    @staticmethod
    def calculate_offset(x, y):
        # calculate offset
        min_d = app.config['PANORAMA_MIN_D']
        max_x = app.config['MAX_X']
        max_y = app.config['MAX_Y']

        offset = 0
        # bottom
        if y < min_d:
            offset = x

        # right
        elif x > max_x - min_d:
            offset = max_x + y

        # top
        elif y > max_y - min_d:
            offset = max_x + max_y + max_x - x

        # left
        elif x < min_d:
            offset = max_x + max_y + max_x + max_y - y
        else:
            return None
        
        return offset

class Photo(db.Model):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    image_path = Column(String(50), nullable=False)
    x = Column(Integer(), nullable=False)
    y = Column(Integer(), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    team = relationship("Teams")


class Sample(db.Model):
    __tablename__ = 'samples'
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    team = relationship("Teams")

    methane = Column(Float(), nullable=False)
    temperature = Column(Float(), nullable=False)
    humidity = Column(Float(), nullable=False)

    x = Column(Integer(), nullable=False)
    y = Column(Integer(), nullable=False)

    timestamp = Column(DateTime, default=datetime.utcnow)
    conf = app.config['SAMPLE_TYPES']

    def __init__(self, team=None, x=None, y=None, methane=conf['methane']['min'], temperature=conf['temperature']['min'], humidity=conf['humidity']['min']):
        self.x = x
        self.y = y
        self.team = team
        self.methane = methane
        self.temperature = temperature
        self.humidity = humidity

    def __repr__(self):
        return '<Sample at %d,%d = %f %f %f>' % (self.x, self.y, self.methane, self.temperature, self.humidity)

    def serialise(self):
        return {
            'id' : self.id,
            'x' : self.x,
            'y' : self.y,
            'team' : self.team.name,
            'methane' : self.methane,
            'temperature' : self.temperature,
            'humidity' : self.humidity,
            }
