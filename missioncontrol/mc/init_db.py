import os
os.environ["DIAG_CONFIG_MODULE"] = "mc.config_real"
from mc import app
from mc import db
from mc.models import Teams, School, Sample, Questions, Answers

def populate():
    team = Teams('earth')
    db.session.add(team)

    school = School('test')
    db.session.add(school)

    sample = Sample(team, 10, 20, 0.1, 0.2, 0.3, 0.4)
    db.session.add(sample)

    question = Questions("what's up doc?", "carrots", "carrot.png")
    db.session.add(question)

    answer = Answers(question, "carrots?", team)
    db.session.add(answer)

    db.session.commit()
    assert team.id == 1

db.drop_all()
db.create_all()
populate()
