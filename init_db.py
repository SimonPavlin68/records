from app import app
from models import db, CompetitionType, Style, Gender, Category, SubCategory

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
        ct_tar = get_or_create(CompetitionType, name="Tarčno")
        ct_pol = get_or_create(CompetitionType, name="Poljsko")
        ct_dvor = get_or_create(CompetitionType, name="Dvorana")
        ct_3d = get_or_create(CompetitionType, name="3D")
        ct_clout = get_or_create(CompetitionType, name="Clout")
        ct_flight = get_or_create(CompetitionType, name="Flight")

        # -----------------------------
        # Styles
        # -----------------------------
        style_recurve = get_or_create(Style, name="Ukrivljeni lok")
        style_compound = get_or_create(Style, name="Sestavljeni lok")
        style_barebow = get_or_create(Style, name="Goli lok")
        style_longbow = get_or_create(Style, name="Dolgi lok")
        style_traditional = get_or_create(Style, name="Tradicionalni lok")

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
        # SubCategories (vedno vežejo Category)
        # -----------------------------
        subcat_names = ["Posamezno", "Klubska ekipa", "Reprezentančna ekipa"]
        for category in all_categories:
            for name in subcat_names:
                get_or_create(SubCategory, name=name, category_id=category.id)

        db.session.commit()
        print("✅ Init DB done.")

if __name__ == "__main__":
    create_tables()
