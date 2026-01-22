from app import app, db
from models import CompetitionType, Style, Gender, Category, SubCategory, RecordType

def add_test_data(tip, lok, spol, kat):
    with app.app_context():  # Uporabimo aplikacijski kontekst
        print(f"Trying to add data for {tip}, {lok}, {spol}, {kat}")

        # Poiščemo CompetitionType z imenom, ki ga podamo
        poljsko = CompetitionType.query.filter_by(name=tip).first()
        if poljsko:
            print(f"Found competition type: {poljsko.name} (ID: {poljsko.id})")
        else:
            print(f"CompetitionType with name '{tip}' not found!")
            return  # Izhod, če tekmovanje ni najdeno

        # Poiščemo Style
        sestavljeni_lok = Style.query.filter_by(name=lok, competition_type_id=poljsko.id).first()
        if sestavljeni_lok:
            print(f"Found style: {sestavljeni_lok.name} (ID: {sestavljeni_lok.id})")
        else:
            print(f"Style with name '{lok}' not found!")
            return

        # Poiščemo Gender
        zenske = Gender.query.filter_by(name=spol).first()
        if zenske:
            print(f"Found gender: {zenske.name} (ID: {zenske.id})")
        else:
            print(f"Gender '{spol}' not found!")
            return

        # Poiščemo Category
        mlajse_od_18 = Category.query.filter_by(name=kat, gender_id=zenske.id).first()
        if mlajse_od_18:
            print(f"Found category: {mlajse_od_18.name} (ID: {mlajse_od_18.id})")
        else:
            print(f"Category '{kat}' not found for gender '{spol}'!")
            return

        # Poiščemo SubCategory
        posamezno = SubCategory.query.filter_by(name='Posamezno', category_id=mlajse_od_18.id).first()
        if posamezno:
            print(f"Found subcategory: {posamezno.name} (ID: {posamezno.id})")
        else:
            print(f"SubCategory 'Posamezno' not found for category '{kat}'!")
            return

        # Dodajanje enega RecordType
        record_type = RecordType(
            name="Rekord type 1",  # Tukaj lahko spreminjaš ime rekorda po potrebi
            subcategory_id=posamezno.id,  # Povežemo z ustrezno podkategorijo
            arrow_count=72,  # 72 puščic
            face=None,  # Ni velikosti lice (face), lahko dodaš, če je potrebno
            is_active=True  # Aktivni rekord
        )

        # Dodajamo v bazo
        db.session.add(record_type)
        db.session.commit()

        print(f"RecordType '{record_type.name}' added successfully with ID {record_type.id}.")

if __name__ == "__main__":
    add_test_data("Poljsko", "Sestavljeni lok", "Ženske", "Mlajše od 15 let")
    add_test_data("3D", "Sestavljeni lok", "Moški", "Mlajši od 15 let")
    add_test_data("Tarčno", "Goli lok", "Moški", "Starejši od 50 let")
