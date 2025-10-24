from app import create_app, db
from app.models import User
import click

# Create the app instance using our factory
app = create_app()


@app.cli.command("create-admin")
@click.argument("username")
@click.argument("password")
def create_admin(username, password):
    """Creates a new admin user."""
    if User.query.filter_by(username=username).first():
        print(f"User '{username}' already exists.")
        return

    admin = User(username=username)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    print(f"Admin user '{username}' created successfully.")


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)