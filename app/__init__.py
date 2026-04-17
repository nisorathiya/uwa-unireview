from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import Config

# Initialise extensions (without binding to an app yet)
csrf = CSRFProtect()

def create_app(config_class=Config):
    """
    Application factory function.
    Creates and configures the Flask app instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialise extensions with the app
    csrf.init_app(app)

    # Register routes blueprint
    from app.routes import main
    app.register_blueprint(main)

    return app
