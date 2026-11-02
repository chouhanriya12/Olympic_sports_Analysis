@echo off
echo ============================================
echo  OlympicsAnalytics - Quick Start (Windows)
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet

REM Prepare data
if not exist "data\stats.json" (
    echo Preparing Olympic dataset...
    python data\prepare_data.py
)

REM Copy .env if needed
if not exist ".env" (
    copy .env.example .env
    echo.
    echo NOTE: .env created from .env.example
    echo       Edit .env to add your Tableau URLs and SECRET_KEY
    echo.
)

REM Start Flask
echo.
echo Starting OlympicsAnalytics on http://localhost:5000
echo Press Ctrl+C to stop.
echo.
python app.py
