from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db      = SQLAlchemy()
migrate = Migrate()

# Initialise extensions (without binding to an app yet)
csrf = CSRFProtect()

def create_app(config_class=Config):
    """
    Application factory function.
    Creates and configures the Flask app instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize database and migration extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    # Initialise extensions with the app
    csrf.init_app(app)

    # Register routes blueprint
    from app.routes import main
    app.register_blueprint(main)

    from app import models
    
    return app
