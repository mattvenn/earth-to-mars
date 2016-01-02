from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from mc.database import Base
from datetime import datetime

class Teams(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    points = Column(Integer)

    def __init__(self, name=None, points=0):
        self.name = name
        self.points = points

    def __repr__(self):
        return self.name

class School(Base):
    __tablename__ = 'schools'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
    points = Column(Integer)

    def __init__(self, name=None, points=0):
        self.name = name
        self.points = points

    def __repr__(self):
        return self.name

class Sample_Types(Base):
    __tablename__ = 'sample_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    min = Column(Float())
    max = Column(Float())

    def __init__(self, name=None, min=0, max=0):
        self.name = name
        self.min = min
        self.max = max

    def __repr__(self):
        return self.name

class Sample(Base):
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

    def __init__(self, type, team, x, y, value):
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
