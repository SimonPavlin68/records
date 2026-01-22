from flask import Flask, render_template, jsonify
from models import db, Category, CompetitionType, RecordType, Style, Gender, SubCategory

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.secret_key = 'tvoj-unikaten-in-tajni-kljuc'


# ============================================================
# Strani
# ============================================================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/nazivi')
def nazivi():
    return render_template('nazivi.html')

@app.route("/record_types")
def record_types_view():
    competition_types = CompetitionType.query.order_by(CompetitionType.name).all()
    categories = Category.query.order_by(Category.name).all()
    subcategories = SubCategory.query.order_by(SubCategory.name).all()

    # Drevesna struktura za template
    tree = {}
    for comp in competition_types:
        comp_styles = Style.query.order_by(Style.name).all()
        tree[comp.id] = {'obj': comp, 'styles': {}}
        for style in comp_styles:
            tree[comp.id]['styles'][style.id] = {'obj': style, 'genders': {}}
            for gender in Gender.query.order_by(Gender.name).all():
                tree[comp.id]['styles'][style.id]['genders'][gender.id] = {'obj': gender, 'categories': {}}
                for category in categories:
                    tree[comp.id]['styles'][style.id]['genders'][gender.id]['categories'][category.id] = {
                        'obj': category,
                        'subcategories': {sc.id: sc for sc in subcategories if sc.category_id == category.id}
                    }

    return render_template("record_types.html", tree=tree)


@app.route('/get_record_types/<int:subcategory_id>')
def get_record_types(subcategory_id):
    subcat = SubCategory.query.get(subcategory_id)
    if subcat:
        data = [{
            'id': r.id,
            'name': r.name,
            'arrow_count': r.arrow_count,
            'face': r.face,
            'is_active': r.is_active
        } for r in subcat.record_types]
    else:
        data = []
    return jsonify(data)


@app.route('/get_record_types_for_subcategory/<int:subcategory_id>')
def get_record_types_count_subcategory(subcategory_id):
    count = RecordType.query.filter_by(subcategory_id=subcategory_id).count()
    return jsonify({'record_types_count': count})

# ============================================================
# API endpoint-i za RecordTypes
# ============================================================
@app.route('/get_record_types_for_competition_type/<int:competition_type_id>', methods=['GET'])
def get_record_types_for_competition_type(competition_type_id):
    # Preštej vse RecordType, ki imajo competition_type_id
    count = RecordType.query.filter_by(competition_type_id=competition_type_id).count()
    return jsonify({'record_types_count': count})



@app.route('/get_record_types_for_style/<int:style_id>', methods=['GET'])
def get_record_types_for_style(style_id):
    count = RecordType.query.filter_by(style_id=style_id).count()
    return jsonify({'record_types_count': count})


@app.route('/get_record_types_for_gender/<int:gender_id>', methods=['GET'])
def get_record_types_for_gender(gender_id):
    count = RecordType.query.filter_by(gender_id=gender_id).count()
    return jsonify({'record_types_count': count})


@app.route('/get_record_types_for_category/<int:category_id>', methods=['GET'])
def get_record_types_for_category(category_id):
    count = RecordType.query.filter_by(category_id=category_id).count()
    return jsonify({'record_types_count': count})


@app.route('/get_subcategories/<int:category_id>', methods=['GET'])
def get_subcategories(category_id):
    subcategories = SubCategory.query.filter_by(category_id=category_id).all()
    return jsonify([{'id': sc.id, 'name': sc.name} for sc in subcategories])


# ============================================================
# Rekordi
# ============================================================

@app.route('/rekordi')
def rekordi():
    categories = Category.query.filter_by(parent_id=None).all()
    # Če rabiš podkategorije
    for category in categories:
        category.children = Category.query.filter_by(parent_id=category.id).all()
        for subcategory in category.children:
            subcategory.children = Category.query.filter_by(parent_id=subcategory.id).all()
    return render_template('rekordi.html', categories=categories)


@app.route('/nastavitve')
def nastavitve():
    return render_template('nastavitve.html')


@app.route('/o_programu')
def o_programu():
    return render_template('o_programu.html')


if __name__ == '__main__':
    app.run(debug=True)
