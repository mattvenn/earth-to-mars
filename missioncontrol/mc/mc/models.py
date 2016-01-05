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

class Sample_Types(db.Model):
    __tablename__ = 'sample_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    min = Column(Float(), nullable=False)
    max = Column(Float(), nullable=False)

    def __init__(self, name=None, min=0, max=0):
        self.name = name
        self.min = min
        self.max = max

    def __repr__(self):
        return self.name

class Sample(db.Model):
    __tablename__ = 'samples'
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    team = relationship("Teams")

    type_id = Column(Integer, ForeignKey('sample_types.id'), nullable=False)
    type = relationship("Sample_Types")

    x = Column(Integer(), nullable=False)
    y = Column(Integer(), nullable=False)
    value = Column(Float(), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __init__(self, type=None, team=None, x=None, y=None, value=None):
        self.value = value
        self.x = x
        self.y = y
        self.team = team
        self.type = type

    def __repr__(self):
        return '<%s Sample at %d,%d = %f>' % (self.type, self.x, self.y, self.value)

    def serialise(self):
        return {
            'id' : self.id,
            'x' : self.x,
            'y' : self.y,
            'type' : self.type.name,
            'team' : self.team.name,
            'value' : self.value,
            }
