from app import app
from models import CompetitionType, Style, Gender, Category, SubCategory


def read_all_tables():
    with app.app_context():
        # Preberemo vse CompetitionTypes
        competition_types = CompetitionType.query.all()
        print("Competition Types:")
        for competition_type in competition_types:
            print(f"ID: {competition_type.id}, Name: {competition_type.name}")

        # Preberemo vse Style
        styles = Style.query.all()
        print("\nStyles:")
        for style in styles:
            print(f"ID: {style.id}, Name: {style.name}")

        # Preberemo vse Gender
        genders = Gender.query.all()
        print("\nGenders:")
        for gender in genders:
            print(f"ID: {gender.id}, Name: {gender.name}")

        # Preberemo vse Category
        categories = Category.query.all()
        print("\nCategories:")
        for category in categories:
            print(f"ID: {category.id}, Name: {category.name}")

        # Preberemo vse SubCategory
        subcategories = SubCategory.query.all()
        print("\nSubCategories:")
        for subcategory in subcategories:
            print(f"ID: {subcategory.id}, Name: {subcategory.name}")


if __name__ == "__main__":
    read_all_tables()
