import random
from app import create_app, db
from app.models import User, Unit, Review
from werkzeug.security import generate_password_hash

app = create_app()

DUMMY_USERS = [
    ("james_wu",      "james.wu@student.uwa.edu.au"),
    ("sarah_miller",  "sarah.miller@student.uwa.edu.au"),
    ("liam_chen",     "liam.chen@student.uwa.edu.au"),
    ("olivia_patel",  "olivia.patel@student.uwa.edu.au"),
    ("noah_kim",      "noah.kim@student.uwa.edu.au"),
    ("emma_jones",    "emma.jones@student.uwa.edu.au"),
    ("ethan_nguyen",  "ethan.nguyen@student.uwa.edu.au"),
    ("ava_smith",     "ava.smith@student.uwa.edu.au"),
    ("mason_brown",   "mason.brown@student.uwa.edu.au"),
    ("isabella_lee",  "isabella.lee@student.uwa.edu.au"),
    ("lucas_taylor",  "lucas.taylor@student.uwa.edu.au"),
    ("mia_wilson",    "mia.wilson@student.uwa.edu.au"),
    ("aiden_davis",   "aiden.davis@student.uwa.edu.au"),
    ("charlotte_anderson", "charlotte.anderson@student.uwa.edu.au"),
    ("oliver_thomas", "oliver.thomas@student.uwa.edu.au"),
]

COMMENTS = [
    "Really enjoyed this unit. The content was well structured and the assignments were challenging but fair.",
    "Heavy workload but very rewarding. Learned a lot of practical skills I can use in industry.",
    "The lectures were a bit dry but the labs made up for it. Worth taking if you are interested in the field.",
    "Reasonable unit overall. The final project was the best part — gave us real hands-on experience.",
    "Tough unit but the lecturers are supportive. Make sure you start assignments early.",
    "One of the better units I have taken at UWA. Very applicable to real world problems.",
    "Content was interesting but the assessments felt disconnected from what was taught in lectures.",
    "Great unit for building foundational knowledge. Would recommend to anyone in the program.",
    "Workload was manageable if you keep up with the weekly content. Do not fall behind.",
    "Decent unit. The group project was stressful but taught me a lot about working in a team.",
    "Lectures were well delivered and the tutor was very helpful during labs.",
    "Harder than expected but I came out of it with a much better understanding of the subject.",
    "Average unit. Nothing groundbreaking but covers the basics well.",
    "Loved the practical components. The theory was dense but necessary.",
    "Would have liked more feedback on assignments. Overall a solid unit though.",
]

with app.app_context():
    # Create dummy users if they don't exist
    created_users = []
    for username, email in DUMMY_USERS:
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash("Password123!")
            )
            db.session.add(user)
            db.session.flush()
        created_users.append(user)

    db.session.commit()
    print(f"Users ready: {len(created_users)}")

    # Seed reviews for each unit
    units = Unit.query.all()
    total = 0

    for unit in units:
        # Shuffle users so each unit gets a different mix
        random.shuffle(created_users)
        num_reviews = random.randint(10, 15)
        users_for_unit = created_users[:num_reviews]

        for user in users_for_unit:
            # Skip if this user already reviewed this unit
            existing = Review.query.filter_by(
                user_id=user.id, unit_id=unit.id
            ).first()
            if existing:
                continue

            review = Review(
                user_id           = user.id,
                unit_id           = unit.id,
                overall_rating    = random.randint(2, 5),
                workload_rating   = random.randint(1, 5),
                difficulty_rating = random.randint(1, 5),
                usefulness_rating = random.randint(2, 5),
                comment           = random.choice(COMMENTS),
                year_taken        = random.choice([2022, 2023, 2024]),
                semester          = random.choice(["S1", "S2"])
            )
            db.session.add(review)
            total += 1

    db.session.commit()
    print(f"Done. {total} reviews seeded across {len(units)} units.")