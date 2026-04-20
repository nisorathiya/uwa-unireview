# ─────────────────────────────────────────────────────────────
# models.py
# Database models for UWA UniReview.

# from app import db  # uncomment when database is setup


class User:
    """
    Represents a registered student.

    Fields (to be implemented with SQLAlchemy):
        id            - primary key
        username      - display name
        email         - must end in @student.uwa.edu.au
        password_hash - bcrypt hash, never plain text
        created_at    - timestamp of registration
    """
    pass


class Unit:
    """
    Represents a UWA unit.

    Fields (to be implemented with SQLAlchemy):
        id            - primary key
        code          - e.g. CITS3403
        name          - full unit name
        faculty       - e.g. Engineering & Computing
        credit_points - 6 or 12
    """
    pass


class Review:
    """
    Represents a student review of a unit.

    Fields (to be implemented with SQLAlchemy):
        id                - primary key
        user_id           - FK → User
        unit_id           - FK → Unit
        overall_rating    - 1 to 5
        workload_rating   - 1 to 5
        difficulty_rating - 1 to 5
        usefulness_rating - 1 to 5
        comment           - free text
        year_taken        - e.g. 2024
        semester          - S1 or S2
        created_at        - timestamp
    Constraints:
        unique(user_id, unit_id) — one review per student per unit
    """
    pass


class Vote:
    """
    Represents an upvote on a review.

    Fields (to be implemented with SQLAlchemy):
        id        - primary key
        user_id   - FK → User
        review_id - FK → Review
        value     - +1 or -1
    Constraints:
        unique(user_id, review_id) — one vote per student per review
    """
    pass


class SavedUnit:
    """
    Represents a unit saved to a student's watchlist.

    Fields (to be implemented with SQLAlchemy):
        id      - primary key
        user_id - FK → User
        unit_id - FK → Unit
    Constraints:
        unique(user_id, unit_id)
    """
    pass
