import os
os.environ["DIAG_CONFIG_MODULE"] = "mc.config_real"
from mc import app
from mc import db
from mc.models import Teams, School, Sample_Types, Sample, Questions, Answers

def populate():
    team = Teams('earth')
    db.session.add(team)

    sample_type = Sample_Types('hydrogen',0,1)
    db.session.add(sample_type)

    school = School('test')
    db.session.add(school)

    sample = Sample(sample_type, team, 10, 20, 0.5)
    db.session.add(sample)

    question = Questions("what's up doc?", "carrots", "carrot.png")
    db.session.add(question)

    answer = Answers(question, "carrots?", team)
    db.session.add(answer)

    db.session.commit()
    assert sample_type.id == 1
    assert team.id == 1

db.drop_all()
db.create_all()
populate()
