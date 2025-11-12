import pandas as pd
from datetime import datetime
from app import app, db
from models import Record

def import_from_excel(file_path):
    # 📘 če tvoj Excel nima glave (header row)
    df = pd.read_excel(
        file_path,
        header=None,
        names=[
            "target", "bow_type", "participants", "individual_or_team", "round_type",
            "series", "score", "archer", "club", "location", "date", "record_type"
        ]
    )

    print(f"Prebranih vrstic: {len(df)}")

    for _, row in df.iterrows():
        try:
            date_val = pd.to_datetime(row["date"], errors="coerce")
        except Exception:
            date_val = None

        record = Record(
            target=row["target"],
            bow_type=row["bow_type"],
            participants=row["participants"],
            individual_or_team=row["individual_or_team"],
            round_type=row["round_type"],
            score=int(row["score"]) if not pd.isna(row["score"]) else None,
            archer=row["archer"],
            club=row["club"],
            location=row["location"],
            date=date_val,
            record_type=row["record_type"]
        )
        db.session.add(record)

    db.session.commit()
    print(f"✅ Uvoženih {len(df)} zapisov v bazo.")

if __name__ == "__main__":
    with app.app_context():
        import_from_excel("Rekordi_od_1.01.1989_do_11_11_2025.xls")

