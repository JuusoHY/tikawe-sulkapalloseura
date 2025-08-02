import os
SECRET_KEY = os.environ.get("SECRET_KEY", "18fd24bf6a2ad4dac04a33963db1c42f")
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "database.db")
