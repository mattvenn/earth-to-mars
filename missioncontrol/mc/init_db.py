#!/usr/bin/env python
import os
import csv
os.environ["DIAG_CONFIG_MODULE"] = "mc.config_real"
from mc import app
from mc import db
from mc.models import Teams, School, Sample, Questions, Answers, GroupGraph
from mc import graphing

def populate():
    with open('teams.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            team = Teams(row[0])
            db.session.add(team)

    with open('questions.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            question = Questions(row[0],row[1],row[2])
            db.session.add(question)

    school = School('test')
    db.session.add(school)

    # not validated, so be careful!
    sample = Sample(team, 10, 20, 0.1, 0.1, 0.1)
    db.session.add(sample)

    db.session.commit()

db.drop_all()
db.create_all()
populate()
