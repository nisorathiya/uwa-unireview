# seed.py

from app import create_app, db
from app.models import Unit

UNITS = [
    # ── Engineering & Computing ───────────────────────────────────────
    ("CITS1001", "Software Engineering with Java",          "engineering", 6),
    ("CITS1401", "Computational Thinking with Python",      "engineering", 6),
    ("CITS2005", "Object Oriented Programming",             "engineering", 6),
    ("CITS2200", "Data Structures and Algorithms",          "engineering", 6),
    ("CITS3001", "Advanced Algorithms", "Engineering & Computing", 6),
    ("CITS3003", "Graphics and Animation",                  "engineering", 6),
    ("CITS3200", "Professional Computing",                  "engineering", 6),
    ("CITS3403", "Agile Web Development",                   "engineering", 6),
    ("CITS3007", "Secure Coding",                           "engineering", 6),
    ("CITS4009", "Fundamentals of Data Science",            "engineering", 6),
    ("CITS5505", "Agile Web Development (Postgrad)",        "engineering", 6),
    ("ENSC3020", "Digital Embedded Systems",                "engineering", 6),

    # ── Science ──────────────────────────────────────────────────────
    ("MATH1011", "Multivariable Calculus",                  "Science", 6),
    ("MATH1012", "Mathematical Theory and Methods",         "Science", 6),
    ("MATH1013", "Mathematical Analysis ",                  "Science", 6),
    ("STAT1400", "Statistics for Science",                  "Science", 6),
    ("STAT2401", "Analysis of Experiments",                 "Science", 6),
    ("BIOL1130", "Frontiers in Biology",                    "Science", 6),
    ("CHEM1002", "Chemistry—Structure and Reactivity",      "Science", 6),
    ("PHYS1001", "Physics for Scientists and Engineers",    "Science", 6),
    ("PSYC1101", "Mind and Brain",                          "Science", 6),

    # ── Business ─────────────────────────────────────────────────────
    ("ACCT1101", "Financial Accounting",                    "Business", 6),
    ("ECON1101", "Microeconomics: Prices and Markets",      "Business", 6),
    ("ECON1102", "Macroeconomics: Money and Finance",       "Business", 6),

    # ── Law ──────────────────────────────────────────────────────────
    ("LAWS1104", "Introduction to Law",                      "Law", 6),
    ("LAWS1110", "Crime and Society",                        "Law", 6),
    ("LAWS1111", "Law in Context",                           "Law", 6),
    ("LAWS1112", "Law for Everyday Lives",                   "Law", 6),

    # ── Arts ─────────────────────────────────────────────────────────
    ("ENGL1000", "Global Literatures",                       "Arts", 6),
    ("HIST1104", "The History of Human Rights",              "Arts", 6),
    ("PHIL1002", "Introduction to Critical Thinking",        "Arts", 6),
    ("POLS1101", "Understanding Politics and Policy",        "Arts", 6),
]

def seed():
    app = create_app()
    with app.app_context():
        db.create_all()
        print(f"Seeding database with {len(UNITS)} units...\n") 

        added   = 0
        skipped = 0

        for code, name, faculty, credits in UNITS:
            if Unit.query.filter_by(code=code).first():
                print(f"  SKIP  {code} — already exists")
                skipped += 1
            else:
                db.session.add(Unit(code=code, name=name, faculty=faculty, credit_points=credits))
                print(f"  ADD   {code} — {name}")
                added += 1

        db.session.commit()
        print(f"\nDone. {added} units added, {skipped} skipped.")


if __name__ == '__main__':
    seed()