from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Tip tekmovanja (Tarčno, Dvorana, Poljsko, 3D Clout, Flight)
class CompetitionType(db.Model):
    __tablename__ = 'competition_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    styles = db.relationship('Style', backref='competition_type', lazy=True)

# Stil (Ukrivljeni lok, Sestavljeni lok, Goli lok, Dolgi lok, Tradicionalni lok)
class Style(db.Model):
    __tablename__ = 'style'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    competition_type_id = db.Column(db.Integer, db.ForeignKey('competition_type.id'), nullable=False)
    genders = db.relationship('Gender', backref='style', lazy=True)

# Spol (Moški, Ženski)
class Gender(db.Model):
    __tablename__ = 'gender'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    style_id = db.Column(db.Integer, db.ForeignKey('style.id'), nullable=False)
    categories = db.relationship('Category', backref='gender', lazy=True)

# Kategorija (Člani, Starejši od 50 let, itd.)

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    gender_id = db.Column(db.Integer, db.ForeignKey('gender.id'), nullable=False)
    subcategories = db.relationship('SubCategory', backref='category', lazy=True)

    # Dodamo parent_id za nadrejeno kategorijo
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    parent = db.relationship('Category', remote_side=[id], backref='children')


# Podkategorija (Posamezno, Klubska ekipa, Reprezentančna ekipa)
class SubCategory(db.Model):
    __tablename__ = 'subcategory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    record_types = db.relationship('RecordType', backref='subcategory', lazy=True)

# Tip rekorda (lice, število puščic, aktiven/na)
class RecordType(db.Model):
    __tablename__ = 'record_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=False)
    arrow_count = db.Column(db.Integer, nullable=True)  # število puščic
    face = db.Column(db.String(100), nullable=True)  # velikost lice
    is_active = db.Column(db.Boolean, default=True)  # ali je rekord aktiven

# Vnos rekorda (ime, priimek, rezultat...)
class Record(db.Model):
    __tablename__ = 'record'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    club = db.Column(db.String(100), nullable=False)
    result = db.Column(db.String(100), nullable=False)
    record_date = db.Column(db.DateTime, nullable=False)
    record_type_id = db.Column(db.Integer, db.ForeignKey('record_type.id'), nullable=False)

    record_type = db.relationship('RecordType', backref='records', lazy=True)

