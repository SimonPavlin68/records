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
    # vzame vse CompetitionType zapise
    # items = CompetitionType.query.order_by(CompetitionType.name).all()
    items = CompetitionType.query.order_by(CompetitionType.id).all()
    return render_template('nastavitve.html', items=items)


@app.route('/nastavitve/add', methods=['POST'])
def add_competition_type():
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
    return redirect(url_for('nastavitve'))


@app.route('/o_programu')
def o_programu():
    return render_template('o_programu.html')


if __name__ == '__main__':
    app.run(debug=True)
