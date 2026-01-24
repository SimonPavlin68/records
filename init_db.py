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
        ct_tarco = get_or_create(CompetitionType, name="Tarčno")
        ct_poljsko = get_or_create(CompetitionType, name="Poljsko")
        ct_dvorana = get_or_create(CompetitionType, name="Dvorana")
        ct_3d = get_or_create(CompetitionType, name="3D")
        ct_clout = get_or_create(CompetitionType, name="Clout")
        ct_flight = get_or_create(CompetitionType, name="Flight")

        db.session.commit()  # da dobijo vsi ID-je

        # -----------------------------
        # Competition SubTypes
        # -----------------------------
        get_or_create(CompetitionSubType, name="70m krog", competition_type_id=ct_tarco.id, arrows=72)
        get_or_create(CompetitionSubType, name="70m dvojni krog", competition_type_id=ct_tarco.id, arrows=144)
        get_or_create(CompetitionSubType, name="poljski krog 12+12", competition_type_id=ct_poljsko.id, arrows=72)
        get_or_create(CompetitionSubType, name="18m", competition_type_id=ct_dvorana.id, arrows=60)
        get_or_create(CompetitionSubType, name="25m", competition_type_id=ct_dvorana.id, arrows=60)
        get_or_create(CompetitionSubType, name="25m + 18m", competition_type_id=ct_dvorana.id, arrows=120)

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
