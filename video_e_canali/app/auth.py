from flask import Blueprint, render_template, request, redirect, url_for, session, flash

bp = Blueprint("auth", __name__, url_prefix="/auth")

# Utente hardcoded solo per esempio
USER = {"username": "admin", "password": "admin"}

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == USER["username"] and password == USER["password"]:
            session["user"] = username
            flash("Login effettuato.", "success")
            return redirect(url_for("main.index"))
        flash("Credenziali non valide.", "danger")
    return render_template("login.html")

@bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logout effettuato.", "info")
    return redirect(url_for("main.index"))
