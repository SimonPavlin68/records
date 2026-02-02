# Seznam kategorij
cat_data = [
    ("Ženske", ["Članice", "Mlajše od 21 let", "Mlajše od 18 let", "Mlajše od 15 let", "Mlajše od 13 let", "Starejše od 50 let"]),
    ("Moški", ["Člani", "Mlajši od 21 let", "Mlajši od 18 let", "Mlajši od 15 let", "Mlajši od 13 let", "Starejši od 50 let"]),
    ("Mix", ["Slepi in slabovidni", "Članska", "Mlajši od 21", "Mlajši od 18", "Mlajši od 15", "Mlajši od 13"])
]


def get_gender_name(row):
    """Funkcija za določanje spola na podlagi kategorije"""
    for gender_name, cat_names in cat_data:
        if row[2] in cat_names:
            return gender_name
    return None  # Če ni najdena kategorija
