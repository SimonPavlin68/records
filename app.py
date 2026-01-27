from flask import Flask, render_template, request, flash, redirect, url_for
from models import db, CompetitionType, Style, Gender, Category, SubCategory, CompetitionSubType, Record
from datetime import datetime

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


# ============================================================
# Rekordi
# ============================================================

@app.route('/rekordi_old')
def rekordi_old():
    records = (
        Record.query
        .order_by(Record.date.desc())
        .all()
    )
    return render_template(
        'rekordi.html',
        records=records,
        competition_types=CompetitionType.query.all(),
        competition_subtypes=CompetitionSubType.query.all(),
        styles=Style.query.all(),
        genders=Gender.query.all(),
        categories=Category.query.all(),
        subcategories=SubCategory.query.all()
    )

@app.route('/rekordi')
def rekordi():
    q = Record.query

    if request.args.get('competitor'):
        q = q.filter(Record.competitor_name.ilike(
            f"%{request.args['competitor']}%"))

    if request.args.get('club'):
        q = q.filter(Record.club.ilike(
            f"%{request.args['club']}%"))

    if request.args.get('location'):
        q = q.filter(Record.location.ilike(
            f"%{request.args['location']}%"))

    if request.args.get('gender'):
        q = q.filter(Record.gender_id == request.args['gender'])

    if request.args.get('competition_type'):
        q = q.filter(Record.competition_type_id ==
                     request.args['competition_type'])

    if request.args.get('competition_subtype'):
        q = q.filter(Record.competition_subtype_id ==
                     request.args['competition_subtype'])

    if request.args.get('style'):
        q = q.filter(Record.style_id == request.args['style'])

    if request.args.get('category'):
        q = q.filter(Record.category_id ==
                     request.args['category'])

    if request.args.get('subcategory'):
        q = q.filter(Record.subcategory_id ==
                     request.args['subcategory'])

    if request.args.get('date_from'):
        q = q.filter(Record.date >= request.args['date_from'])

    if request.args.get('date_to'):
        q = q.filter(Record.date <= request.args['date_to'])

    records = q.order_by(Record.date.desc()).all()

    return render_template(
        'rekordi.html',
        records=records,
        genders=Gender.query.all(),
        competition_types=CompetitionType.query.all(),
        competition_subtypes=CompetitionSubType.query.all(),
        styles=Style.query.all(),
        categories=Category.query.all(),
        subcategories=SubCategory.query.all()
    )


@app.route('/rekordi/new', methods=['POST'])
def record_new():
    competitor_name = request.form.get("competitor_name")
    team = [
        request.form.get("team_1"),
        request.form.get("team_2"),
        request.form.get("team_3"),
    ]
    team = [t.strip() for t in team if t and t.strip()]
    if team:
        competitor_name = ", ".join(team)

    r = Record(
        competitor_name=competitor_name,
        club=request.form.get('club'),
        result=request.form['result'],
        location=request.form.get('location'),

        date=datetime.strptime(
            request.form['date'],
            "%Y-%m-%d"
        ).date(),

        competition_type_id=request.form['competition_type_id'],
        competition_subtype_id=request.form.get('competition_subtype_id') or None,
        style_id=request.form['style_id'],
        gender_id=request.form['gender_id'],
        category_id=request.form['category_id'],
        subcategory_id=request.form.get('subcategory_id') or None
    )

    db.session.add(r)
    db.session.commit()

    return redirect(url_for('rekordi'))


@app.route('/rekordi/edit/<int:id>', methods=['POST'])
def record_edit(id):
    r = Record.query.get_or_404(id)
    form = request.form
    r.competitor_name = form['competitor_name']
    r.club = form.get('club')
    r.result = form['result']
    r.location = form.get('location')
    r.date = datetime.strptime(form['date'], '%Y-%m-%d').date()
    r.competition_type_id = form['competition_type_id']
    r.competition_subtype_id = form.get('competition_subtype_id') or None
    r.style_id = form['style_id']
    r.gender_id = form['gender_id']
    r.category_id = form['category_id']
    r.subcategory_id = form.get('subcategory_id') or None
    db.session.commit()
    return redirect(url_for('rekordi'))


@app.route('/rekordi/delete/<int:id>', methods=['POST'])
def record_delete(id):
    r = Record.query.get_or_404(id)
    db.session.delete(r)
    db.session.commit()
    return redirect(url_for('rekordi'))



@app.route('/nastavitve')
def nastavitve():
    # Query iz baze
    competition_items = CompetitionType.query.order_by(CompetitionType.id).all()
    style_items = Style.query.order_by(Style.id).all()
    category_items = Category.query.order_by(Category.id).all()
    genders = Gender.query.order_by(Gender.id).all()
    subcategory_items = SubCategory.query.order_by(SubCategory.id).all()
    competition_subtype_items = CompetitionSubType.query.order_by(CompetitionSubType.id).all()

    return render_template(
        'nastavitve.html',
        competition_items=competition_items,
        style_items=style_items,
        category_items=category_items,
        genders=genders,
        subcategory_items=subcategory_items,
        competition_subtype_items=competition_subtype_items,
    )


@app.route('/nastavitve/new_competition_type', methods=['POST'])
def new_competition_type():
    name = request.form.get('name').strip()
    if name:
        exists = CompetitionType.query.filter(db.func.lower(CompetitionType.name) == name.lower()).first()
        if exists:
            flash(f'Competition Type "{name}" že obstaja!', 'danger')
        else:
            new_ct = CompetitionType(name=name)
            db.session.add(new_ct)
            db.session.commit()
            flash(f'Competition Type "{name}" dodan!', 'success')
    return redirect(url_for('nastavitve', tab='competition'))


@app.route('/nastavitve/delete_competition_type/<int:idd>', methods=['POST'])
def delete_competition_type(idd):
    ct = CompetitionType.query.get_or_404(idd)
    db.session.delete(ct)
    db.session.commit()
    flash(f'Competition Type "{ct.name}" je bil izbrisan!', 'success')
    return redirect(url_for('nastavitve', tab='competition'))


@app.route('/nastavitve/edit_competition_type/<int:idd>', methods=['POST'])
def edit_competition_type(idd):
    ct = CompetitionType.query.get_or_404(idd)
    new_name = request.form.get('name').strip()
    if new_name:
        exists = CompetitionType.query.filter(
            db.func.lower(CompetitionType.name) == new_name.lower(),
            CompetitionType.id != idd
        ).first()
        if exists:
            flash(f'Competition Type "{new_name}" že obstaja!', 'danger')
        else:
            ct.name = new_name
            db.session.commit()
            flash(f'Competition Type posodobljen na "{new_name}"!', 'success')
    return redirect(url_for('nastavitve', tab='competition'))


# =====================
# STYLE CRUD
# =====================

@app.route('/nastavitve/new_style', methods=['POST'])
def new_style():
    name = request.form.get('name').strip()
    if not name:
        flash("Ime je obvezno", "danger")
        return redirect(url_for('nastavitve'))
    exists = Style.query.filter(db.func.lower(Style.name) == name.lower()).first()
    if exists:
        flash(f'Style "{name}" že obstaja!', "danger")
        return redirect(url_for('nastavitve'))
    new_item = Style(name=name)
    db.session.add(new_item)
    db.session.commit()
    flash(f'Style "{name}" dodan!', "success")
    return redirect(url_for('nastavitve', tab='style'))


@app.route('/nastavitve/edit_style/<int:idd>', methods=['POST'])
def edit_style(idd):
    st = Style.query.get_or_404(idd)
    new_name = request.form.get('name').strip()
    if new_name:
        exists = Style.query.filter(db.func.lower(Style.name) == new_name.lower(), Style.id != idd).first()
        if exists:
            flash(f'Style "{new_name}" že obstaja!', "danger")
        else:
            st.name = new_name
            db.session.commit()
            flash(f'Style posodobljen na "{new_name}"!', "success")
    return redirect(url_for('nastavitve', tab='style'))


@app.route('/nastavitve/delete_style/<int:idd>', methods=['POST'])
def delete_style(idd):
    st = Style.query.get_or_404(idd)
    db.session.delete(st)
    db.session.commit()
    flash(f'Style "{st.name}" izbrisan!', "success")
    return redirect(url_for('nastavitve', tab='style'))


@app.route('/nastavitve/new_category', methods=['POST'])
def new_category():
    name = request.form['name']
    gender_id = request.form['gender_id']
    parent_id = request.form.get('parent_id') or None

    category = Category(
        name=name,
        gender_id=gender_id,
        parent_id=parent_id
    )
    db.session.add(category)
    db.session.commit()

    return redirect(url_for('nastavitve', tab='category'))


@app.route('/nastavitve/edit_category/<int:idd>', methods=['POST'])
def edit_category(idd):
    category = Category.query.get_or_404(idd)

    category.name = request.form['name']
    category.gender_id = request.form['gender_id']
    category.parent_id = request.form.get('parent_id') or None

    db.session.commit()
    return redirect(url_for('nastavitve', tab='category'))


@app.route('/nastavitve/delete_category/<int:idd>', methods=['POST'])
def delete_category(idd):
    category = Category.query.get_or_404(idd)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('nastavitve', tab='category'))

@app.route('/nastavitve/new_subcategory', methods=['POST'])
def new_subcategory():
    name = request.form.get('name', '').strip()

    if not name:
        flash('Ime ne sme biti prazno', 'danger')
        return redirect(url_for('nastavitve', tab='subcategory'))

    if SubCategory.query.filter_by(name=name).first():
        flash('Podkategorija s tem imenom že obstaja', 'danger')
        return redirect(url_for('nastavitve', tab='subcategory'))

    sub = SubCategory(name=name)
    db.session.add(sub)
    db.session.commit()

    flash('Podkategorija dodana', 'success')
    return redirect(url_for('nastavitve', tab='subcategory'))

@app.route('/nastavitve/edit_subcategory/<int:id>', methods=['POST'])
def edit_subcategory(id):
    sub = SubCategory.query.get_or_404(id)
    name = request.form.get('name', '').strip()

    if not name:
        flash('Ime ne sme biti prazno', 'danger')
        return redirect(url_for('nastavitve', tab='subcategory'))

    exists = SubCategory.query.filter(
        SubCategory.name == name,
        SubCategory.id != id
    ).first()

    if exists:
        flash('Podkategorija s tem imenom že obstaja', 'danger')
        return redirect(url_for('nastavitve', tab='subcategory'))

    sub.name = name
    db.session.commit()

    flash('Podkategorija posodobljena', 'success')
    return redirect(url_for('nastavitve', tab='subcategory'))

@app.route('/nastavitve/delete_subcategory/<int:id>', methods=['POST'])
def delete_subcategory(id):
    sub = SubCategory.query.get_or_404(id)
    db.session.delete(sub)
    db.session.commit()

    flash('Podkategorija izbrisana', 'success')
    return redirect(url_for('nastavitve', tab='subcategory'))

@app.route('/nastavitve/new_competition_subtype', methods=['POST'])
def new_competition_subtype():
    name = request.form.get('name').strip()
    competition_type_id = request.form.get('competition_type_id')
    arrows = request.form.get('arrows')

    # zaščita pred duplikati (ime + disciplina)
    exists = CompetitionSubType.query.filter_by(
        name=name,
        competition_type_id=competition_type_id
    ).first()

    if exists:
        flash("Podtip za izbrano disciplino že obstaja.", "danger")
        return redirect(url_for('nastavitve', tab='competition_subtype'))

    item = CompetitionSubType(
        name=name,
        competition_type_id=competition_type_id,
        arrows=arrows if arrows else None
    )

    db.session.add(item)
    db.session.commit()

    flash("Podtip tekmovanja dodan.", "success")
    return redirect(url_for('nastavitve', tab='competition_subtype'))

@app.route('/nastavitve/edit_competition_subtype/<int:id>', methods=['POST'])
def edit_competition_subtype(id):
    item = CompetitionSubType.query.get_or_404(id)

    name = request.form.get('name').strip()
    competition_type_id = request.form.get('competition_type_id')
    arrows = request.form.get('arrows')

    # duplicate check (izjema: sam sebe)
    exists = CompetitionSubType.query.filter(
        CompetitionSubType.id != id,
        CompetitionSubType.name == name,
        CompetitionSubType.competition_type_id == competition_type_id
    ).first()

    if exists:
        flash("Podtip za izbrano disciplino že obstaja.", "danger")
        return redirect(url_for('nastavitve', tab='competition_subtype'))

    item.name = name
    item.competition_type_id = competition_type_id
    item.arrows = arrows if arrows else None

    db.session.commit()

    flash("Podtip tekmovanja posodobljen.", "success")
    return redirect(url_for('nastavitve', tab='competition_subtype'))


@app.route('/nastavitve/delete_competition_subtype/<int:id>', methods=['POST'])
def delete_competition_subtype(id):
    item = CompetitionSubType.query.get_or_404(id)

    db.session.delete(item)
    db.session.commit()

    flash("Podtip tekmovanja izbrisan.", "success")
    return redirect(url_for('nastavitve', tab='competition_subtype'))


@app.route('/o_programu')
def o_programu():
    return render_template('o_programu.html')


if __name__ == '__main__':
    app.run(debug=True)
