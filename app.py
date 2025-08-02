import click
import config
import db
from flask import Flask, render_template, request, redirect, url_for, flash, session
import users  # your users.py module

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY

# Close the database connection after each request
app.teardown_appcontext(db.close_db)

# Add the `flask init-db` command to initialize the database
@app.cli.command("init-db")
def init_db_command():
    """Create the database tables from schema.sql."""
    db.init_db()
    click.echo("Initialized the database.")

# Example home route
@app.route("/")
def index():
    return "Tervetuloa sovellukseen!"


# Show registration form
@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")

# Handle registration submission
@app.route("/register", methods=["POST"])
def register_post():
    username = request.form["username"]
    password = request.form["password"]
    password2 = request.form["password2"]

    if not username or not password:
        flash("Username and password are required.")
        return redirect(url_for("register"))

    if password != password2:
        flash("Passwords do not match.")
        return redirect(url_for("register"))

    try:
        users.create_user(username, password)
    except Exception:
        flash("Username already taken.")
        return redirect(url_for("register"))

    flash("Registration successful—please log in.")
    return redirect(url_for("login"))

# Show login form
@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

# Handle login submission
@app.route("/login", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    user_id = users.check_login(username, password)
    if user_id:
        session.clear()
        session["user_id"] = user_id
        session["username"] = username
        return redirect(url_for("index"))
    else:
        flash("Invalid credentials.")
        return redirect(url_for("login"))

# Log out
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))