from flask import (
    Blueprint, render_template, flash,
    redirect, url_for, request, jsonify, current_app
)
from app import db
from app.models import User
from flask_login import login_user, logout_user, current_user, login_required
import os
from datetime import datetime

from app.hardware import camera

# 1. Create the Blueprint
bp = Blueprint('main', __name__)


# 2. Define the routes
@bp.route('/')
@bp.route('/dashboard')
@login_required  # This route is now protected
def dashboard():
    """The main dashboard page, shown after login."""
    return render_template('dashboard.html', title='Dashboard')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """The login page."""
    # If user is already logged in, send them to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Find the user in the database
        user = User.query.filter_by(username=username).first()

        # Check if user exists and the password is correct
        if user is None or not user.check_password(password):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('main.login'))

        # Log the user in and send them to the dashboards
        login_user(user, remember=True)
        return redirect(url_for('main.dashboard'))

    # For a GET request, just show the login page
    return render_template('login.html', title='Sign In')


@bp.route('/logout')
def logout():
    """Logs the user out."""
    logout_user()
    return redirect(url_for('main.login'))


# --- NEW MODIFIED API ENDPOINT ---
@bp.route('/take-picture', methods=['POST'])
@login_required
def take_picture():
    """
    API endpoint to trigger the camera.
    """
    try:
        # 1. Generate a unique filename with a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{timestamp}.jpg"

        # 2. Create the full file path
        # current_app.root_path is the 'app' folder
        save_path = os.path.join(
            current_app.root_path, 'static', 'uploads', filename
        )

        # 3. Call the camera module to capture the image
        success = camera.capture_frame(save_path)

        if success:
            # 4. Create a web-accessible URL for the image
            image_url = url_for('static', filename=f'uploads/{filename}')
            return jsonify({
                'status': 'success',
                'message': 'Picture taken successfully!',
                'image_url': image_url
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to capture image. Is camera connected?'
            }), 500

    except Exception as e:
        print(f"Error in /take-picture: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500