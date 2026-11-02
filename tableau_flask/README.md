# 🔥 OlympicsAnalytics — Global Olympic Sports Performance Analysis

> A full-stack data analytics platform built with Python Flask, Tableau, Bootstrap 5 and Chart.js — analysing 120+ years of Olympic history.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Dataset](#dataset)
- [Tableau Integration](#tableau-integration)
- [Flask API Endpoints](#flask-api-endpoints)
- [Deployment on Render](#deployment-on-render)
- [Tableau Workbook — Step-by-Step Guide](#tableau-workbook--step-by-step-guide)
- [Final Demo Checklist](#final-demo-checklist)

---

## Project Overview

OlympicsAnalytics is a professional web application that transforms raw historical Olympic data into interactive visualisations and analytics insights. It combines:

| Layer | Technology |
|---|---|
| Backend | Python Flask 3.0 |
| Data Processing | Pandas, NumPy |
| Frontend | Bootstrap 5.3, Chart.js 4 |
| BI Dashboards | Tableau (Embedding API v3) |
| Deployment | Render (Gunicorn) |

---

## Features

- ✅ **5-page responsive website** — Home, Dashboard, Story, Insights, About
- ✅ **Olympic-themed dark navy & gold design**
- ✅ **8+ Chart.js visualisations** powered by real dataset values
- ✅ **Tableau Dashboard** embedded (with graceful placeholder when URL not set)
- ✅ **7-scene Tableau Story** embedded
- ✅ **Flask REST API** at `/api/stats`, `/api/top-countries`, `/api/medals-by-year`, `/api/gender-by-year`
- ✅ **Animated counters, scroll effects, responsive layout**
- ✅ **Auto data preparation** — runs `prepare_data.py` on first startup
- ✅ **Production-ready** — Gunicorn + Render deployment

---

## Project Structure

```
tableau_flask/
│
├── app.py                    # Flask application & routes
├── requirements.txt          # Python dependencies
├── Procfile                  # Gunicorn startup for Render
├── render.yaml               # Render configuration
├── .env.example              # Environment variable template
├── .gitignore
├── README.md
│
├── data/
│   ├── prepare_data.py       # Data cleaning & stats computation
│   ├── olympics.csv          # Cleaned dataset (auto-generated)
│   └── stats.json            # Pre-computed statistics (auto-generated)
│
├── templates/
│   ├── base.html             # Navbar + footer layout
│   ├── index.html            # Home page
│   ├── dashboard.html        # Tableau dashboard + Chart.js
│   ├── story.html            # Tableau story + scene cards
│   ├── insights.html         # Analytics insights
│   ├── about.html            # Project documentation
│   ├── 404.html
│   └── 500.html
│
└── static/
    ├── css/style.css         # Full design system
    ├── js/main.js            # Global JS (counters, scroll, AOS)
    └── img/                  # Place Olympic images here
```

---

## Quick Start

### 1. Clone / download the project

```bash
git clone <your-repo-url>
cd tableau_flask
```

### 2. Create a virtual environment

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare the dataset

```bash
python data/prepare_data.py
```

This generates `data/olympics.csv` and `data/stats.json`.

> **Optional**: If you have the Kaggle dataset (`athlete_events.csv`), copy it to `data/olympics_raw.csv` before running the script — it will use your real data instead of the built-in sample.

### 5. Configure environment (optional)

```bash
cp .env.example .env
# Edit .env and set your Tableau URLs and SECRET_KEY
```

### 6. Run the Flask app

```bash
python app.py
```

Visit **http://localhost:5000** in your browser.

---

## Dataset

The project uses the schema of the **Kaggle "120 Years of Olympic History"** dataset:

| Column | Description |
|--------|-------------|
| ID | Athlete unique identifier |
| Name | Full name |
| Sex | M / F |
| Age | Age at event |
| Team | Country name |
| NOC | 3-letter National Olympic Committee code |
| Games | e.g. "2000 Summer" |
| Year | Olympic year |
| Season | Summer / Winter |
| City | Host city |
| Sport | Sport category |
| Event | Specific event |
| Medal | Gold / Silver / Bronze / NaN |

**Important:** Records where Medal is NaN represent athletes who competed but did not win — these are **kept** to preserve participation statistics.

### Using the real Kaggle dataset

1. Download from: https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results
2. Place `athlete_events.csv` in the `data/` folder and rename it to `olympics_raw.csv`
3. Run `python data/prepare_data.py`

---

## Tableau Integration

### Setting your Tableau URLs

After publishing your workbook to Tableau Public:

**Method A — Environment variable (recommended for Render):**
```bash
TABLEAU_DASHBOARD_URL=https://public.tableau.com/views/YourWorkbook/Dashboard
TABLEAU_STORY_URL=https://public.tableau.com/views/YourWorkbook/Story
```

**Method B — Edit app.py directly:**
```python
TABLEAU_CONFIG = {
    "dashboard_url": "https://public.tableau.com/views/...",
    "story_url":     "https://public.tableau.com/views/...",
}
```

### Getting the correct Tableau embed URL

1. Open your workbook on Tableau Public
2. Click **Share** → **Copy Link**
3. The URL format is: `https://public.tableau.com/views/<WorkbookName>/<SheetName>`
4. Append `?:embed=y&:showVizHome=no` for direct embedding

---

## Flask API Endpoints

| Endpoint | Returns |
|----------|---------|
| `GET /api/stats` | Full statistics JSON |
| `GET /api/top-countries` | Top 10 countries by medal count |
| `GET /api/medals-by-year` | Medal totals per Olympic year |
| `GET /api/gender-by-year` | Male/Female counts per year |

---

## Deployment on Render

### Step-by-step

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit — OlympicsAnalytics"
   git remote add origin https://github.com/YOUR_USERNAME/olympics-analytics.git
   git push -u origin main
   ```

2. **Create a new Web Service on Render**
   - Go to https://render.com → New → Web Service
   - Connect your GitHub repository

3. **Configure the service**
   | Setting | Value |
   |---------|-------|
   | Environment | Python |
   | Build Command | `pip install -r requirements.txt && python data/prepare_data.py` |
   | Start Command | `gunicorn app:app` |
   | Instance Type | Free |

4. **Add Environment Variables** (in Render dashboard)
   ```
   SECRET_KEY          = <generate a random 32-char string>
   TABLEAU_DASHBOARD_URL = <your tableau dashboard URL>
   TABLEAU_STORY_URL     = <your tableau story URL>
   ```

5. **Deploy** — Render will build and deploy automatically. Your app will be live at `https://your-service-name.onrender.com`

---

## Tableau Workbook — Step-by-Step Guide

### Prerequisites
- Tableau Desktop (free trial) or Tableau Public Desktop
- The cleaned `data/olympics.csv` file

### Step 1: Connect to data
1. Open Tableau Desktop
2. **Connect → Text File** → select `data/olympics.csv`
3. Tableau auto-detects column types — verify `Year` is Number, `Medal` is String

### Step 2: Create Calculated Fields
| Field Name | Formula |
|-----------|---------|
| Is Gold | `[Medal] = "Gold"` |
| Is Silver | `[Medal] = "Silver"` |
| Is Bronze | `[Medal] = "Bronze"` |
| Total Medals | `IF NOT ISNULL([Medal]) THEN 1 ELSE 0 END` |
| Medal Count | `COUNTD(IF NOT ISNULL([Medal]) THEN [ID] END)` |

### Step 3: Build the 8 Charts

| # | Sheet Name | Chart Type | Details |
|---|-----------|-----------|---------|
| 1 | Medal Map | Filled Map | Country → Colour by sum(Total Medals) |
| 2 | Top 10 Countries | Horizontal Bar | NOC → Medals, sorted desc, top 10 |
| 3 | Gold/Silver/Bronze | Stacked Bar | NOC → stacked by medal type |
| 4 | Medals Over Time | Line | Year → sum(Medals) |
| 5 | Gender Participation | Stacked Bar | Year → count, colour by Sex |
| 6 | Sports Medals | Horizontal Bar | Sport → medals, sorted desc |
| 7 | Country Comparison | Side-by-side Bar | Year vs NOC filtered |
| 8 | Athlete Trends | Line | Year → COUNTD(ID) |

### Step 4: Create Filters (apply to all sheets)
- Year (slider range)
- NOC / Team (multiple select)
- Sport (multiple select)
- Sex (radio)
- Medal (multiple select)

### Step 5: Build the Dashboard
1. New Dashboard → size: Automatic
2. Drag charts 1–8 into layout
3. Add KPI text tiles: Total Gold, Silver, Bronze, Total Medals, Athletes, Nations
4. Add filter actions: clicking a country on the map filters all other charts
5. Format: dark background `#0a1628`, gold text `#FFD700`

### Step 6: Build the Story (7 scenes)
1. New Story
2. Scene 1 — drag "Medals Over Time" sheet → title: "Evolution of the Olympic Games"
3. Scene 2 — drag "Top 10 Countries" → title: "Top Performing Countries"
4. Scene 3 — drag "Medal Map" → title: "Medal Distribution"
5. Scene 4 — drag "Gender Participation" → title: "Growth of Women's Participation"
6. Scene 5 — drag "Sports Medals" → title: "Most Successful Sports"
7. Scene 6 — drag "Athlete Trends" → title: "Historical Performance Trends"
8. Scene 7 — drag Dashboard → title: "Key Findings and Conclusion"

### Step 7: Publish to Tableau Public
1. **File → Save to Tableau Public** (or sign in to Tableau Public)
2. Enter workbook name: `OlympicsAnalytics`
3. After publishing, copy the URL from the browser
4. Set `TABLEAU_DASHBOARD_URL` and `TABLEAU_STORY_URL` in `.env`

---

## Final Demo Checklist

### ✅ Website
- [ ] Home page loads with hero, stats, charts
- [ ] Navigation links all work (Home, Dashboard, Story, Insights, About)
- [ ] Footer links work
- [ ] Responsive on mobile (375px), tablet (768px), desktop (1440px)
- [ ] Counter animations trigger on scroll
- [ ] No broken images or 404 routes

### ✅ Data
- [ ] `data/olympics.csv` exists
- [ ] `data/stats.json` exists
- [ ] `/api/stats` returns valid JSON
- [ ] Chart.js charts render on Dashboard and Home pages

### ✅ Tableau
- [ ] Dashboard URL set in `.env` / `app.py`
- [ ] Story URL set in `.env` / `app.py`
- [ ] Tableau dashboard loads in Dashboard page
- [ ] Tableau story loads in Story page
- [ ] If URLs not set, placeholder shown with instructions

### ✅ Deployment
- [ ] `requirements.txt` complete
- [ ] `Procfile` present
- [ ] Environment variables set on Render
- [ ] Build command runs `prepare_data.py`
- [ ] App live on Render URL

---

## Technologies Used

| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.11+ | Runtime |
| Flask | 3.0.3 | Web framework |
| Pandas | 2.2.2 | Data processing |
| NumPy | 1.26.4 | Numerical operations |
| Gunicorn | 22.0.0 | WSGI production server |
| Bootstrap | 5.3.3 | CSS framework |
| Chart.js | 4.4.3 | Built-in charts |
| Bootstrap Icons | 1.11.3 | Icon library |
| Tableau | Public / Desktop | BI dashboards |
| Tableau Embedding API | v3 | Dashboard embed |

---

*OlympicsAnalytics — Built with Python Flask & Tableau*
