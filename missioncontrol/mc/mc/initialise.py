import csv

def initialise(db):
    #TODO fix repetition here
    # team names
    with open('teams.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            print ', '.join(row)
            db.execute('insert into teams (name) values (?)',
                 row)
            db.commit()

    # sample types
    with open('sample_types.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            print ', '.join(row)
            db.execute('insert into sample_types (name, min, max) values (?, ?, ?)',
                 row)
            db.commit()
    
    # questions
    with open('questions.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            print ', '.join(row)
            db.execute('insert into questions (mission_id, question_text, answer_text, photo_path) values (?, ?, ?, ?)',
                 row)
            db.commit()

