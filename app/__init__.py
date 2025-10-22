from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# 1. Initialize extensions (but don't connect them to an app yet)
db = SQLAlchemy()
login = LoginManager()

# 2. Tell the login manager where to find the login page
# 'main.login' means the 'login' function inside the 'main' blueprint
login.login_view = 'main.login'
login.login_message = 'Please log in to access this page.'
login.login_message_category = 'info'


def create_app(config_class=Config):
    """The application factory function."""
    app = Flask(__name__)

    # 3. Load the configuration from our config.py file
    app.config.from_object(config_class)

    # 4. Connect the extensions to the app instance
    db.init_app(app)
    login.init_app(app)

    # 5. Register our "main" blueprint
    # We import here to avoid circular dependencies
    from app.routes import bp as main_blueprint
    app.register_blueprint(main_blueprint)

    # 6. Create the database tables if they don't already exist
    # We use app.app_context() to make sure we're in the right
    # context for the database operations.
    with app.app_context():
        # Import models here so create_all knows about them
        from app import models
        db.create_all()

    return app