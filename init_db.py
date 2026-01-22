from app import app
from models import db, CompetitionType, Style, Gender, Category, SubCategory

def get_or_create(model, **kwargs):
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
        get_or_create(CompetitionType, name="Tarčno")
        get_or_create(CompetitionType, name="Poljsko")
        get_or_create(CompetitionType, name="Dvorana")
        get_or_create(CompetitionType, name="3D")
        get_or_create(CompetitionType, name="Clout")
        get_or_create(CompetitionType, name="Flight")

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
        get_or_create(Gender, name="Moški")
        get_or_create(Gender, name="Ženske")
        get_or_create(Gender, name="Alien")  # Dodano

        # -----------------------------
        # Categories
        # -----------------------------
        get_or_create(Category, name="Člani")
        get_or_create(Category, name="Članice")
        get_or_create(Category, name="Starejši od 50 let")
        get_or_create(Category, name="Starejše od 50 let")
        get_or_create(Category, name="Mlajši od 21 let")
        get_or_create(Category, name="Mlajše od 21 let")
        get_or_create(Category, name="Mlajši od 18 let")
        get_or_create(Category, name="Mlajše od 18 let")
        get_or_create(Category, name="Mlajši od 15 let")
        get_or_create(Category, name="Mlajše od 15 let")
        get_or_create(Category, name="Mlajši od 13 let")
        get_or_create(Category, name="Mlajše od 13 let")

        # -----------------------------
        # SubCategories (brez povezave na Category)
        # -----------------------------
        get_or_create(SubCategory, name="Posamezno", category_id=1)
        get_or_create(SubCategory, name="Klubska ekipa", category_id=1)
        get_or_create(SubCategory, name="Reprezentančna ekipa", category_id=1)

        db.session.commit()

        print("✅ Init DB done.")


if __name__ == "__main__":
    create_tables()
