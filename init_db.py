from app import app
from models import db, CompetitionType, CompetitionSubType, Style, Gender, Category, SubCategory

def get_or_create(model, **kwargs):
    """Vrne obstoječi objekt ali ga ustvari, brez commit-a"""
    obj = model.query.filter_by(**kwargs).first()
    if obj:
        return obj
    obj = model(**kwargs)
    db.session.add(obj)
    return obj

def create_tables():
    with app.app_context():
        print("➡️ Creating tables...")
        db.create_all()

        # -----------------------------
        # Competition types
        # -----------------------------
        ct_tarcno = get_or_create(CompetitionType, name="Tarčno")
        ct_poljsko = get_or_create(CompetitionType, name="Poljsko")
        ct_dvorana = get_or_create(CompetitionType, name="Dvorana")
        ct_3d = get_or_create(CompetitionType, name="3D")
        ct_clout = get_or_create(CompetitionType, name="Clout")
        ct_flight = get_or_create(CompetitionType, name="Flight")

        db.session.commit()  # da dobijo vsi ID-je

        # -----------------------------
        # Competition SubTypes
        # -----------------------------

        get_or_create(CompetitionSubType, name="30m", competition_type_id=ct_tarcno.id, arrows=36)
        get_or_create(CompetitionSubType, name="40m", competition_type_id=ct_tarcno.id, arrows=36)
        get_or_create(CompetitionSubType, name="50m", competition_type_id=ct_tarcno.id, arrows=36)
        get_or_create(CompetitionSubType, name="60m", competition_type_id=ct_tarcno.id, arrows=36)
        get_or_create(CompetitionSubType, name="70m", competition_type_id=ct_tarcno.id, arrows=36)
        get_or_create(CompetitionSubType, name="90m", competition_type_id=ct_tarcno.id, arrows=36)
        get_or_create(CompetitionSubType, name="60m krog", competition_type_id=ct_tarcno.id, arrows=72)
        get_or_create(CompetitionSubType, name="70m krog", competition_type_id=ct_tarcno.id, arrows=72)
        get_or_create(CompetitionSubType, name="70m dvojni krog", competition_type_id=ct_tarcno.id, arrows=144)

        get_or_create(CompetitionSubType, name="18m", competition_type_id=ct_dvorana.id, arrows=60)
        get_or_create(CompetitionSubType, name="25m", competition_type_id=ct_dvorana.id, arrows=60)
        get_or_create(CompetitionSubType, name="25m + 18m", competition_type_id=ct_dvorana.id, arrows=120)
        get_or_create(CompetitionSubType, name="900 krogov", competition_type_id=ct_tarcno.id, arrows=90)
        get_or_create(CompetitionSubType, name="900 krogov (LZS)", competition_type_id=ct_tarcno.id, arrows=90)

        get_or_create(CompetitionSubType, name="poljski krog 12+12", competition_type_id=ct_poljsko.id, arrows=72)
        get_or_create(CompetitionSubType, name="poljski krog 24+24", competition_type_id=ct_poljsko.id, arrows=144)
        get_or_create(CompetitionSubType, name="poljski krog 12+12 ( do 2007 )", competition_type_id=ct_poljsko.id, arrows=72)
        get_or_create(CompetitionSubType, name="poljski krog 12+12 ( do 2007 )", competition_type_id=ct_poljsko.id, arrows=72)
        get_or_create(CompetitionSubType, name="poljski krog 12+12 ( do 2023 )", competition_type_id=ct_poljsko.id, arrows=72)
        get_or_create(CompetitionSubType, name="gozdni krog", competition_type_id=ct_poljsko.id, arrows=24)

        get_or_create(CompetitionSubType, name="3D krog 14 tarč", competition_type_id=ct_3d.id, arrows=14)
        get_or_create(CompetitionSubType, name="3D krog 20 tarč", competition_type_id=ct_3d.id, arrows=20)
        get_or_create(CompetitionSubType, name="3D krog 20 tarč ( 2p )", competition_type_id=ct_3d.id, arrows=40)
        get_or_create(CompetitionSubType, name="3D krog 24 tarč", competition_type_id=ct_3d.id, arrows=48)
        get_or_create(CompetitionSubType, name="3D krog 28 tarč", competition_type_id=ct_3d.id, arrows=28)
        get_or_create(CompetitionSubType, name="3D krog 28 tarč ( max 10 )", competition_type_id=ct_3d.id, arrows=28)


        get_or_create(CompetitionSubType, name="neomejeno", competition_type_id=ct_flight.id, arrows=6)
        get_or_create(CompetitionSubType, name="do 50 lbs ( 22,70 kg )", competition_type_id=ct_flight.id, arrows=6)
        get_or_create(CompetitionSubType, name="do 35 lbs ( 15,88 kg )", competition_type_id=ct_flight.id, arrows=6)
        get_or_create(CompetitionSubType, name="do 39,7 lbs ( 18 kg )", competition_type_id=ct_flight.id, arrows=6)
        get_or_create(CompetitionSubType, name="do 45 lbs ( 20,40 kg )", competition_type_id=ct_flight.id, arrows=6)
        get_or_create(CompetitionSubType, name="do 55,1 lbs ( 25 kg )", competition_type_id=ct_flight.id, arrows=6)
        get_or_create(CompetitionSubType, name="do 60 lbs ( 27,20 kg )", competition_type_id=ct_flight.id, arrows=6)

        get_or_create(CompetitionSubType, name="185m", competition_type_id=ct_clout.id, arrows=36)
        get_or_create(CompetitionSubType, name="165m", competition_type_id=ct_clout.id, arrows=36)
        get_or_create(CompetitionSubType, name="85m", competition_type_id=ct_clout.id, arrows=36)


        # -----------------------------
        # Styles
        # -----------------------------
        get_or_create(Style, name="Ukrivljeni lok")
        get_or_create(Style, name="Sestavljeni lok")
        get_or_create(Style, name="Goli lok")
        get_or_create(Style, name="Dolgi lok")
        get_or_create(Style, name="Tradicionalni lok")

        # -----------------------------
        # Genders
        # -----------------------------
        gender_male = get_or_create(Gender, name="Moški")
        gender_female = get_or_create(Gender, name="Ženske")

        db.session.commit()  # da dobijo vsi Gender ID-je

        # -----------------------------
        # Categories
        # -----------------------------
        cat_data = [
            (gender_male, ["Člani", "Starejši od 50 let", "Mlajši od 21 let", "Mlajši od 18 let", "Mlajši od 15 let", "Mlajši od 13 let"]),
            (gender_female, ["Članice", "Starejše od 50 let", "Mlajše od 21 let", "Mlajše od 18 let", "Mlajše od 15 let", "Mlajše od 13 let"])
        ]

        all_categories = []
        for gender_obj, cat_names in cat_data:
            for cat_name in cat_names:
                cat = get_or_create(Category, name=cat_name, gender_id=gender_obj.id)
                all_categories.append(cat)

        db.session.commit()  # da dobijo vsi Category ID-je

        # -----------------------------
        # SubCategories
        # -----------------------------
        get_or_create(SubCategory, name="Posamezno")
        get_or_create(SubCategory, name="Klubska ekipa")
        get_or_create(SubCategory, name="Reprezentančna ekipa")

        db.session.commit()
        print("✅ Init DB done.")


if __name__ == "__main__":
    create_tables()
