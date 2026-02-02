import pandas as pd
from app import app
from configuration.categories import get_gender_name
from models import db, CompetitionType, CompetitionSubType, Style, Gender, Category, SubCategory, Record

file_path = "Rekordi.xls"
df = pd.read_excel(file_path, header=None)


def create_record_from_row(row):
    with app.app_context():
        # 0: CompetitionType
        comp_type = CompetitionType.query.filter_by(name=row[0]).first()
        if not comp_type:
            return  # ignoriraj vrstico, če tip ne obstaja

        # 4: CompetitionSubType
        comp_subtype = CompetitionSubType.query.filter_by(name=row[4], competition_type_id=comp_type.id).first()

        # 1: Style
        style = Style.query.filter_by(name=row[1]).first()
        if not style:
            return  # ignoriraj vrstico, če style ne obstaja

        # 2: Gender + Category
        gender_name = get_gender_name(row)
        gender = Gender.query.filter_by(name=gender_name).first()
        category = Category.query.filter_by(name=row[2], gender_id=gender.id).first()
        if not category:
            return  # ignoriraj vrstico, če category ne obstaja

        # 3: SubCategory
        subcategory = SubCategory.query.filter_by(name=row[3]).first()

        # 7: competitor_name
        competitor_name = row[7]

        # Popravljena vrstica: Club in Location
        club = row[8] if not pd.isna(row[8]) else None
        location = row[9] if not pd.isna(row[9]) else None

        # 6: result
        raw_result = row[6]

        if pd.isna(raw_result):
            return  # ali result = None, če želiš dovoliti prazno
        elif isinstance(raw_result, (int, float)):
            if float(raw_result).is_integer():
                result = str(int(raw_result))  # 1307.0 → "1307"
            else:
                result = str(raw_result)  # 455.5 → "455.5"
        else:
            result = str(raw_result)

        # 10: date
        date = row[10]
        if not pd.isna(date):
            date = pd.to_datetime(date).date()

        # Preveri, če Record že obstaja
        existing = Record.query.filter_by(
            competitor_name=competitor_name,
            club=club,
            date=date,
            competition_type_id=comp_type.id,
            competition_subtype_id=comp_subtype.id if comp_subtype else None,
            style_id=style.id,
            gender_id=gender.id,
            category_id=category.id,
            subcategory_id=subcategory.id if subcategory else None,
            result=result
        ).first()

        if existing:
            print("že obstaja!!! ")
            return existing  # že obstaja, nič ne naredi

        # Ustvari Record
        record = Record(
            competitor_name=competitor_name,
            club=club,
            result=result,
            location=location,
            date=date,
            competition_type_id=comp_type.id,
            competition_subtype_id=comp_subtype.id if comp_subtype else None,
            style_id=style.id,
            gender_id=gender.id,
            category_id=category.id,
            subcategory_id=subcategory.id if subcategory else None
        )

        db.session.add(record)
        db.session.commit()
        return record


# Uvozi prvih 100 vrstic
# for i, row in df.head(500).iterrows():
count = 1
for i, row in df.iterrows():
    # Izpiši indeks in vrednosti posamezne vrstice (če želiš)
    #for idx, value in enumerate(row):
    #    print(f"{idx}: {value}")

    # Ustvari Record iz te vrstice
    create_record_from_row(row)
    print(count)
    count = count + 1



