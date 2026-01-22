from app import app, db
from models import CompetitionType, Style, Gender, Category, SubCategory, RecordType


def create_tables():
    with app.app_context():
        # Izbrišemo obstoječe tabele in ustvarimo nove
        db.drop_all()
        db.create_all()

        # Dodajamo fiksne tipe tekmovanj (če še ne obstajajo)
        competition_types = ['Tarčno', 'Dvorana', 'Poljsko', '3D Clout', 'Flight']
        for comp_name in competition_types:
            if not CompetitionType.query.filter_by(name=comp_name).first():
                competition_type = CompetitionType(name=comp_name)
                db.session.add(competition_type)

        db.session.commit()

        # Dodajanje stilov za vsak tip tekmovanja
        for competition_type in CompetitionType.query.all():
            styles = ['Ukrivljeni lok', 'Sestavljeni lok', 'Goli lok', 'Dolgi lok', 'Tradicionalni lok']
            for style_name in styles:
                if not Style.query.filter_by(name=style_name, competition_type_id=competition_type.id).first():
                    style = Style(name=style_name, competition_type_id=competition_type.id)
                    db.session.add(style)

        db.session.commit()

        # Dodajanje spolov za vsak stil
        for style in Style.query.all():
            genders = ['Moški', 'Ženske']
            for gender_name in genders:
                if not Gender.query.filter_by(name=gender_name, style_id=style.id).first():
                    gender = Gender(name=gender_name, style_id=style.id)
                    db.session.add(gender)

        db.session.commit()

        # Dodajanje kategorij za vsak spol
        for gender in Gender.query.all():
            if gender.name == 'Moški':
                categories = [
                    'Člani', 'Mlajši od 21 let', 'Mlajši od 18 let', 'Mlajši od 15 let',
                    'Mlajši od 13 let', 'Starejši od 50 let'
                ]
            else:  # Za ženske
                categories = [
                    'Članice', 'Mlajše od 21 let', 'Mlajše od 18 let', 'Mlajše od 15 let',
                    'Mlajše od 13 let', 'Starejše od 50 let'
                ]

            for category_name in categories:
                if not Category.query.filter_by(name=category_name, gender_id=gender.id).first():
                    category = Category(name=category_name, gender_id=gender.id)
                    db.session.add(category)

        db.session.commit()

        # Dodajanje podkategorij za "Posamezno", "Klubska ekipa" in "Reprezentančna ekipa"
        for category in Category.query.all():
            subcategories = ['Posamezno', 'Klubska ekipa', 'Reprezentančna ekipa']
            for subcategory_name in subcategories:
                if not SubCategory.query.filter_by(name=subcategory_name, category_id=category.id).first():
                    subcategory = SubCategory(name=subcategory_name, category_id=category.id)
                    db.session.add(subcategory)

        db.session.commit()


        print("Baza in podatki so bili uspešno ustvarjeni.")


if __name__ == "__main__":
    create_tables()
