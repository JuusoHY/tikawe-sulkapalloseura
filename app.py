import click
from flask import Flask
import config
import db

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
