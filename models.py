from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import aliased
from sqlalchemy import func, cast, Float

db = SQLAlchemy()

# ============================================================
# ŠIFRANTI (lookup tabele)
# ============================================================


class CompetitionType(db.Model):
    __tablename__ = 'competition_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<CompetitionType {self.name}>"

class CompetitionSubType(db.Model):
    __tablename__ = 'competition_subtype'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    # FK na CompetitionType
    competition_type_id = db.Column(db.Integer, db.ForeignKey('competition_type.id'), nullable=False)
    competition_type = db.relationship('CompetitionType', backref='subtypes')

    # Število puščic za ta "vrsto tekmovanja"
    arrows = db.Column(db.Integer, nullable=False, default=0)

    # Novo polje: lice (lahko null)
    lice = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f"<CompetitionSubType {self.name} ({self.competition_type.name}) - {self.arrows} arrows, lice={self.lice}>"



class Style(db.Model):
    __tablename__ = 'style'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<Style {self.name}>"


class Gender(db.Model):
    __tablename__ = 'gender'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"<Gender {self.name}>"


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    parent = db.relationship('Category', remote_side=[id], backref='children')

    gender_id = db.Column(db.Integer, db.ForeignKey('gender.id'), nullable=False)
    gender = db.relationship('Gender', backref='categories')

    def __repr__(self):
        return f"<Category {self.name} ({self.gender.name})>"


class SubCategory(db.Model):
    __tablename__ = 'subcategory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<SubCategory {self.name}>"


class Record(db.Model):
    __tablename__ = 'record'

    id = db.Column(db.Integer, primary_key=True)

    # ====== osnovni podatki ======
    competitor_name = db.Column(db.String(150), nullable=False)
    club = db.Column(db.String(150), nullable=True)
    result = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(150), nullable=True)
    date = db.Column(db.Date, nullable=False)

    # ====== povezave ======
    competition_type_id = db.Column(
        db.Integer,
        db.ForeignKey('competition_type.id'),
        nullable=False
    )
    competition_type = db.relationship('CompetitionType')

    competition_subtype_id = db.Column(
        db.Integer,
        db.ForeignKey('competition_subtype.id'),
        nullable=True
    )
    competition_subtype = db.relationship('CompetitionSubType')

    style_id = db.Column(
        db.Integer,
        db.ForeignKey('style.id'),
        nullable=False
    )
    style = db.relationship('Style')

    gender_id = db.Column(
        db.Integer,
        db.ForeignKey('gender.id'),
        nullable=False
    )
    gender = db.relationship('Gender')

    category_id = db.Column(
        db.Integer,
        db.ForeignKey('category.id'),
        nullable=False
    )
    category = db.relationship('Category')

    subcategory_id = db.Column(
        db.Integer,
        db.ForeignKey('subcategory.id'),
        nullable=True
    )
    subcategory = db.relationship('SubCategory')

    @classmethod
    def best_results(cls, competition_type_name=None):
        r2 = aliased(cls)

        q = db.session.query(
            cls.competition_type_id,
            cls.competition_subtype_id,
            cls.style_id,
            cls.gender_id,
            cls.category_id,
            cls.subcategory_id,
            func.max(cast(cls.result, Float)).label("max_result")
        )

        if competition_type_name:
            q = q.join(cls.competition_type) \
                .filter(CompetitionType.name == competition_type_name)

        subq = q.group_by(
            cls.competition_type_id,
            cls.competition_subtype_id,
            cls.style_id,
            cls.gender_id,
            cls.category_id,
            cls.subcategory_id,
        ).subquery()

        return (
            db.session.query(cls)
                .join(
                subq,
                (cls.competition_type_id == subq.c.competition_type_id) &
                (func.coalesce(cls.competition_subtype_id, 0)
                 == func.coalesce(subq.c.competition_subtype_id, 0)) &
                (cls.style_id == subq.c.style_id) &
                (cls.gender_id == subq.c.gender_id) &
                (cls.category_id == subq.c.category_id) &
                (func.coalesce(cls.subcategory_id, 0)
                 == func.coalesce(subq.c.subcategory_id, 0)) &
                (cast(cls.result, Float) == subq.c.max_result)
            )
                .all()
        )

    def __repr__(self):
        return (
            f"<Record {self.competitor_name} | {self.result} | "
            f"{self.date}>"
        )

