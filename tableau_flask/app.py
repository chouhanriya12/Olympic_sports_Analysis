"""
OlympicsAnalytics — Flask Application
=======================================
Global Olympic Sports Performance Analysis Platform

Run locally:
    pip install -r requirements.txt
    python data/prepare_data.py   # first time only
    python app.py

Production (Render):
    gunicorn app:app
"""

import os
import json
import subprocess
import sys
from pathlib import Path

from flask import Flask, render_template, jsonify, abort
from dotenv import load_dotenv

# ─── Environment ────────────────────────────────────────────────────────────
load_dotenv()

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
STATS_FILE = DATA_DIR / "stats.json"

# ─── Auto-run data preparation if stats.json doesn't exist ─────────────────
if not STATS_FILE.exists():
    print("stats.json not found — running prepare_data.py …")
    subprocess.run(
        [sys.executable, str(DATA_DIR / "prepare_data.py")],
        check=True,
    )

# ─── Load stats ────────────────────────────────────────────────────────────
def load_stats() -> dict:
    if STATS_FILE.exists():
        with open(STATS_FILE) as f:
            return json.load(f)
    return {}

# ─── Flask App ──────────────────────────────────────────────────────────────
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "olympic-analytics-2024-dev")
app.config["DEBUG"] = os.getenv("FLASK_DEBUG", "False").lower() == "true"

# ── Tableau configuration ────────────────────────────────────────────────────
# Paste your published Tableau Public / Tableau Server URLs here.
# Leave the default placeholders — the pages will show a "Connect Tableau" UI.
TABLEAU_CONFIG = {
    "dashboard_url": os.getenv(
        "TABLEAU_DASHBOARD_URL",
        "YOUR_TABLEAU_DASHBOARD_URL_HERE"
    ),
    "story_url": os.getenv(
        "TABLEAU_STORY_URL",
        "YOUR_TABLEAU_STORY_URL_HERE"
    ),
}

PLACEHOLDER_URL = "YOUR_TABLEAU"


# ─── Context processor ──────────────────────────────────────────────────────
@app.context_processor
def inject_globals():
    stats = load_stats()
    return {
        "stats": stats,
        "tableau": TABLEAU_CONFIG,
        "tableau_ready": not TABLEAU_CONFIG["dashboard_url"].startswith(PLACEHOLDER_URL),
    }


# ─── Routes ─────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    stats = load_stats()
    return render_template("index.html", stats=stats)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", tableau=TABLEAU_CONFIG)


@app.route("/story")
def story():
    return render_template("story.html", tableau=TABLEAU_CONFIG)


@app.route("/insights")
def insights():
    stats = load_stats()
    return render_template("insights.html", stats=stats)


@app.route("/about")
def about():
    return render_template("about.html")


# ─── API endpoints ──────────────────────────────────────────────────────────
@app.route("/api/stats")
def api_stats():
    """Return dataset statistics as JSON."""
    stats = load_stats()
    if not stats:
        return jsonify({"error": "Stats not yet computed. Run prepare_data.py"}), 503
    return jsonify(stats)


@app.route("/api/top-countries")
def api_top_countries():
    stats = load_stats()
    return jsonify(stats.get("top10_countries", []))


@app.route("/api/medals-by-year")
def api_medals_by_year():
    stats = load_stats()
    return jsonify(stats.get("medals_by_year", []))


@app.route("/api/gender-by-year")
def api_gender_by_year():
    stats = load_stats()
    return jsonify(stats.get("gender_by_year", []))


# ─── Error handlers ─────────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


# ─── Entry point ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])
