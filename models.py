from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    discipline = db.Column(db.String(100), nullable=False)  # Disciplina (Tarčno, Dvorano...)
    style = db.Column(db.String(100), nullable=False)       # Slog (Ukrivljeni lok, Sestavljeni lok...)
    gender = db.Column(db.String(10), nullable=False)       # Spol (M/Ž)
    face = db.Column(db.String(50), nullable=False)         # Lice (40cm, 60cm...)
    type = db.Column(db.String(20), nullable=False)         # Tip (posamezno, ekipa)
    name = db.Column(db.String(50), nullable=False)         # Naziv (18m, 70m...)
    category_type = db.Column(db.String(50), nullable=False) # Tip kategorije (npr. 18m, 70m)

    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)  # Starševska kategorija (za podkategorije)
    parent = db.relationship('Category', remote_side=[id])  # Relacija za podkategorije

    def __repr__(self):
        return f'<Category {self.discipline} - {self.style}>'
