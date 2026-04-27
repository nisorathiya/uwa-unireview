# ─────────────────────────────────────────────────────────────
# models.py
# Database models for UWA UniReview.

from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer,     primary_key=True)
    username      = db.Column(db.String(80),  nullable=False)
    email         = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at    = db.Column(db.DateTime,    default=datetime.utcnow)

    reviews     = db.relationship('Review',    backref='author', lazy=True)
    votes       = db.relationship('Vote',      backref='user',   lazy=True)
    saved_units = db.relationship('SavedUnit', backref='user',   lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'


class Unit(db.Model):
    __tablename__ = 'units'

    id            = db.Column(db.Integer,      primary_key=True)
    code          = db.Column(db.String(10),   nullable=False, unique=True)
    name          = db.Column(db.String(150),  nullable=False)
    faculty       = db.Column(db.String(100))
    credit_points = db.Column(db.Integer,      default=6)

    reviews  = db.relationship('Review',    backref='unit', lazy=True)
    saved_by = db.relationship('SavedUnit', backref='unit', lazy=True)

    def __repr__(self):
        return f'<Unit {self.code}>'


class Review(db.Model):
    __tablename__ = 'reviews'

    id                = db.Column(db.Integer,    primary_key=True)
    user_id           = db.Column(db.Integer,    db.ForeignKey('users.id'), nullable=False)
    unit_id           = db.Column(db.Integer,    db.ForeignKey('units.id'), nullable=False)
    overall_rating    = db.Column(db.Integer,    nullable=False)   # 1–5
    workload_rating   = db.Column(db.Integer,    nullable=False)   # 1–5
    difficulty_rating = db.Column(db.Integer,    nullable=False)   # 1–5
    usefulness_rating = db.Column(db.Integer,    nullable=False)   # 1–5
    comment           = db.Column(db.Text,       nullable=False)
    year_taken        = db.Column(db.Integer)
    semester          = db.Column(db.String(2))  # S1 or S2
    created_at        = db.Column(db.DateTime,   default=datetime.utcnow)

    votes = db.relationship('Vote', backref='review', lazy=True)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'unit_id', name='unique_review'),
    )

    def __repr__(self):
        return f'<Review {self.id} by User {self.user_id}>'


class Vote(db.Model):
    __tablename__ = 'votes'

    id        = db.Column(db.Integer, primary_key=True)
    user_id   = db.Column(db.Integer, db.ForeignKey('users.id'),   nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False)
    value     = db.Column(db.Integer, nullable=False)   # +1 or -1

    __table_args__ = (
        db.UniqueConstraint('user_id', 'review_id', name='unique_vote'),
    )

    def __repr__(self):
        return f'<Vote {self.value} by User {self.user_id}>'


class SavedUnit(db.Model):
    __tablename__ = 'saved_units'

    id      = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'unit_id', name='unique_saved'),
    )

    def __repr__(self):
        return f'<SavedUnit User {self.user_id} Unit {self.unit_id}>'