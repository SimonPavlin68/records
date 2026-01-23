from flask import Flask, render_template, request, flash, redirect, url_for
from models import db, CompetitionType, Style, Gender, Category, SubCategory

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

@app.route('/rekordi')
def rekordi():
    return render_template('rekordi.html')


@app.route('/nastavitve')
def nastavitve():
    # Query iz baze
    competition_items = CompetitionType.query.order_by(CompetitionType.id).all()
    style_items = Style.query.order_by(Style.id).all()

    return render_template(
        'nastavitve.html',
        competition_items=competition_items,
        style_items=style_items
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


@app.route('/o_programu')
def o_programu():
    return render_template('o_programu.html')


if __name__ == '__main__':
    app.run(debug=True)
