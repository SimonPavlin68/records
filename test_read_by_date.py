import datetime
from app import app
from models import db, Record

# datum meje
date_limit = datetime.date(2025, 1, 1)

with app.app_context():
    # poizvedba: vse rekorde, kjer je datum > 1.1.2025
    records = Record.query.filter(Record.date > date_limit).order_by(Record.date).all()

    print(f"Število rekordov mlajših od {date_limit}: {len(records)}\n")

    # izpišemo prvih 20 za kontrolo
    for r in records[:100]:
        print(f"{r.id}: {r.competitor_name} | {r.result} | {r.location or '-'} | "
              f"{r.competition_subtype.name if r.competition_subtype else '-'} | {r.date}")
