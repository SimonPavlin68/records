from flask import Flask, render_template, request, redirect, url_for
from models import db, Record
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()  # ustvari bazo, če še ne obstaja


# --- Prikaz vseh rekordov ---
@app.route('/', methods=['GET'])
def index():
    filters = {
        'bow_type': request.args.get('bow_type'),
        'club': request.args.get('club'),
        'record_type': request.args.get('record_type')
    }

    query = Record.query
    if filters['bow_type']:
        query = query.filter_by(bow_type=filters['bow_type'])
    if filters['club']:
        query = query.filter_by(club=filters['club'])
    if filters['record_type']:
        query = query.filter_by(record_type=filters['record_type'])

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
