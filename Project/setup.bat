@echo off
REM Phone Recommendation AI - Quick Setup Script

echo.
echo ========================================
echo  PHONE RECOMMENDATION AI - SETUP
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed!
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo Python found!
echo.

echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo  SETUP COMPLETE!
echo ========================================
echo.
echo Available commands:
echo.
echo 1. Start Backend API:
echo    python app.py
echo    (Then open index.html in browser)
echo.
echo 2. Command-line tools:
echo    python interactive.py                    (Budget search)
echo    python ecommerce_search.py               (Platform search)
echo    python phone_analyzer.py                 (Spec analyzer)
echo    python user_profile_recommender.py       (Profile-based)
echo.
echo 3. View demos:
echo    python profile_demo.py
echo    python analyzer_demo.py
echo    python ecommerce_demo.py
echo.
echo ========================================
echo.
pause
