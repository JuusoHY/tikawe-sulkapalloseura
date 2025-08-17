import click
import secrets
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

def check_csrf():
    """Abort with 403 if CSRF token missing or invalid."""
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session.get("csrf_token"):
        abort(403)

# --- Home: list all announcements ---
@app.route("/")
def index():
    all_anns = announcements.get_announcements()
    return render_template("index.html", announcements=all_anns)

# --- Search ---
@app.route("/search")
def search():
    q = request.args.get("query", "").strip()
    if not q:
        return redirect(url_for("index"))
    results = announcements.find_announcements(q)
    return render_template("search_results.html", query=q, announcements=results)

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
        # Generate per-session CSRF token on login
        session["csrf_token"] = secrets.token_hex(16)
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

# --- Announcement CRUD + classifications ---

@app.route("/announcement/new")
def new_announcement():
    require_login()
    all_classes = announcements.get_all_classes()
    return render_template("new_announcement.html", all_classes=all_classes)

@app.route("/announcement/create", methods=["POST"])
def create_announcement():
    require_login()
    check_csrf()

    title       = request.form["title"]
    description = request.form["description"]
    location    = request.form["location"]
    time        = request.form["time"]
    slots       = request.form["slots_needed"]
    user_id     = session["user_id"]

    if not title or not description:
        flash("Title and description are required.")
        return redirect(url_for("new_announcement"))

    # Validate class selections against DB
    all_classes = announcements.get_all_classes()
    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

    ann_id = announcements.create_announcement(
        title, description, location, time, slots, user_id, classes
    )
    return redirect(url_for("show_announcement", ann_id=ann_id))

@app.route("/announcement/<int:ann_id>")
def show_announcement(ann_id):
    ann = announcements.get_announcement(ann_id)
    if not ann:
        abort(404)
    classes = announcements.get_classes(ann_id)
    msgs = announcements.get_messages(ann_id)
    return render_template("show_announcement.html", ann=ann, classes=classes, messages=msgs)

@app.route("/announcement/<int:ann_id>/edit")
def edit_announcement(ann_id):
    require_login()
    ann = announcements.get_announcement(ann_id)
    if not ann or ann["user_id"] != session["user_id"]:
        abort(403)

    all_classes = announcements.get_all_classes()
    selected = {title: "" for title in all_classes.keys()}
    for entry in announcements.get_classes(ann_id):
        selected[entry["title"]] = entry["value"]

    return render_template("edit_announcement.html", ann=ann, all_classes=all_classes, selected_classes=selected)

@app.route("/announcement/<int:ann_id>/update", methods=["POST"])
def update_announcement(ann_id):
    require_login()
    check_csrf()

    ann = announcements.get_announcement(ann_id)
    if not ann or ann["user_id"] != session["user_id"]:
        abort(403)

    title       = request.form["title"]
    description = request.form["description"]
    location    = request.form["location"]
    time        = request.form["time"]
    slots       = request.form["slots_needed"]

    # Validate class selections
    all_classes = announcements.get_all_classes()
    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

    announcements.update_announcement(
        ann_id, title, description, location, time, slots, classes
    )
    return redirect(url_for("show_announcement", ann_id=ann_id))

@app.route("/announcement/<int:ann_id>/delete", methods=["POST"])
def delete_announcement(ann_id):
    require_login()
    check_csrf()

    ann = announcements.get_announcement(ann_id)
    if not ann or ann["user_id"] != session["user_id"]:
        abort(403)
    announcements.delete_announcement(ann_id)
    return redirect(url_for("index"))

# --- Additional info/messages on someone else’s announcement ---

@app.route("/announcement/<int:ann_id>/message", methods=["POST"])
def add_message(ann_id):
    require_login()
    check_csrf()

    ann = announcements.get_announcement(ann_id)
    if not ann:
        abort(404)

    # Only on someone else’s announcement
    if ann["user_id"] == session["user_id"]:
        flash("You cannot send additional info to your own announcement.")
        return redirect(url_for("show_announcement", ann_id=ann_id))

    content = request.form.get("content", "").strip()
    if not content or len(content) > 1000:
        flash("Message must be 1–1000 characters.")
        return redirect(url_for("show_announcement", ann_id=ann_id))

    announcements.add_message(ann_id, session["user_id"], content)
    flash("Message added.")
    return redirect(url_for("show_announcement", ann_id=ann_id))
