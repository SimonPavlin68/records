from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Category

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.secret_key = 'tvoj-unikaten-in-tajni-kljuc'


# Pot za domačo stran
@app.route('/')
def index():
    return render_template('index.html')


# Pot za Nazivi
@app.route('/nazivi')
def nazivi():
    return render_template('nazivi.html')


# Pot za Vrste
@app.route('/vrste', methods=['GET', 'POST'])
def vrste():
    if request.method == 'POST':
        # Dodajanje nove kategorije v bazo
        new_category = Category(
            discipline=request.form['discipline'],
            style=request.form['style'],
            gender=request.form['gender'],
            face=request.form['face'],
            type=request.form['type'],
            name=request.form['name'],
            category_type=request.form['category_type']  # Dodali smo tudi category_type
        )
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('vrste'))  # Preusmeritev nazaj na seznam kategorij

    categories = Category.query.all()  # Pridobimo vse kategorije
    return render_template('vrste.html', categories=categories)


@app.route('/delete_category', methods=['POST'])
def delete_category():
    category_id = request.form.get('category_id')

    # Preveri, če ID obstaja
    if category_id:
        category = Category.query.get(category_id)  # Poiščemo kategorijo v bazi
        if category:
            db.session.delete(category)  # Izbrišemo kategorijo
            db.session.commit()  # Shranimo spremembe
            flash(f'Kategorija "{category.name}" je bila uspešno izbrisana!', 'success')
        else:
            flash('Kategorija ni bila najdena.', 'danger')
    else:
        flash('ID kategorije ni bil poslan.', 'danger')

    # Po končanem izbrisu preusmerimo nazaj na seznam kategorij
    return redirect(url_for('vrste'))  # Preusmeritev na seznam vrst


# Pot za Rekorde (z dinamičnim nalaganjem kategorij)
@app.route('/rekordi')
def rekordi():
    categories = Category.query.filter_by(parent_id=None).all()  # Pridobimo vse glavne kategorije
    # Poiščemo podkategorije za vsako kategorijo
    for category in categories:
        category.children = Category.query.filter_by(parent_id=category.id).all()
        for subcategory in category.children:
            subcategory.children = Category.query.filter_by(parent_id=subcategory.id).all()

    return render_template('rekordi.html', categories=categories)


# Pot za Nastavitve
@app.route('/nastavitve')
def nastavitve():
    return render_template('nastavitve.html')


# Pot za O programu
@app.route('/o_programu')
def o_programu():
    return render_template('o_programu.html')


if __name__ == '__main__':
    app.run(debug=True)
