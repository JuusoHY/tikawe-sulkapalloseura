import click
import sqlite3
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, abort
)
import config
import db
import users
import announcements

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY

# Close the DB at the end of each request
app.teardown_appcontext(db.close_db)

# CLI: flask init-db
@app.cli.command("init-db")
def init_db_command():
    """Initialize the database from schema.sql."""
    db.init_db()
    click.echo("Initialized the database.")

def require_login():
    """Abort with 403 if the user isn’t logged in."""
    if "user_id" not in session:
        abort(403)

# --- Home: list all announcements ---
@app.route("/")
def index():
    all_anns = announcements.get_announcements()
    return render_template("index.html", announcements=all_anns)

# --- User Registration & Login ---

@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")

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
    except sqlite3.IntegrityError:
        flash("Username already taken.")
        return redirect(url_for("register"))

    flash("Registration successful—please log in.")
    return redirect(url_for("login"))

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

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

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# --- User page: stats + user’s announcements ---

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_anns = users.get_announcements(user_id)
    total = users.get_announcement_count(user_id)
    return render_template("show_user.html", user=user, announcements=user_anns, total=total)

# --- Announcement CRUD ---

@app.route("/announcement/new")
def new_announcement():
    require_login()
    return render_template("new_announcement.html")

@app.route("/announcement/create", methods=["POST"])
def create_announcement():
    require_login()
    title       = request.form["title"]
    description = request.form["description"]
    location    = request.form["location"]
    time        = request.form["time"]
    slots       = request.form["slots_needed"]
    user_id     = session["user_id"]

    if not title or not description:
        flash("Title and description are required.")
        return redirect(url_for("new_announcement"))

    announcements.create_announcement(
        title, description, location, time, slots, user_id
    )
    return redirect(url_for("index"))

@app.route("/announcement/<int:ann_id>")
def show_announcement(ann_id):
    ann = announcements.get_announcement(ann_id)
    if not ann:
        abort(404)
    return render_template("show_announcement.html", ann=ann)

@app.route("/announcement/<int:ann_id>/edit")
def edit_announcement(ann_id):
    require_login()
    ann = announcements.get_announcement(ann_id)
    if not ann or ann["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_announcement.html", ann=ann)

@app.route("/announcement/<int:ann_id>/update", methods=["POST"])
def update_announcement(ann_id):
    require_login()
    ann = announcements.get_announcement(ann_id)
    if not ann or ann["user_id"] != session["user_id"]:
        abort(403)

    title       = request.form["title"]
    description = request.form["description"]
    location    = request.form["location"]
    time        = request.form["time"]
    slots       = request.form["slots_needed"]

    announcements.update_announcement(
        ann_id, title, description, location, time, slots
    )
    return redirect(url_for("show_announcement", ann_id=ann_id))

@app.route("/announcement/<int:ann_id>/delete", methods=["POST"])
def delete_announcement(ann_id):
    require_login()
    ann = announcements.get_announcement(ann_id)
    if not ann or ann["user_id"] != session["user_id"]:
        abort(403)
    announcements.delete_announcement(ann_id)
    return redirect(url_for("index"))
