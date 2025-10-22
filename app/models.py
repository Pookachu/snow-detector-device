# /snow-detector-device/app/models.py
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# This function is required by Flask-Login to load a user from the session
@login.user_loader
def load_user(user_id):
    """Flask-Login callback to load a user from an ID."""
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    """Database model for a user account."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        """Creates a secure hash for a new password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks a submitted password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'