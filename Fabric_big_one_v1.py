# scaffold.py
"""
Scaffold complet du projet "Veille YouTube → TikTok" (local, Docker, port 4443).

▶ Utilisation
    python3 scaffold.py          # génère tous les fichiers
    cp .env.example .env && nano .env
    docker build -t veille-tiktok .
    docker run -d --name veille-tiktok -p 4443:4443 --env-file .env veille-tiktok

Le script écrit :
- Backend Flask (app.py), modèles (models.py), client YouTube (youtube_client.py)
- Scheduler (APScheduler) intégré (1 worker gunicorn pour éviter les doublons)
- Templates Jinja (UI pastel) + static/styles.css
- Tests (pytest), Dockerfile, requirements.txt, README, .dockerignore
- Scripts utilitaires : manage.sh, clean_scaffold.sh
"""
from __future__ import annotations
import os
from pathlib import Path

ROOT = Path.cwd()
FILES: dict[str, str] = {}

def add(path: str, content: str) -> None:
    FILES[path] = content.lstrip("\n")

# ---------------------------
# .dockerignore (SAFE)
# ---------------------------
add(
    ".dockerignore",
    r"""
# garder le code, ignorer ce qui est inutile
.git
__pycache__/
*.pyc
*.pyo
*.pyd
*.log
*.sqlite
*.sqlite3
.pytest_cache/

# envs locaux
venv/
.venv/

# secrets locaux (passés via --env-file)
.env
    """,
)

# ---------------------------
# .gitignore
# ---------------------------
add(
    ".gitignore",
    r"""
.env
*.db
__pycache__/
*.pyc
.pytest_cache/
venv/
.venv/
    """,
)

# ---------------------------
# requirements.txt
# ---------------------------
add(
    "requirements.txt",
    r"""
Flask==3.0.3
Flask-SQLAlchemy==3.1.1
SQLAlchemy==2.0.32
google-api-python-client==2.137.0
python-dotenv==1.0.1
APScheduler==3.10.4
requests==2.32.3
isodate==0.6.1
gunicorn==22.0.0
pytest==8.3.3
    """,
)

# ---------------------------
# .env.example
# ---------------------------
add(
    ".env.example",
    r"""
# Sécurité minimale
APP_USERNAME=admin
APP_PASSWORD=adminpass
SECRET_KEY=change-me

# YouTube
YOUTUBE_API_KEY=COLLE_TA_CLE_ICI

# Horaires (HH:MM)
SCHEDULE_MORNING=08:00
SCHEDULE_NOON=13:00
SCHEDULE_EVENING=19:00

# Régions (FR,US,ES)
REGIONS=FR,US,ES

# Thèmes (modifiable)
THEMES=nourriture,voiture,business,drôle,influenceurs

# Alerte flash (minutes)
ALERT_INTERVAL_MIN=15
    """,
)

# ---------------------------
# config.py
# ---------------------------
add(
    "config.py",
    r"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///data.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security (basic auth)
    APP_USERNAME = os.getenv("APP_USERNAME", "admin")
    APP_PASSWORD = os.getenv("APP_PASSWORD", "adminpass")

    # YouTube API
    YT_API_KEY = os.getenv("YOUTUBE_API_KEY", "")

    # Scheduling (HH:MM, 24h)
    SCHEDULE_MORNING = os.getenv("SCHEDULE_MORNING", "08:00")
    SCHEDULE_NOON = os.getenv("SCHEDULE_NOON", "13:00")
    SCHEDULE_EVENING = os.getenv("SCHEDULE_EVENING", "19:00")

    # Regions et thèmes
    REGIONS = [r.strip() for r in os.getenv("REGIONS", "FR,US,ES").split(",") if r.strip()]
    THEMES = [t.strip() for t in os.getenv(
        "THEMES",
        "nourriture,voiture,business,drôle,influenceurs"
    ).split(",") if t.strip()]

    # Alertes: intervalle en minutes
    ALERT_INTERVAL_MIN = int(os.getenv("ALERT_INTERVAL_MIN", "15"))
    """,
)

# ---------------------------
# models.py
# ---------------------------
add(
    "models.py",
    r"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index

db = SQLAlchemy()

class Video(db.Model):
    __tablename__ = "videos"
    id = db.Column(db.Integer, primary_key=True)
    yt_id = db.Column(db.String(32), unique=True, nullable=False)
    title = db.Column(db.String(512), nullable=False)
    channel = db.Column(db.String(256))
    url = db.Column(db.String(512))
    thumbnail = db.Column(db.String(512))
    category_id = db.Column(db.String(16))
    region = db.Column(db.String(8))
    language = db.Column(db.String(8))
    published_at = db.Column(db.DateTime)

    views_initial = db.Column(db.Integer, default=0)
    likes_initial = db.Column(db.Integer, default=0)
    views_current = db.Column(db.Integer, default=0)
    likes_current = db.Column(db.Integer, default=0)

    is_short = db.Column(db.Boolean, default=False)
    used = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def views_per_hour(self) -> float:
        if not self.published_at or not self.views_current:
            return 0.0
        hours = max((datetime.utcnow() - self.published_at).total_seconds() / 3600.0, 0.016)
        return float(self.views_current) / hours

Index("idx_video_used_created", Video.used, Video.created_at.desc())

class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey("videos.id"), nullable=False)
    content = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class StatSnapshot(db.Model):
    __tablename__ = "stat_snapshots"
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey("videos.id"), nullable=False)
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    captured_at = db.Column(db.DateTime, default=datetime.utcnow)
    """,
)

# ---------------------------
# youtube_client.py
# ---------------------------
add(
    "youtube_client.py",
    r"""
from datetime import datetime, timezone
from typing import List, Dict, Any
from googleapiclient.discovery import build

YOUTUBE_CATEGORIES = {
    "autos": "2",
    "comedy": "23",
    "education": "27",
    "entertainment": "24",
    "howto": "26",
    "people": "22",
    "sports": "17",
    "gaming": "20",
    "music": "10",
}

THEME_RULES = {
    "voiture": {"category_ids": [YOUTUBE_CATEGORIES["autos"]], "keywords": ["car", "voiture", "auto", "tuning"]},
    "drôle": {"category_ids": [YOUTUBE_CATEGORIES["comedy"]], "keywords": ["funny", "prank", "drôle", "humour"]},
    "business": {"category_ids": [YOUTUBE_CATEGORIES["education"], YOUTUBE_CATEGORIES["people"]], "keywords": ["business", "finance", "entrepreneur"]},
    "nourriture": {"category_ids": [YOUTUBE_CATEGORIES["howto"], YOUTUBE_CATEGORIES["people"]], "keywords": ["food", "recette", "cuisine", "street food"]},
    "influenceurs": {"category_ids": [YOUTUBE_CATEGORIES["entertainment"], YOUTUBE_CATEGORIES["people"]], "keywords": ["vlog", "influence", "storytime"]},
    "gaming": {"category_ids": [YOUTUBE_CATEGORIES["gaming"]], "keywords": ["game", "gaming", "let's play"]},
    "sport": {"category_ids": [YOUTUBE_CATEGORIES["sports"]], "keywords": ["match", "goal", "highlights"]},
    "musique": {"category_ids": [YOUTUBE_CATEGORIES["music"]], "keywords": ["official video", "lyrics", "clip"]},
}

class YouTubeClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.service = build("youtube", "v3", developerKey=api_key)

    def most_popular(self, region: str, max_results: int = 50) -> List[Dict[str, Any]]:
        req = self.service.videos().list(
            part="id,snippet,statistics,contentDetails",
            chart="mostPopular",
            regionCode=region,
            maxResults=max_results,
        )
        res = req.execute()
        return res.get("items", [])

    @staticmethod
    def parse_published_at(s: str) -> datetime | None:
        try:
            return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc).replace(tzinfo=None)
        except Exception:
            return None
    """,
)

# ---------------------------
# app.py (scheduler + UI)
# ---------------------------
add(
    "app.py",
    r"""
from __future__ import annotations
import hmac
from datetime import datetime, timedelta
from typing import List
from flask import Flask, render_template, redirect, request, url_for, jsonify, Response
from apscheduler.schedulers.background import BackgroundScheduler

from config import Config
from models import db, Video, Note, StatSnapshot
from youtube_client import YouTubeClient, THEME_RULES

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
with app.app_context():
    db.create_all()

# --- YouTube client ---
yt = YouTubeClient(Config.YT_API_KEY) if Config.YT_API_KEY else None

# --- Basic Auth ---
def _eq(a: str, b: str) -> bool:
    return hmac.compare_digest(a or "", b or "")

def check_auth(username, password):
    return _eq(username, Config.APP_USERNAME) and _eq(password, Config.APP_PASSWORD)

def authenticate():
    return Response("Authentication required", 401, {"WWW-Authenticate": 'Basic realm="Login Required"'})

def requires_auth(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# --- Helpers ---
REGION_LANG = {"FR": "fr", "US": "en", "ES": "es"}
THEME_LIST = [t.strip() for t in Config.THEMES if t.strip()]

def _now():
    return datetime.utcnow()

def pick_theme_video(items, theme_name: str):
    rules = THEME_RULES.get(theme_name, {})
    cat_ids = set(rules.get("category_ids", []))
    keywords = [k.lower() for k in rules.get("keywords", [])]

    best = None
    best_score = -1.0

    for it in items:
        snip = it.get("snippet", {})
        stats = it.get("statistics", {})
        title = snip.get("title", "")
        cat = snip.get("categoryId")
        views = int(stats.get("viewCount", 0))
        published_at = snip.get("publishedAt")
        published_dt = YouTubeClient.parse_published_at(published_at) if published_at else None

        hours = max((_now() - published_dt).total_seconds() / 3600.0, 0.016) if published_dt else 1.0
        vph = views / hours

        title_l = title.lower()
        kw_match = any(k in title_l for k in keywords) if keywords else False
        cat_match = cat in cat_ids if cat_ids else False

        score = vph * (1.4 if (kw_match or cat_match) else 1.0)
        if score > best_score:
            best_score = score
            best = it
    return best

from isodate import parse_duration

def compute_is_short(content_details) -> bool:
    dur = content_details.get("duration") if content_details else None
    if not dur:
        return False
    try:
        seconds = int(parse_duration(dur).total_seconds())
        return seconds <= 60
    except Exception:
        return False

@app.context_processor
def inject_now_and_next():
    now = _now()
    times = [Config.SCHEDULE_MORNING, Config.SCHEDULE_NOON, Config.SCHEDULE_EVENING]
    next_dt = None
    for t in times:
        h, m = [int(x) for x in t.split(":")]
        target = now.replace(hour=h, minute=m, second=0, microsecond=0)
        if target > now:
            next_dt = target
            break
    if not next_dt:
        h, m = [int(x) for x in Config.SCHEDULE_MORNING.split(":")]
        next_dt = (now + timedelta(days=1)).replace(hour=h, minute=m, second=0, microsecond=0)
    return {"server_now": now, "next_refresh": next_dt}

# --- Views ---
@app.route("/")
@requires_auth
def index():
    videos = Video.query.filter_by(used=False).order_by(Video.created_at.desc()).limit(5).all()
    return render_template("index.html", videos=videos, themes=THEME_LIST)

@app.route("/history")
@requires_auth
def history():
    videos = Video.query.filter_by(used=True).order_by(Video.created_at.desc()).all()
    last_snaps = {}
    for v in videos:
        snap = (
            StatSnapshot.query.filter_by(video_id=v.id)
            .order_by(StatSnapshot.captured_at.desc())
            .first()
        )
        last_snaps[v.id] = snap
    return render_template("history.html", videos=videos, snaps=last_snaps)

@app.route("/use/<int:vid>", methods=["POST"]) 
@requires_auth
def mark_used(vid):
    v = Video.query.get_or_404(vid)
    v.used = True
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/note/<int:vid>", methods=["POST"]) 
@requires_auth
def add_note(vid):
    content = request.form.get("content", "").strip()
    if content:
        n = Note(video_id=vid, content=content)
        db.session.add(n)
        db.session.commit()
    return redirect(url_for("history"))

@app.route("/api/refresh", methods=["POST"]) 
@requires_auth
def api_refresh():
    count = refresh_trending()
    return jsonify({"status": "ok", "added": count})

@app.route("/api/stats-refresh", methods=["POST"]) 
@requires_auth
def api_stats_refresh():
    refresh_stats()
    return jsonify({"status": "ok"})

# --- Workers ---

def refresh_trending() -> int:
    if yt is None:
        return 0

    added = 0
    items_all: List[dict] = []
    for region in Config.REGIONS:
        try:
            items = yt.most_popular(region=region, max_results=50)
            for it in items:
                it["_region"] = region
            items_all.extend(items)
        except Exception as e:
            print("YouTube API error:", e)

    for theme in THEME_LIST:
        best = pick_theme_video(items_all, theme)
        if not best:
            continue
        yt_id = best["id"]
        if Video.query.filter_by(yt_id=yt_id).first():
            continue

        snip = best.get("snippet", {})
        stats = best.get("statistics", {})
        cont = best.get("contentDetails", {})
        region = best.get("_region")

        v = Video(
            yt_id=yt_id,
            title=snip.get("title", ""),
            channel=snip.get("channelTitle"),
            url=f"https://www.youtube.com/watch?v={yt_id}",
            thumbnail=(snip.get("thumbnails", {}).get("medium", {}).get("url")
                       or snip.get("thumbnails", {}).get("default", {}).get("url")),
            category_id=snip.get("categoryId"),
            region=region,
            language=REGION_LANG.get(region, ""),
            published_at=YouTubeClient.parse_published_at(snip.get("publishedAt")),
            views_initial=int(stats.get("viewCount", 0)),
            likes_initial=int(stats.get("likeCount", 0)) if stats.get("likeCount") else 0,
            views_current=int(stats.get("viewCount", 0)),
            likes_current=int(stats.get("likeCount", 0)) if stats.get("likeCount") else 0,
            is_short=compute_is_short(cont),
        )
        db.session.add(v)
        db.session.commit()
        snap = StatSnapshot(video_id=v.id, views=v.views_current, likes=v.likes_current)
        db.session.add(snap)
        db.session.commit()
        added += 1
        if added >= 5:
            break

    print(f"[refresh_trending] Added {added} videos at {datetime.utcnow()} UTC")
    return added


def refresh_stats():
    if yt is None:
        return
    vids = Video.query.all()
    for i in range(0, len(vids), 50):
        chunk = vids[i:i+50]
        ids = [v.yt_id for v in chunk]
        try:
            res = yt.service.videos().list(part="id,statistics", id=",".join(ids)).execute()
            by_id = {it["id"]: it for it in res.get("items", [])}
            for v in chunk:
                it = by_id.get(v.yt_id)
                if not it:
                    continue
                stats = it.get("statistics", {})
                v.views_current = int(stats.get("viewCount", v.views_current or 0))
                v.likes_current = int(stats.get("likeCount", v.likes_current or 0)) if stats.get("likeCount") else v.likes_current
                db.session.add(v)
                db.session.flush()
                db.session.add(StatSnapshot(video_id=v.id, views=v.views_current, likes=v.likes_current))
            db.session.commit()
        except Exception as e:
            print("YouTube stats refresh error:", e)


def flash_alert_scan():
    if yt is None:
        return
    try:
        items = []
        for region in Config.REGIONS:
            items.extend(yt.most_popular(region=region, max_results=25))
        threshold = 500_000.0
        best = None
        best_vph = 0.0
        for it in items:
            stats = it.get("statistics", {})
            snip = it.get("snippet", {})
            views = int(stats.get("viewCount", 0))
            pub = snip.get("publishedAt")
            dt = YouTubeClient.parse_published_at(pub) if pub else None
            if not dt:
                continue
            hours = max((_now() - dt).total_seconds()/3600.0, 0.016)
            vph = views / hours
            if vph > threshold and vph > best_vph:
                best_vph = vph
                best = it
        if best:
            yt_id = best["id"]
            if not Video.query.filter_by(yt_id=yt_id).first():
                snip = best.get("snippet", {})
                stats = best.get("statistics", {})
                cont = best.get("contentDetails", {})
                v = Video(
                    yt_id=yt_id,
                    title=snip.get("title", ""),
                    channel=snip.get("channelTitle"),
                    url=f"https://www.youtube.com/watch?v={yt_id}",
                    thumbnail=(snip.get("thumbnails", {}).get("medium", {}).get("url")
                               or snip.get("thumbnails", {}).get("default", {}).get("url")),
                    category_id=snip.get("categoryId"),
                    region="BONUS",
                    language="",
                    published_at=YouTubeClient.parse_published_at(snip.get("publishedAt")),
                    views_initial=int(stats.get("viewCount", 0)),
                    likes_initial=int(stats.get("likeCount", 0)) if stats.get("likeCount") else 0,
                    views_current=int(stats.get("viewCount", 0)),
                    likes_current=int(stats.get("likeCount", 0)) if stats.get("likeCount") else 0,
                    is_short=compute_is_short(cont),
                )
                db.session.add(v)
                db.session.commit()
                db.session.add(StatSnapshot(video_id=v.id, views=v.views_current, likes=v.likes_current))
                db.session.commit()
                print(f"[flash_alert] Added FLASH video {yt_id} at VPH={best_vph:.0f}")
    except Exception as e:
        print("flash_alert_scan error:", e)

# --- Scheduler (unique instance) ---
scheduler = BackgroundScheduler(timezone="UTC")

# Helper pour exécuter un job dans le contexte Flask

def _run(fn):
    with app.app_context():
        fn()

# Fonctions de job (sans décorateurs)

def _job_morning():
    _run(refresh_trending)

def _job_noon():
    _run(refresh_trending)

def _job_evening():
    _run(refresh_trending)

def _job_stats():
    _run(refresh_stats)

def _job_flash():
    _run(flash_alert_scan)

# Ajout des jobs dynamiquement avec des valeurs HH:MM parsées

def _parse_hm(s: str):
    h, m = [int(x) for x in s.split(":")]
    return h, m

h, m = _parse_hm(Config.SCHEDULE_MORNING)
scheduler.add_job(_job_morning, "cron", hour=h, minute=m, id="refresh_morning", replace_existing=True)

h, m = _parse_hm(Config.SCHEDULE_NOON)
scheduler.add_job(_job_noon, "cron", hour=h, minute=m, id="refresh_noon", replace_existing=True)

h, m = _parse_hm(Config.SCHEDULE_EVENING)
scheduler.add_job(_job_evening, "cron", hour=h, minute=m, id="refresh_evening", replace_existing=True)

scheduler.add_job(_job_stats, "interval", minutes=60, id="refresh_stats", replace_existing=True)
scheduler.add_job(_job_flash, "interval", minutes=Config.ALERT_INTERVAL_MIN, id="flash_alert", replace_existing=True)

# Démarrer le scheduler à l'import (1 worker gunicorn => 1 scheduler)
scheduler.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4443, debug=True)
    """,
)

# ---------------------------
# templates/base.html
# ---------------------------
add(
    "templates/base.html",
    r"""
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Veille YouTube & TikTok</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body class="bg-pastel">
  <nav class="navbar navbar-expand-lg navbar-dark glass-nav">
    <div class="container">
      <a class="navbar-brand d-flex align-items-center gap-2" href="/">
        <span class="brand-logo">⚡</span>
        <span class="fw-bold">Veille Trends</span>
      </a>
      <div class="ms-auto d-flex gap-2">
        <a class="btn btn-light btn-sm soft-btn" href="/">Accueil</a>
        <a class="btn btn-outline-light btn-sm soft-btn" href="/history">Historique</a>
      </div>
    </div>
  </nav>

  <main class="container py-5">
    {% block content %}{% endblock %}
  </main>

  <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 1080">
    <div id="toast" class="toast align-items-center text-bg-success border-0" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="d-flex">
        <div class="toast-body" id="toast-body">Action réussie</div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
    </div>
  </div>

  <div id="overlay" class="overlay d-none">
    <div class="spinner-border" role="status"><span class="visually-hidden">Chargement...</span></div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
  <script>
    function showToast(msg, danger=false){
      const toastEl = document.getElementById('toast');
      const body = document.getElementById('toast-body');
      body.textContent = msg;
      toastEl.classList.toggle('text-bg-danger', !!danger);
      new bootstrap.Toast(toastEl).show();
    }
    async function postJSON(url){
      const ov = document.getElementById('overlay');
      ov.classList.remove('d-none');
      try{ const r = await fetch(url,{method:'POST'}); const d=await r.json(); showToast('Opération effectuée ✔️'); setTimeout(()=>location.reload(), 600); return d; }
      catch(e){ showToast('Erreur: '+e.message,true); }
      finally{ ov.classList.add('d-none'); }
    }
    document.addEventListener('click', (e)=>{
      if(e.target && e.target.matches('#refreshNow')){ e.preventDefault(); postJSON('/api/refresh'); }
      if(e.target && e.target.matches('#refreshStats')){ e.preventDefault(); postJSON('/api/stats-refresh'); }
    });
  </script>
</body>
</html>
    """,
)

# ---------------------------
# templates/index.html
# ---------------------------
add(
    "templates/index.html",
    r"""
{% extends 'base.html' %}
{% block content %}
<section class="hero mb-4">
  <div class="d-flex justify-content-between align-items-center">
    <div>
      <h1 class="display-6 fw-semibold">Sélection actuelle</h1>
      <p class="text-muted mb-0">Les 5 meilleures idées du créneau, classées par vélocité.</p>
    </div>
    <div class="text-end">
      <div class="small text-muted">Prochain refresh dans</div>
      <div id="countdown" class="fw-bold h4 mb-0">--</div>
      <div class="mt-2 d-flex gap-2 justify-content-end">
        <a href="#" id="refreshNow" class="btn btn-primary soft-btn">Rafraîchir maintenant</a>
        <a href="#" id="refreshStats" class="btn btn-outline-secondary soft-btn">Mettre à jour stats</a>
      </div>
    </div>
  </div>
</section>

{% if videos|length == 0 %}
  <div class="empty card shadow-sm border-0 p-4 text-center">
    <div class="emoji">🔎</div>
    <h5 class="mt-2">Aucune vidéo pour le moment</h5>
    <p class="text-muted">Clique sur <strong>Rafraîchir maintenant</strong> pour récupérer les tendances.</p>
    <a href="#" id="refreshNow" class="btn btn-primary soft-btn">Rafraîchir maintenant</a>
  </div>
{% else %}
  <div class="row g-4">
    {% for v in videos %}
    <div class="col-xl-4 col-lg-6">
      <div class="card trend-card shadow-sm border-0 h-100">
        <div class="thumb-wrap">
          <a href="{{ v.url }}" target="_blank">
            <img src="{{ v.thumbnail }}" class="thumb" alt="thumb">
          </a>
          {% if v.is_short %}<span class="badge soft-badge badge-short">Short</span>{% endif %}
          {% if v.region %}<span class="badge soft-badge badge-region">{{ v.region }}</span>{% endif %}
        </div>
        <div class="card-body d-flex flex-column">
          <a href="{{ v.url }}" target="_blank" class="stretched-link text-decoration-none text-dark"><h6 class="card-title clamp-2">{{ v.title }}</h6></a>
          <div class="text-muted small mb-2">{{ v.channel }}</div>
          <div class="d-flex flex-wrap gap-2 mt-auto">
            <span class="chip">{{ '{:,}'.format(v.views_current).replace(',', ' ') }} vues</span>
            {% set vph = '%.0f' % v.views_per_hour() %}
            <span class="chip chip-accent">🚀 {{ vph }} vues/h</span>
          </div>
          <form class="mt-3" method="post" action="/use/{{ v.id }}">
            <button class="btn w-100 btn-outline-primary soft-btn">Marquer comme utilisée</button>
          </form>
        </div>
      </div>
    </div>
    {% endfor %}
  </div>
{% endif %}

<script>
(function(){
  const el = document.getElementById('countdown');
  if(!el) return;
  const nextRefreshTs = new Date("{{ next_refresh.isoformat() }}Z").getTime();
  setInterval(()=>{
    const now = Date.now();
    let diff = Math.max(0, nextRefreshTs - now);
    const h = Math.floor(diff/3600000); diff%=3600000;
    const m = Math.floor(diff/60000); diff%=60000;
    const s = Math.floor(diff/1000);
    el.textContent = `${String(h).padStart(2,'0')}h ${String(m).padStart(2,'0')}m ${String(s).padStart(2,'0')}s`;
  }, 1000);
})();
</script>
{% endblock %}
    """,
)

# ---------------------------
# templates/history.html
# ---------------------------
add(
    "templates/history.html",
    r"""
{% extends 'base.html' %}
{% block content %}
<section class="hero mb-4">
  <div class="d-flex justify-content-between align-items-end">
    <div>
      <h1 class="display-6 fw-semibold">Historique</h1>
      <p class="text-muted mb-0">Suivi de l’évolution des vues et notes personnelles.</p>
    </div>
    <div>
      <a href="#" id="refreshStats" class="btn btn-outline-secondary soft-btn">Rafraîchir les stats</a>
    </div>
  </div>
</section>

{% if videos|length == 0 %}
  <div class="empty card shadow-sm border-0 p-4 text-center">
    <div class="emoji">🗂️</div>
    <h5 class="mt-2">Aucune vidéo utilisée pour le moment</h5>
    <p class="text-muted">Marque des vidéos depuis l’accueil pour commencer le suivi.</p>
  </div>
{% else %}
  <div class="row g-4">
    {% for v in videos %}
    <div class="col-xl-6">
      <div class="card shadow-sm border-0 h-100">
        <div class="row g-0">
          <div class="col-4 p-2">
            <img src="{{ v.thumbnail }}" class="thumb rounded" alt="thumb">
          </div>
          <div class="col-8">
            <div class="card-body pt-3 pb-2">
              <a href="{{ v.url }}" target="_blank" class="text-decoration-none"><h6 class="card-title clamp-2">{{ v.title }}</h6></a>
              <div class="small text-muted">{{ v.channel }} • {{ v.region }}</div>
              {% set latest = snaps.get(v.id) %}
              <div class="d-flex flex-wrap gap-2 mt-2">
                <span class="chip">Initial: {{ '{:,}'.format(v.views_initial).replace(',', ' ') }}</span>
                <span class="chip">Actuel: {{ '{:,}'.format(v.views_current).replace(',', ' ') }}</span>
                {% if latest %}
                {% set hours = ((latest.captured_at - v.created_at).total_seconds() / 3600.0) | round(1) %}
                <span class="chip chip-accent">+ {{ (v.views_current - v.views_initial) | int }} vues / {{ hours }}h</span>
                {% endif %}
              </div>
              <form class="mt-3" method="post" action="/note/{{ v.id }}">
                <div class="input-group">
                  <input type="text" name="content" class="form-control" placeholder="Ajouter une note (idée TikTok, résultat, etc.)">
                  <button class="btn btn-primary soft-btn">Ajouter</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
    {% endfor %}
  </div>
{% endif %}
{% endblock %}
    """,
)

# ---------------------------
# static/styles.css
# ---------------------------
add(
    "static/styles.css",
    r"""
:root{
  --pastel-bg: #f4f6ff;
  --grad-a: #7a8cff;
  --grad-b: #b18cff;
  --ink: #1f2440;
  --chip: #edf0ff;
}
body{ background: linear-gradient(180deg, #f8f9ff 0%, #f1f3ff 100%); font-family: 'Inter', system-ui, -apple-system, Segoe UI, Roboto, sans-serif; color: var(--ink); }
.glass-nav{ background: linear-gradient(90deg, var(--grad-a), var(--grad-b)); backdrop-filter: blur(8px); box-shadow: 0 6px 24px rgba(122,140,255,.25); }
.soft-btn{ border-radius: 12px; box-shadow: 0 4px 14px rgba(0,0,0,.06); }
.hero{ background: white; border-radius: 20px; padding: 22px; box-shadow: 0 10px 30px rgba(71,88,255,.07); border: 1px solid #eef0ff; }
.card{ border-radius: 18px; }
.trend-card .thumb-wrap{ position: relative; }
.thumb{ width: 100%; height: 170px; object-fit: cover; border-top-left-radius: 18px; border-top-right-radius: 18px; }
.soft-badge{ position: absolute; top: 10px; left: 10px; background: rgba(255,255,255,.85); backdrop-filter: blur(4px); color: var(--ink); border-radius: 999px; padding: 4px 10px; font-weight: 600; }
.badge-region{ left: auto; right: 10px; }
.badge-short{ background: rgba(255,240,199,.9); }
.chip{ background: var(--chip); border-radius: 999px; padding: 6px 10px; font-weight: 600; font-size: .85rem; }
.chip-accent{ background: #e9f5ff; }
.clamp-2{ display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.empty .emoji{ font-size: 42px; }
.overlay{ position: fixed; inset: 0; display: grid; place-items: center; background: rgba(255,255,255,.5); backdrop-filter: blur(2px); }
#countdown{ letter-spacing: .5px; }
    """,
)

# ---------------------------
# Dockerfile
# ---------------------------
add(
    "Dockerfile",
    r"""
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 4443

# 1 seul worker pour éviter plusieurs schedulers en parallèle
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:4443", "app:app"]
    """,
)

# ---------------------------
# README.md
# ---------------------------
add(
    "README.md",
    r"""
# Veille YouTube → TikTok (Local, Docker)

## 3 commandes vitales
```bash
cp .env.example .env && nano .env      # 1) mets ta clé YOUTUBE_API_KEY + identifiants

docker build -t veille-tiktok .        # 2) build l'image

docker run -d --name veille-tiktok \
  -p 4443:4443 --env-file .env \
  --restart=always veille-tiktok       # 3) lance (et redémarre au boot)
```

Interface (local) : http://localhost:4443  
Identifiants : APP_USERNAME / APP_PASSWORD (dans `.env`)
    """,
)

# ---------------------------
# manage.sh
# ---------------------------
add(
    "manage.sh",
    r"""
#!/usr/bin/env bash
set -euo pipefail
IMAGE="veille-tiktok"; NAME="veille-tiktok"; PORT="4443"; ENV_FILE=".env"
usage(){ cat <<USAGE
Usage: $0 <cmd>
  up|build|run|start|stop|restart|status|logs|clean|nuke|refresh|stats|help
USAGE
}
exists_container(){ docker ps -a --format '{{.Names}}' | grep -q "^${NAME}$"; }
build(){ docker build -t ${IMAGE} .; }
run(){ docker run -d --name ${NAME} -p ${PORT}:${PORT} --env-file ${ENV_FILE} --restart=always ${IMAGE}; }
start(){ docker start ${NAME}; }
stop(){ docker stop ${NAME}; }
restart(){ docker restart ${NAME}; }
status(){ docker ps -a --filter "name=${NAME}"; }
logs(){ docker logs -f ${NAME}; }
clean(){ exists_container && docker rm -f ${NAME} || true; }
nuke(){ clean; docker images --format '{{.Repository}}:{{.Tag}}' | grep -q "^${IMAGE}:" && docker rmi -f ${IMAGE} || true; }
read_env(){ [[ -f "${ENV_FILE}" ]] || { echo "${ENV_FILE} introuvable"; return 1; }; APP_USERNAME=$(grep -E '^APP_USERNAME=' ${ENV_FILE} | cut -d= -f2-); APP_PASSWORD=$(grep -E '^APP_PASSWORD=' ${ENV_FILE} | cut -d= -f2-); }
refresh(){ read_env && curl -sS -u "$APP_USERNAME:$APP_PASSWORD" -X POST http://localhost:${PORT}/api/refresh | jq . || true; }
stats(){ read_env && curl -sS -u "$APP_USERNAME:$APP_PASSWORD" -X POST http://localhost:${PORT}/api/stats-refresh | jq . || true; }
cmd=${1:-help}
case "$cmd" in
  up) build; clean; run;; build) build;; run) run;; start) start;; stop) stop;; restart) restart;; status) status;; logs) logs;; clean) clean;; nuke) nuke;; refresh) refresh;; stats) stats;; help|-h|--help) usage;; *) echo "Commande inconnue: $cmd"; usage; exit 1;; esac
    """,
)

# ---------------------------
# clean_scaffold.sh
# ---------------------------
add(
    "clean_scaffold.sh",
    r"""
#!/usr/bin/env bash
set -euo pipefail
DRY=0; ALL=0; DOCKER=0; ASK=1
for a in "$@"; do case "$a" in --dry-run) DRY=1;; --all) ALL=1;; --docker) DOCKER=1;; -y) ASK=0;; -h|--help) echo "--dry-run --all --docker -y"; exit 0;; *) echo "opt inconnue: $a"; exit 1;; esac; done
[[ -f scaffold.py ]] || { echo "scaffold.py introuvable"; exit 1; }
DEL=(".env" ".env.example" ".gitignore" ".dockerignore" "Dockerfile" "requirements.txt" "README.md" "manage.sh" "clean_scaffold.sh" "app.py" "config.py" "models.py" "youtube_client.py" "scheduler.py" "templates" "static" "tests" "data.db" "__pycache__" ".pytest_cache")
[[ $ALL -eq 1 ]] && DEL+=("scaffold.py")
EXIST=(); for p in "${DEL[@]}"; do [[ -e "$p" ]] && EXIST+=("$p"); done
[[ ${#EXIST[@]} -eq 0 && $DOCKER -eq 0 ]] && { echo "Rien à supprimer"; exit 0; }
echo "Suppression:"; for p in "${EXIST[@]}"; do echo " - $p"; done
[[ $DOCKER -eq 1 ]] && { echo " - Docker: conteneur & image veille-tiktok"; }
[[ $DRY -eq 1 ]] && { echo "Dry-run"; exit 0; }
[[ $ASK -eq 1 ]] && read -r -p "Confirmer ? (oui/NO) " ans && [[ "$ans" != "oui" ]] && { echo "Annulé"; exit 0; }
for p in "${EXIST[@]}"; do [[ -d "$p" ]] && rm -rf -- "$p" || rm -f -- "$p"; done
if [[ $DOCKER -eq 1 ]]; then docker stop veille-tiktok >/dev/null 2>&1 || true; docker rm veille-tiktok >/dev/null 2>&1 || true; docker rmi -f veille-tiktok >/dev/null 2>&1 || true; fi
echo "OK"
    """,
)

# ---------------------------
# tests/test_core.py
# ---------------------------
add(
    "tests/test_core.py",
    r"""
from datetime import datetime, timedelta
from models import Video

def test_views_per_hour_zero_when_missing_data():
    v = Video(views_current=0, published_at=None)
    assert v.views_per_hour() == 0.0

def test_views_per_hour_positive():
    v = Video(views_current=3600, published_at=datetime.utcnow() - timedelta(hours=1))
    assert 3500 <= v.views_per_hour() <= 3700

def test_schedule_format_examples():
    def is_hhmm(s):
        try:
            h, m = [int(x) for x in s.split(":")]
            return 0 <= h < 24 and 0 <= m < 60
        except Exception:
            return False
    assert is_hhmm("08:00")
    assert is_hhmm("13:00")
    assert is_hhmm("19:00")
    """,
)

# ---------------------------
# Écriture des fichiers + chmod
# ---------------------------
for path, content in FILES.items():
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

for exe in ("manage.sh", "clean_scaffold.sh"):
    try:
        os.chmod(ROOT / exe, 0o755)
    except Exception:
        pass

print("✅ Projet généré.")
print("""➡️ Étapes :
  1) cp .env.example .env && nano .env  (mets YOUTUBE_API_KEY et tes identifiants)
  2) docker build -t veille-tiktok .
  3) docker run -d --name veille-tiktok -p 4443:4443 --env-file .env veille-tiktok
  (option) démarrage auto : docker update --restart=always veille-tiktok
""")
