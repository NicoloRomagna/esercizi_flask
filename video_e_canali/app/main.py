from flask import Blueprint, render_template, current_app, request, redirect, url_for, flash, session
from . import repository

bp = Blueprint("main", __name__)

def get_db():
    return current_app.get_db()

@bp.route("/")
def index():
    db = get_db()
    channels = repository.get_all_channels(db)
    return render_template("index.html", channels=channels)

@bp.route("/canali")
def channels():
    db = get_db()
    channels = repository.get_all_channels(db)
    return render_template("channels.html", channels=channels)

@bp.route("/canali/<int:channel_id>")
def channel_detail(channel_id):
    db = get_db()
    channel = repository.get_channel_by_id(db, channel_id)
    if channel is None:
        flash("Canale non trovato.", "warning")
        return redirect(url_for("main.channels"))
    videos = repository.get_videos_by_channel(db, channel_id)
    return render_template("channel_detail.html", channel=channel, videos=videos)

@bp.route("/canali/nuovo", methods=["GET", "POST"])
def create_channel():
    if "user" not in session:
        flash("Devi essere loggato per creare un canale.", "warning")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        categoria = request.form.get("categoria", "").strip()
        numero_iscritti = request.form.get("numero_iscritti", "0").strip() or "0"

        if not nome or not categoria:
            flash("Nome e categoria sono obbligatori.", "danger")
        else:
            try:
                numero_iscritti_int = int(numero_iscritti)
            except ValueError:
                numero_iscritti_int = 0
            db = get_db()
            repository.create_channel(db, nome, numero_iscritti_int, categoria)
            flash("Canale creato con successo.", "success")
            return redirect(url_for("main.channels"))

    return render_template("create_channel.html")

@bp.route("/canali/<int:channel_id>/video/nuovo", methods=["GET", "POST"])
def create_video(channel_id):
    if "user" not in session:
        flash("Devi essere loggato per inserire un video.", "warning")
        return redirect(url_for("auth.login"))

    db = get_db()
    channel = repository.get_channel_by_id(db, channel_id)
    if channel is None:
        flash("Canale non trovato.", "warning")
        return redirect(url_for("main.channels"))

    if request.method == "POST":
        titolo = request.form.get("titolo", "").strip()
        durata = request.form.get("durata", "").strip()
        immagine = request.form.get("immagine", "").strip() or None

        if not titolo or not durata:
            flash("Titolo e durata sono obbligatori.", "danger")
        else:
            try:
                durata_int = int(durata)
            except ValueError:
                durata_int = 0
            repository.create_video(db, channel_id, titolo, durata_int, immagine)
            flash("Video creato con successo.", "success")
            return redirect(url_for("main.channel_detail", channel_id=channel_id))

    return render_template("create_video.html", channel=channel)
