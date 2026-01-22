from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ============================================================
# ŠIFRANTI (lookup tabele)
# ============================================================

class CompetitionType(db.Model):
    __tablename__ = 'competition_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, default=True)

    styles = db.relationship('Style', backref='competition_type', lazy=True)

    def __repr__(self):
        return f"<CompetitionType {self.name}>"


class Style(db.Model):
    __tablename__ = 'style'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    competition_type_id = db.Column(db.Integer, db.ForeignKey('competition_type.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Style {self.name}>"


class Gender(db.Model):
    __tablename__ = 'gender'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Gender {self.name}>"


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    parent = db.relationship('Category', remote_side=[id], backref='children')

    def __repr__(self):
        return f"<Category {self.name}>"


class SubCategory(db.Model):
    __tablename__ = 'subcategory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref='subcategories')

    # povezava na RecordType, backref poimenovan 'subcat', da ni konflikta
    record_types = db.relationship('RecordType', backref='subcat', lazy=True)

    def __repr__(self):
        return f"<SubCategory {self.name}>"


# ============================================================
# RECORD TYPE – osrednja definicija pravil
# ============================================================

class RecordType(db.Model):
    __tablename__ = 'record_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    competition_type_id = db.Column(db.Integer, db.ForeignKey('competition_type.id'), nullable=False)
    style_id = db.Column(db.Integer, db.ForeignKey('style.id'), nullable=False)
    gender_id = db.Column(db.Integer, db.ForeignKey('gender.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=False)

    arrow_count = db.Column(db.Integer, nullable=True)
    face = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    competition_type = db.relationship('CompetitionType')
    style = db.relationship('Style')
    gender = db.relationship('Gender')
    category = db.relationship('Category')
    # subcategory relacija → že definiran preko backref 'subcat' v SubCategory

    __table_args__ = (
        db.UniqueConstraint(
            'competition_type_id',
            'style_id',
            'gender_id',
            'category_id',
            'subcategory_id',
            name='uq_recordtype_definition'
        ),
    )

    def __repr__(self):
        return (
            f"<RecordType {self.name}: "
            f"{self.competition_type.name}, "
            f"{self.style.name}, "
            f"{self.gender.name}, "
            f"{self.category.name}, "
            f"{self.subcat.name}>"
        )


# ============================================================
# RECORD – dejanski rezultat
# ============================================================

class Record(db.Model):
    __tablename__ = 'record'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    club = db.Column(db.String(100), nullable=False)

    result = db.Column(db.String(100), nullable=False)
    record_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    record_type_id = db.Column(db.Integer, db.ForeignKey('record_type.id'), nullable=False)
    record_type = db.relationship('RecordType', backref='records')

    def __repr__(self):
        return f"<Record {self.first_name} {self.last_name} ({self.result})>"
