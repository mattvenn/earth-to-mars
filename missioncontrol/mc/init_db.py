#!/usr/bin/env python
import os
os.environ["DIAG_CONFIG_MODULE"] = "mc.config_real"
from mc import app
from mc import db
from mc.models import Teams, School, Sample, Questions, Answers, GroupGraph
from mc import graphing

def populate():
    team = Teams('Earth')
    db.session.add(team)

    school = School('test')
    db.session.add(school)

    # not validated, so be careful!
    sample = Sample(team, 10, 20, 0.1, 0.1, 0.1, 0.1)
    db.session.add(sample)

    question = Questions("what's up doc?", "carrots", "carrots.png")
    db.session.add(question)

    answer = Answers(question, "carrots?", team)
    db.session.add(answer)

    db.session.commit()
    assert team.id == 1

db.drop_all()
db.create_all()
populate()
