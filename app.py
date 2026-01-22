from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Category, CompetitionType, RecordType, Style, Gender, SubCategory

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


@app.route('/vrste')
def vrste():
    # Naložimo vse tipe tekmovanja z vsemi povezavami
    competition_types = CompetitionType.query.options(
        db.joinedload(CompetitionType.styles)
          .joinedload(Style.genders)
          .joinedload(Gender.categories)
          .joinedload(Category.subcategories)
          .joinedload(SubCategory.record_types)
    ).all()

    return render_template('vrste.html', competition_types=competition_types)


@app.route('/get_record_types/<int:subcategory_id>')
def get_record_types(subcategory_id):
    subcategory = SubCategory.query.options(
        db.joinedload(SubCategory.record_types)
    ).get(subcategory_id)

    if subcategory and subcategory.record_types:
        data = [{
            'id': r.id,
            'name': r.name,
            'arrow_count': r.arrow_count,
            'face': r.face,
            'is_active': r.is_active
        } for r in subcategory.record_types]
    else:
        data = []

    return jsonify(data)


@app.route('/get_styles/<int:competition_type_id>', methods=['GET'])
def get_styles(competition_type_id):
    styles = Style.query.filter_by(competition_type_id=competition_type_id).all()
    return jsonify([{'id': style.id, 'name': style.name} for style in styles])


@app.route('/get_genders/<int:style_id>', methods=['GET'])
def get_genders(style_id):
    genders = Gender.query.filter_by(style_id=style_id).all()
    return jsonify([{'id': gender.id, 'name': gender.name} for gender in genders])


@app.route('/get_categories/<int:gender_id>', methods=['GET'])
def get_categories(gender_id):
    categories = Category.query.filter_by(gender_id=gender_id).all()
    return jsonify([{'id': category.id, 'name': category.name} for category in categories])


@app.route('/get_subcategories/<int:category_id>', methods=['GET'])
def get_subcategories(category_id):
    subcategories = SubCategory.query.filter_by(category_id=category_id).all()
    return jsonify([{'id': subcategory.id, 'name': subcategory.name} for subcategory in subcategories])


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
