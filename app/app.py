# Add jsonify to your imports from flask
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a-default-fallback-key-for-development')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create dictionary of users
# TODO: connect to sqlite database that the program runs.


users = {}


class User(UserMixin):
    def __init__(self, userid, password):
        self.id = userid
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Default user TODO: REMOVE
users['admin'] = User('admin', 'password123')


@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)


# --- Routes ---

@app.route('/')
@login_required
def home():
    return render_template('dashboard.html', username=current_user.id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # ... (login function is unchanged)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users.get(username)

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/take-picture', methods=['POST'])
@login_required
def take_picture():
    """
    This is an API endpoint. It doesn't return an HTML page.
    It performs an action and returns a JSON status response.
    """
    print("Received request to take a picture!")

    # TODO: Code to take picture from USB camera

    # Return a JSON response to the JavaScript on the frontend
    return jsonify({'status': 'success', 'message': 'Picture taken successfully!'})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)