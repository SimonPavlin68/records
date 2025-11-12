from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))                  # tip tekme
    style = db.Column(db.String(50))                 # lok / stil
    category = db.Column(db.String(50))              # kategorija
    individual_or_team = db.Column(db.String(20))    # posamezno / ekipno
    details = db.Column(db.String(100))              # opis / krog
    arrows = db.Column(db.Integer)                   # število puščic
    score = db.Column(db.Integer)                    # rezultat
    archer = db.Column(db.String(100))               # ime priimek
    club = db.Column(db.String(100))                 # klub
    location = db.Column(db.String(100))             # kraj
    date = db.Column(db.Date)                        # datum
    record_type = db.Column(db.String(50))           # npr. "najboljši rezultat"

