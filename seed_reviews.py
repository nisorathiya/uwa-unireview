"""Seed the database with dummy users and reviews for development/testing."""

import random
from app import create_app, db
from app.models import User, Unit, Review
from werkzeug.security import generate_password_hash

app = create_app()

# ---------------------------------------------------------------------------
# Dev-only fixture data. Do NOT run this in production.
# Default password is intentionally weak for local testing only.
# ---------------------------------------------------------------------------
DEV_PASSWORD = "Password123!"

DUMMY_USERS = [
    ("james_wu",            "james.wu@student.uwa.edu.au"),
    ("sarah_miller",        "sarah.miller@student.uwa.edu.au"),
    ("liam_chen",           "liam.chen@student.uwa.edu.au"),
    ("olivia_patel",        "olivia.patel@student.uwa.edu.au"),
    ("noah_kim",            "noah.kim@student.uwa.edu.au"),
    ("emma_jones",          "emma.jones@student.uwa.edu.au"),
    ("ethan_nguyen",        "ethan.nguyen@student.uwa.edu.au"),
    ("ava_smith",           "ava.smith@student.uwa.edu.au"),
    ("mason_brown",         "mason.brown@student.uwa.edu.au"),
    ("isabella_lee",        "isabella.lee@student.uwa.edu.au"),
    ("lucas_taylor",        "lucas.taylor@student.uwa.edu.au"),
    ("mia_wilson",          "mia.wilson@student.uwa.edu.au"),
    ("aiden_davis",         "aiden.davis@student.uwa.edu.au"),
    ("charlotte_anderson",  "charlotte.anderson@student.uwa.edu.au"),
    ("oliver_thomas",       "oliver.thomas@student.uwa.edu.au"),
]

# ---------------------------------------------------------------------------
# Comments are grouped by sentiment bucket so they match the overall rating.
# Each list also includes some faculty-flavoured variants to reduce repetition.
# ---------------------------------------------------------------------------

POSITIVE_COMMENTS = {
    "general": [
        "One of the best units I've taken at UWA. Content was well structured and the assessments felt fair.",
        "Genuinely enjoyed this. The lecturer was engaging and the workload was manageable if you stayed on top of it.",
        "Highly recommend. Clear learning objectives and the teaching team actually cared about student feedback.",
        "Solid unit. Came out of it with skills I'm already using and a much better grasp of the field.",
        "Really well run unit. Tutorials reinforced the lectures and the final assessment tied everything together nicely.",
    ],
    "Engineering & Computing": [
        "The labs were the highlight — proper hands-on work and the tutors knew their stuff. Project was challenging but doable.",
        "Loved this unit. The coding assignments were tough but the feedback loop on submissions was fast and useful.",
        "Great mix of theory and practical. The group project taught me more about real software development than any other unit.",
    ],
    "Science": [
        "Lab sessions were well organised and the prac reports were marked thoroughly. Lecturer clearly knew the material inside out.",
        "Content was dense but the lecturer broke it down well. The practicals reinforced everything from the lectures.",
    ],
    "Business": [
        "Case studies were genuinely interesting and the group work felt purposeful rather than busywork.",
        "Good unit. Guest lectures from industry were a highlight and the assignments mirrored real business problems.",
    ],
    "Law": [
        "Demanding but rewarding. The tutorials forced you to actually engage with the cases, which I appreciated.",
        "Lecturer was excellent. Built up the doctrine logically and the final exam was a fair test of understanding.",
    ],
    "Arts": [
        "Thought-provoking unit with great reading materials. Tutorials had real discussion rather than just box-ticking.",
        "Enjoyed the essay topics — they gave you genuine room to develop your own argument.",
    ],
}

NEUTRAL_COMMENTS = {
    "general": [
        "Decent unit overall. Covers the basics well but nothing groundbreaking.",
        "Average experience. Lectures were a bit dry but the content itself was useful.",
        "Workload was reasonable. Some assessments felt disconnected from the lecture content though.",
        "Fine unit. Did the job but I wouldn't go out of my way to recommend it.",
        "Mixed feelings. The content is important but the delivery could be improved.",
    ],
    "Engineering & Computing": [
        "Coding assignments were okay but the specs were vague. Had to clarify a lot on the forum.",
        "Lectures didn't always match up with what was needed for the labs. Manageable if you read ahead.",
    ],
    "Science": [
        "Pracs were hit and miss. Some were great, others felt like we were just following a recipe.",
    ],
    "Business": [
        "Group work was a mixed bag depending on who you got. Content itself was reasonable.",
    ],
    "Law": [
        "Heavy reading load but the doctrine isn't too bad once you sit with it. Tutorials varied by tutor.",
    ],
    "Arts": [
        "Essay-heavy. If you like writing you'll be fine, otherwise it can feel like a slog.",
    ],
}

NEGATIVE_COMMENTS = {
    "general": [
        "Disappointing. Assessments felt unfair and feedback was minimal. Would not take again if I had the choice.",
        "Struggled with this one. Workload was heavy for the credit point value and the support wasn't great.",
        "Content was interesting in theory but the unit was poorly organised. Deadlines kept shifting.",
        "Tough unit and not in a rewarding way. Lectures often went off-topic from what was actually assessed.",
    ],
    "Engineering & Computing": [
        "Assignment briefs were unclear and marking felt inconsistent. The content has potential but the delivery let it down.",
    ],
    "Science": [
        "Practicals were rushed and the marking criteria for reports kept changing. Content itself is okay.",
    ],
    "Business": [
        "Felt like busywork. The group project was a nightmare and the content didn't justify the workload.",
    ],
    "Law": [
        "Reading load was unreasonable and the exam didn't really reflect what was emphasised in tutorials.",
    ],
    "Arts": [
        "Essay feedback was thin and the marking felt arbitrary. Hard to know how to improve.",
    ],
}


def pick_comment(overall_rating, faculty):
    """Pick a comment that matches the sentiment and (sometimes) the faculty."""
    if overall_rating >= 4:
        bucket = POSITIVE_COMMENTS
    elif overall_rating == 3:
        bucket = NEUTRAL_COMMENTS
    else:
        bucket = NEGATIVE_COMMENTS

    # 60% chance of faculty-flavoured comment if available, else general
    if faculty in bucket and random.random() < 0.6:
        return random.choice(bucket[faculty])
    return random.choice(bucket["general"])


def correlated_ratings():
    """
    Generate a 4-tuple (overall, workload, difficulty, usefulness) where the
    sub-ratings correlate sensibly with the overall rating, with realistic noise.

    Distribution of `overall` is biased positive — real review sites cluster
    around 3.5-4.0 rather than being uniform.
    """
    # Biased positive: weights favour 3-5
    overall = random.choices(
        population=[1, 2, 3, 4, 5],
        weights=[2, 6, 18, 40, 34],
        k=1,
    )[0]

    # Usefulness tracks overall fairly closely (+/- 1)
    usefulness = max(1, min(5, overall + random.choice([-1, 0, 0, 0, 1])))

    # Workload and difficulty are weakly correlated with overall —
    # a hard unit can still be loved, so we add more noise here.
    # Tendency: lower-rated units skew toward higher workload/difficulty.
    base = 6 - overall  # invert: overall=5 -> base=1, overall=1 -> base=5
    workload = max(1, min(5, base + random.choice([-1, 0, 0, 1, 1])))
    difficulty = max(1, min(5, base + random.choice([-1, -1, 0, 0, 1])))

    return overall, workload, difficulty, usefulness


def get_faculty(unit):
    """Best-effort faculty lookup. Falls back to 'general' if the field doesn't exist."""
    for attr in ("faculty", "school", "department"):
        value = getattr(unit, attr, None)
        if value:
            return value
    return "general"


with app.app_context():
    # -----------------------------------------------------------------------
    # 1. Ensure dummy users exist
    # -----------------------------------------------------------------------
    created_users = []
    for username, email in DUMMY_USERS:
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(DEV_PASSWORD),
            )
            db.session.add(user)
            db.session.flush()
        created_users.append(user)

    db.session.commit()
    print(f"Users ready: {len(created_users)}")

    # -----------------------------------------------------------------------
    # 2. Seed reviews
    # -----------------------------------------------------------------------
    units = Unit.query.all()
    total_added = 0
    total_skipped = 0

    for unit in units:
        faculty = get_faculty(unit)

        # Shuffle for variety, but cap by how many users are actually free
        # for this unit (haven't reviewed it yet).
        random.shuffle(created_users)
        target_review_count = random.randint(10, 15)

        added_for_this_unit = 0
        for user in created_users:
            if added_for_this_unit >= target_review_count:
                break

            existing = Review.query.filter_by(
                user_id=user.id, unit_id=unit.id
            ).first()
            if existing:
                total_skipped += 1
                continue

            overall, workload, difficulty, usefulness = correlated_ratings()
            comment = pick_comment(overall, faculty)

            review = Review(
                user_id           = user.id,
                unit_id           = unit.id,
                overall_rating    = overall,
                workload_rating   = workload,
                difficulty_rating = difficulty,
                usefulness_rating = usefulness,
                comment           = comment,
                year_taken        = random.choices(
                    population=[2022, 2023, 2024, 2025],
                    weights=[1, 2, 4, 4],  # bias toward recent years
                    k=1,
                )[0],
                semester          = random.choice(["S1", "S2"]),
            )

            # Seed helpful_votes if the field exists on the model.
            # Most reviews get 0-2, a few are "top reviews" with more.
            if hasattr(Review, "helpful_votes"):
                review.helpful_votes = random.choices(
                    population=[0, 1, 2, 3, 5, 8, 12],
                    weights=[30, 25, 15, 10, 10, 7, 3],
                    k=1,
                )[0]

            db.session.add(review)
            added_for_this_unit += 1
            total_added += 1

    db.session.commit()
    print(f"Done. {total_added} reviews seeded across {len(units)} units "
          f"({total_skipped} skipped as duplicates).")