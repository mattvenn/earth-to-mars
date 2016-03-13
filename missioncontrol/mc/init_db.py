#!/usr/bin/env python
import os
import csv
os.environ["DIAG_CONFIG_MODULE"] = "mc.config_real"
from mc import app
from mc import db
from mc.models import Teams, School, Sample, Questions, Answers, GroupGraph, Photo, Panorama
from mc import graphing

# populates a new database with initial records
def populate():
    with open('teams.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            team = Teams(row[0])
            db.session.add(team)

    with open('questions.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        for row in reader:
            question = Questions(row[0],row[1],row[2])
            db.session.add(question)

    school = School('Schoolname')
    db.session.add(school)
    db.session.commit()


def populate_test():
    populate()
    school = School('test')
    db.session.add(school)
    team = Teams.query.first()

    # not validated, so be careful!
    sample = Sample(team, 10, 20, 0.1, 0.1, 0.1)
    db.session.add(sample)
    db.session.commit()

def drop_graphs():
    import glob, os
    graphs = glob.glob(app.static_folder + "/graphs/*.png")
    for f in graphs:
        os.remove(f)
    photos = glob.glob(app.static_folder + "/photos/*")
    for f in photos:
        os.remove(f)

# drops and replaces all tables
def init():
    db.drop_all()
    db.create_all()

# resets the database between workshops
def reset():
    # delete all records
    Answers.query.delete()
    GroupGraph.query.delete()
    Panorama.query.delete()
    Photo.query.delete()
    Sample.query.delete()

    # delete graphs
    drop_graphs()

    # init graphs
    graphing.update_group_graph()

    p = Panorama()
    db.session.add(p)
    db.session.commit()


if __name__ == '__main__':
    init()
    reset()
    populate()
