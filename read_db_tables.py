from app import app
from models import CompetitionType, CompetitionSubType, Style, Gender, Category, SubCategory

def read_all_tables():
    with app.app_context():
        # -----------------------------
        # Competition Types
        # -----------------------------
        competition_types = CompetitionType.query.all()
        print("Competition Types:")
        for competition_type in competition_types:
            print(f"ID: {competition_type.id}, Name: {competition_type.name}")

        # -----------------------------
        # Competition SubTypes
        # -----------------------------
        subtypes = CompetitionSubType.query.all()
        print("\nCompetition SubTypes:")
        for subtype in subtypes:
            print(f"ID: {subtype.id}, Name: {subtype.name}, Type: {subtype.competition_type.name}, Arrows: {subtype.arrows}")

        # -----------------------------
        # Styles
        # -----------------------------
        styles = Style.query.all()
        print("\nStyles:")
        for style in styles:
            print(f"ID: {style.id}, Name: {style.name}")

        # -----------------------------
        # Genders
        # -----------------------------
        genders = Gender.query.all()
        print("\nGenders:")
        for gender in genders:
            print(f"ID: {gender.id}, Name: {gender.name}")

        # -----------------------------
        # Categories
        # -----------------------------
        categories = Category.query.all()
        print("\nCategories:")
        for category in categories:
            print(f"ID: {category.id}, Name: {category.name}, Gender: {category.gender.name}")

        # -----------------------------
        # SubCategories
        # -----------------------------
        subcategories = SubCategory.query.all()
        print("\nSubCategories:")
        for subcategory in subcategories:
            print(f"ID: {subcategory.id}, Name: {subcategory.name}")

if __name__ == "__main__":
    read_all_tables()
