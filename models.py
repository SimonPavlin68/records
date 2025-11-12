from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.String(50))
    bow_type = db.Column(db.String(50))
    participants = db.Column(db.String(50))
    individual_or_team = db.Column(db.String(50))
    round_type = db.Column(db.String(50))
    score = db.Column(db.Integer)
    archer = db.Column(db.String(100))
    club = db.Column(db.String(100))
    location = db.Column(db.String(100))
    date = db.Column(db.Date)
    record_type = db.Column(db.String(50))

    def __repr__(self):
        return f"<Record {self.archer} {self.score}>"
