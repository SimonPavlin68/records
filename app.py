from flask import Flask, render_template, request, redirect, url_for
from models import db, Record
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()  # ustvari bazo, če še ne obstaja


@app.route('/', methods=['GET'])
def index():
    # pobrati filtre iz GET parametrov
    filters = {
        'type': request.args.get('type'),
        'style': request.args.get('style'),
        'category': request.args.get('category'),
        'archer': request.args.get('archer'),
        'club': request.args.get('club'),
        'date': request.args.get('date')
    }

    query = Record.query

    if filters['type']:
        query = query.filter(Record.type.ilike(f"%{filters['type']}%"))
    if filters['style']:
        query = query.filter(Record.style.ilike(f"%{filters['style']}%"))
    if filters['category']:
        query = query.filter(Record.category.ilike(f"%{filters['category']}%"))
    if filters['archer']:
        query = query.filter(Record.archer.ilike(f"%{filters['archer']}%"))
    if filters['club']:
        query = query.filter(Record.club.ilike(f"%{filters['club']}%"))
    if filters['date']:
        query = query.filter(Record.date == filters['date'])

    records = query.order_by(Record.date.desc()).all()

    return render_template('index.html', records=records, filters=filters)


# --- Vnos novega rekorda ---
@app.route('/add', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        record = Record(
            type=request.form['type'],  # 🆕
            bow_type=request.form['bow_type'],
            participants=request.form['participants'],
            individual_or_team=request.form['individual_or_team'],
            round_type=request.form['round_type'],
            score=int(request.form['score']),
            archer=request.form['archer'],
            club=request.form['club'],
            location=request.form['location'],
            date=datetime.strptime(request.form['date'], '%Y-%m-%d'),
            record_type=request.form['record_type']
        )
        db.session.add(record)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')


if __name__ == '__main__':
    app.run(debug=True)
