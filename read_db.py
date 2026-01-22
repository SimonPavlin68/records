# read_db.py
from app import app, db
from models import RecordType


def read_record_types():
    with app.app_context():
        # Poiščemo vse tipe rekorda
        record_types = RecordType.query.all()

        if record_types:
            for record in record_types:
                print(f"Record type ID: {record.id}, Name: {record.name}, "
                      f"Arrow Count: {record.arrow_count}, Face: {record.face}, "
                      f"Active: {record.is_active}")
                print(f"  Subcategory: {record.subcategory.name}")
                print(f"    Category: {record.subcategory.category.name}")
                print(f"      Gender: {record.subcategory.category.gender.name}")
                print(f"        Style: {record.subcategory.category.gender.style.name}")
                print(f"          Competition Type: {record.subcategory.category.gender.style.competition_type.name}\n")
        else:
            print("Ni bilo najdenih vnosov.")


if __name__ == "__main__":
    read_record_types()
