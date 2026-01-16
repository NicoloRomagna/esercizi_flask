from typing import List, Optional, Dict

def get_all_channels(db) -> List[Dict]:
    cur = db.execute(
        "SELECT id, nome, numero_iscritti, categoria FROM canali ORDER BY nome"
    )
    return cur.fetchall()

def get_channel_by_id(db, channel_id: int):
    cur = db.execute(
        "SELECT id, nome, numero_iscritti, categoria FROM canali WHERE id = ?",
        (channel_id,),
    )
    return cur.fetchone()

def get_videos_by_channel(db, channel_id: int):
    cur = db.execute(
        """SELECT id, titolo, durata, immagine
           FROM video
           WHERE canale_id = ?
           ORDER BY id DESC""",
        (channel_id,),
    )
    return cur.fetchall()

def create_channel(db, nome: str, numero_iscritti: int, categoria: str):
    db.execute(
        "INSERT INTO canali (nome, numero_iscritti, categoria) VALUES (?, ?, ?)",
        (nome, numero_iscritti, categoria),
    )
    db.commit()

def create_video(db, canale_id: int, titolo: str, durata: int, immagine: Optional[str]):
    db.execute(
        "INSERT INTO video (canale_id, titolo, durata, immagine) VALUES (?, ?, ?, ?)",
        (canale_id, titolo, durata, immagine),
    )
    db.commit()
