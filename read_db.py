from app import app
from models import RecordType

def list_record_types():
    with app.app_context():
        record_types = RecordType.query.order_by(RecordType.id).all()
        if not record_types:
            print("❌ Ni nobenih RecordType v bazi.")
            return

        print(f"📋 Vse RecordType ({len(record_types)}):\n")
        for rt in record_types:
            print(
                f"ID {rt.id} | Name: {rt.name} | "
                f"CompType: {rt.competition_type.name} | "
                f"Style: {rt.style.name} | "
                f"Gender: {rt.gender.name} | "
                f"Category: {rt.category.name} | "
                f"SubCategory: {rt.subcat.name} | "
                f"Arrows: {rt.arrow_count} | Face: {rt.face} | "
                f"Active: {'✅' if rt.is_active else '❌'}"
            )


if __name__ == "__main__":
    list_record_types()
