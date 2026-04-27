import os

class Config:
    # Secret key for CSRF protection and session management
    # In production this should be stored as an environment variable, not hardcoded
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'uwa-unireview-dev-key-change-in-production'

    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///unireview.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Database will be configured here in a later sprint
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///unireview.db'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
