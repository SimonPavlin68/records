from app import app, db
from models import CompetitionType, Style, Gender, Category, SubCategory, RecordType

def add_test_data():
    with app.app_context():  # Uporabimo aplikacijski kontekst
        # Poiščemo "Poljsko" tekmovanje
        poljsko = CompetitionType.query.filter_by(name='Poljsko').first()
        # Poiščemo stil "Sestavljeni lok"
        sestavljeni_lok = Style.query.filter_by(name='Sestavljeni lok', competition_type_id=poljsko.id).first()
        # Poiščemo spol "Ženske"
        zenske = Gender.query.filter_by(name='Ženske').first()
        # Poiščemo kategorijo "Mlajše od 18 let" za ženske
        mlajse_od_18 = Category.query.filter_by(name='Mlajše od 18 let', gender_id=zenske.id).first()
        # Poiščemo podkategorijo "Posamezno"
        posamezno = SubCategory.query.filter_by(name='Posamezno', category_id=mlajse_od_18.id).first()

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

        print("RecordType je bil uspešno dodan.")

if __name__ == "__main__":
    add_test_data()
