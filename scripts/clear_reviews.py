# run this script to clear all reviews and votes from the database
from app import db, create_app
from app.models import Review, Vote

app = create_app()
with app.app_context():
    Vote.query.delete()
    Review.query.delete()
    db.session.commit()
    print("All reviews and votes deleted")