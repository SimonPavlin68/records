# test_records_by_date.py
from app import app
from models import db, Record
from datetime import datetime

with app.app_context():
    # Limitni datum
    date_limit = datetime(2025, 1, 1).date()

    # Query
    records = Record.query.filter(Record.date < date_limit).order_by(Record.date.desc()).all()

    print(f"Število rekordov mlajših od {date_limit}: {len(records)}\n")

    # Izpiši prvih 10 za test
    for r in records[:10]:
        print(
            f"{r.id}: {r.competitor_name} | {r.result} | "
            f"{r.competition_type.name} | {r.competition_subtype.name if r.competition_subtype else '-'} | {r.date}"
        )
