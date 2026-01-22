from app import app, db
from models import CompetitionType, Style, Gender, Category, SubCategory, RecordType

def add_record_type(tip, lok, spol, kat, ime="Rekord type 1", arrow_count=72, face=None):
    with app.app_context():
        print(f"Trying to add RecordType for: {tip}, {lok}, {spol}, {kat}")

        # 1️⃣ CompetitionType
        comp = CompetitionType.query.filter_by(name=tip).first()
        if not comp:
            print(f"❌ CompetitionType '{tip}' not found!")
            return
        print(f"Found CompetitionType: {comp.name} (ID {comp.id})")

        # 2️⃣ Style
        style = Style.query.filter_by(name=lok).first()
        if not style:
            print(f"❌ Style '{lok}' not found!")
            return
        print(f"Found Style: {style.name} (ID {style.id})")

        # 3️⃣ Gender
        gender = Gender.query.filter_by(name=spol).first()
        if not gender:
            print(f"❌ Gender '{spol}' not found!")
            return
        print(f"Found Gender: {gender.name} (ID {gender.id})")

        # 4️⃣ Category
        category = Category.query.filter_by(name=kat).first()
        if not category:
            print(f"❌ Category '{kat}' not found!")
            return
        print(f"Found Category: {category.name} (ID {category.id})")

        # 5️⃣ SubCategory → Posamezno (brez povezave na category)
        subcat = SubCategory.query.filter_by(name="Posamezno").first()
        if not subcat:
            print(f"❌ SubCategory 'Posamezno' not found!")
            return
        print(f"Found SubCategory: {subcat.name} (ID {subcat.id})")

        # 6️⃣ Preverimo, če RecordType že obstaja
        existing = RecordType.query.filter_by(
            competition_type_id=comp.id,
            style_id=style.id,
            gender_id=gender.id,
            category_id=category.id,
            subcategory_id=subcat.id
        ).first()
        if existing:
            print(f"⚠️ RecordType že obstaja: {existing.name} (ID {existing.id})")
            return

        # 7️⃣ Dodajanje RecordType
        record_type = RecordType(
            name=ime,
            competition_type_id=comp.id,
            style_id=style.id,
            gender_id=gender.id,
            category_id=category.id,
            subcategory_id=subcat.id,
            arrow_count=arrow_count,
            face=face,
            is_active=True
        )
        db.session.add(record_type)
        db.session.commit()
        print(f"✅ RecordType '{record_type.name}' added successfully with ID {record_type.id}")


if __name__ == "__main__":
    # Primeri
    add_record_type(
        "Poljsko", "Sestavljeni lok", "Ženske", "Mlajše od 15 let",
        ime="Poljsko Sestavljeni – Ženske U15"
    )
    add_record_type(
        "3D", "Sestavljeni lok", "Moški", "Mlajši od 15 let",
        ime="3D Sestavljeni – Moški U15", arrow_count=24, face="3D živali"
    )
    add_record_type(
        "Tarčno", "Goli lok", "Moški", "Starejši od 50 let",
        ime="Tarčno Goli – Moški 50+", arrow_count=72, face="122 cm"
    )
