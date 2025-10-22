import os

# Find the absolute path of the directory this file is in
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration class."""
    # Secret key is crucial for sessions and security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-super-secret-default-key'

    # --- Database Configuration ---
    # Use an environment variable for the database URL, or default to a
    # local SQLite file named 'app.db' in the base directory.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')

    # Disable a Flask-SQLAlchemy feature we don't need
    SQLALCHEMY_TRACK_MODIFICATIONS = False