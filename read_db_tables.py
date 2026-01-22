from app import app, db
from models import CompetitionType, Style, Gender, Category, SubCategory, RecordType


def read_all_tables():
    with app.app_context():
        # Preberemo vse CompetitionTypes
        competition_types = CompetitionType.query.all()
        print("Competition Types:")
        for competition_type in competition_types:
            print(f"ID: {competition_type.id}, Name: {competition_type.name}")
        #    for style in competition_type.styles:
        #        print(f"  Style: {style.name}, ID: {style.id}")
        #        for gender in style.genders:
        #            print(f"    Gender: {gender.name}, ID: {gender.id}")
        #            for category in gender.categories:
        #                print(f"      Category: {category.name}, ID: {category.id}")
        #                for subcategory in category.subcategories:
        #                    print(f"        SubCategory: {subcategory.name}, ID: {subcategory.id}")
        #                    for record_type in subcategory.record_types:
        #                        print(f"          RecordType: {record_type.name}, ID: {record_type.id}")

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

        # Preberemo vse RecordTypes
        record_types = RecordType.query.all()
        print("\nRecord Types:")
        for record in record_types:
            print(
                f"ID: {record.id}, Name: {record.name}, Arrow Count: {record.arrow_count}, Face: {record.face}, Active: {record.is_active}")


if __name__ == "__main__":
    read_all_tables()
