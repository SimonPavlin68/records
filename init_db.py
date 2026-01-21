from models import db, Category
from app import app  # Uvozimo aplikacijo za uporabo njenega konteksta

# Uporabimo kontekst aplikacije za dostop do baze
with app.app_context():
    # Izbrišemo vse tabele (če obstajajo)
    db.drop_all()  # Izbriše vse tabele v bazi
    print("Vse tabele so bile izbrisane.")

    # Ponovno ustvarimo vse tabele (vključno z 'category' in 'records')
    db.create_all()
    print("Vse tabele so bile ponovno ustvarjene.")

    # Inicializacija kategorij (če so še prazne)
    if not Category.query.first():  # Samo, če so kategorije še prazne
        # Dodajamo glavne discipline
        tarcno = Category(name="Tarčno", discipline="Tarčno", style="Ukrivljeni lok", gender="M/Ž", face="40cm", type="Posamezno", category_type="18m")
        dvoransko = Category(name="Dvoransko", discipline="Dvoransko", style="Sestavljeni lok", gender="M/Ž", face="60cm", type="Ekipno", category_type="20m")
        three_d = Category(name="3D", discipline="3D", style="Goli lok", gender="M/Ž", face="40cm", type="Posamezno", category_type="30m")
        clout = Category(name="Clout", discipline="Clout", style="Dolgi lok", gender="M/Ž", face="100cm", type="Ekipno", category_type="40m")
        flight = Category(name="Flight", discipline="Flight", style="Tradicionalni lok", gender="M/Ž", face="50cm", type="Posamezno", category_type="50m")

        db.session.add_all([tarcno, dvoransko, three_d, clout, flight])
        db.session.commit()

        # Dodajmo podkategorije za "Tarčno"
        ukrivljeni_lok = Category(name="Ukrivljeni lok", parent=tarcno, discipline="Tarčno", style="Ukrivljeni lok", gender="M/Ž", face="40cm", type="Posamezno", category_type="18m")
        sestavljeni_lok = Category(name="Sestavljeni lok", parent=tarcno, discipline="Tarčno", style="Sestavljeni lok", gender="M/Ž", face="40cm", type="Posamezno", category_type="18m")
        goli_lok = Category(name="Goli lok", parent=tarcno, discipline="Tarčno", style="Goli lok", gender="M/Ž", face="40cm", type="Posamezno", category_type="18m")
        dolgi_lok = Category(name="Dolgi lok", parent=tarcno, discipline="Tarčno", style="Dolgi lok", gender="M/Ž", face="40cm", type="Posamezno", category_type="18m")
        tradicionalni_lok = Category(name="Tradicionalni lok", parent=tarcno, discipline="Tarčno", style="Tradicionalni lok", gender="M/Ž", face="40cm", type="Posamezno", category_type="18m")

        db.session.add_all([ukrivljeni_lok, sestavljeni_lok, goli_lok, dolgi_lok, tradicionalni_lok])
        db.session.commit()

        print("Baza je bila inicializirana z začetnimi podatki!")
    else:
        print("Baza je že inicializirana.")
