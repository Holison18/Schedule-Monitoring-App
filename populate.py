from app import create_app, db
from app.models import Pair, School
import pandas as pd

# Load your Excel file
file_path = "Assets/june.xlsx"
df = pd.read_excel(file_path)

# Strip whitespace and fill NaNs just in case
df.fillna('', inplace=True)

# Initialize Flask app context
app = create_app()

with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Tables created.")

    print("Adding monitoring pairs...")

    # Track already created pairs to avoid duplicates
    pair_map = {}

    for _, row in df.iterrows():
        pair_name = row["Monitors"]
        email1 = row["Email 1"]
        email2 = row["Email 2"]

        # Avoid duplicate pair insertion
        if pair_name not in pair_map:
            pair = Pair(
                pair_name=pair_name,
                user1_email=email1.lower().strip(),
                user2_email=email2.lower().strip()
            )
            db.session.add(pair)
            pair_map[pair_name] = pair  # Store for reuse
        else:
            pair = pair_map[pair_name]

    print("Committing pairs...")
    db.session.commit()

    print("Adding schools...")

    for _, row in df.iterrows():
        pair = pair_map[row["Monitors"]]
        school = School(
            school_name=row["School"],
            region=row["Region"],
            district=row["District"],
            location=row["Location"],
            school_code=str(int(row["Code"])) if row["Code"] else "N/A",
            head_teacher_name=row["Headmaster"],
            head_teacher_contact=str(row["Headmaster contact"]).replace("`", "").strip(),
            assigned_pair=pair
        )
        db.session.add(school)

    db.session.commit()
    print("✅ All data has been successfully saved to the database!")
    exit()
