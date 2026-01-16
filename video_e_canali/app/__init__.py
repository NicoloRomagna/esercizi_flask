import os
import sqlite3
from flask import Flask, g

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-key"
    app.config["DATABASE"] = os.path.join(app.instance_path, "app.db")

    # Assicura che la cartella instance/ esista
    os.makedirs(app.instance_path, exist_ok=True)

    # ---------------------------
    # DATABASE
    # ---------------------------
    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(
                app.config["DATABASE"],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
        return g.db

    def close_db(e=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    app.teardown_appcontext(close_db)
    app.get_db = get_db

    # ---------------------------
    # BLUEPRINTS
    # ---------------------------
    from . import main
    from . import auth
    from . import login
    from . import logout
    from . import register

    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(login.bp)
    app.register_blueprint(logout.bp)
    app.register_blueprint(register.bp)

    return app
