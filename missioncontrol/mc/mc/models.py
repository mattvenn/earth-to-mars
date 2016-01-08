from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from mc import db

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
        return "%d: %s" % (self.id, self.question)

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

    def __repr__(self):
        return self.answer

class Teams(db.Model):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    points = Column(Integer)

    def __init__(self, name=None, points=0):
        self.name = name
        self.points = points

    def __repr__(self):
        return self.name

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


class Sample(db.Model):
    __tablename__ = 'samples'
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    team = relationship("Teams")

    methane = Column(Float(), nullable=False)
    oxygen = Column(Float(), nullable=False)
    temperature = Column(Float(), nullable=False)
    humidity = Column(Float(), nullable=False)

    x = Column(Integer(), nullable=False)
    y = Column(Integer(), nullable=False)

    timestamp = Column(DateTime, default=datetime.utcnow)

    def __init__(self, team=None, x=None, y=None, methane=0, oxygen=0, temperature=0, humidity=0):
        self.x = x
        self.y = y
        self.team = team
        self.methane = methane
        self.oxygen = oxygen
        self.temperature = temperature
        self.humidity = humidity

    def __repr__(self):
        return '<Sample at %d,%d = %f %f %f %f>' % (self.x, self.y, self.methane, self.oxygen, self.temperature, self.humidity)

    def serialise(self):
        return {
            'id' : self.id,
            'x' : self.x,
            'y' : self.y,
            'oxygen' : self.oxygen,
            'team' : self.team.name,
            'methane' : self.methane,
            'temperature' : self.temperature,
            'humidity' : self.humidity,
            }
