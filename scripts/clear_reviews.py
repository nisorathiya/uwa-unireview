"""
Dev utility script — wipes all reviews and votes from the database.
Used during development for testing fresh-state scenarios.
NOT for production use.

Run: python3 scripts/clear_reviews.py
"""
from app import db, create_app
from app.models import Review, Vote

app = create_app()
with app.app_context():
    Vote.query.delete()
    Review.query.delete()
    db.session.commit()
    print("All reviews and votes deleted")