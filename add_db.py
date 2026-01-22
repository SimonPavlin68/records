from app import app, db
from models import Category  # Uvozi model Category


def add_test_data():
    with app.app_context():  # Omogoči aplikacijsko okolje
        # Dodaj nekaj testnih kategorij
        category1 = Category(
            discipline='Tarčno',
            style='Ukrivljeni lok',
            gender='M',
            face='122cm',
            type='Posamezno',
            name='Člani'
        )
        category2 = Category(
            discipline='Dvorana',
            style='Sestavljeni lok',
            gender='Ž',
            face='40cm',
            type='Ekipa',
            name='Mlajše od 21 let'
        )

        # Dodaj v sejo
        db.session.add(category1)
        db.session.add(category2)

        # Shranimo spremembe v bazo
        db.session.commit()

        print("Testne kategorije so bile dodane.")


if __name__ == "__main__":
    add_test_data()
