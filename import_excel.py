import pandas as pd
from app import app, db
from models import Record


def import_from_excel(file_path):
    # Excel nima headerja
    df = pd.read_excel(
        file_path,
        header=None,
        names=[
            "type", "style", "category", "individual_or_team", "details",
            "arrows", "score", "archer", "club", "location", "date", "record_type"
        ]
    )

    print(f"Prebranih vrstic: {len(df)}")

    for _, row in df.iterrows():
        # pretvorba datuma
        try:
            date_val = pd.to_datetime(row["date"], errors="coerce").date()
        except Exception:
            date_val = None

        record = Record(
            type=row["type"],
            style=row["style"],
            category=row["category"],
            individual_or_team=row["individual_or_team"],
            details=row["details"],
            arrows=int(row["arrows"]) if not pd.isna(row["arrows"]) else None,
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

