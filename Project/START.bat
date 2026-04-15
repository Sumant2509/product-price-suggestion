@echo off
REM Phone Recommendation AI - Full System Launcher
REM Starts Backend API + Opens Frontend in Browser

cls
echo.
echo ========================================================================
echo                    PHONE RECOMMENDATION AI
echo                    Complete System Launcher
echo ========================================================================
echo.
echo Checking system requirements...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not installed!
    echo Please install Python 3.8+ from python.org
    echo.
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check dependencies
echo Verifying dependencies...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Flask not installed
    echo Installing dependencies...
    pip install -r backend\requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

echo [OK] All dependencies ready
echo.

REM Check frontend file
if not exist frontend\index.html (
    echo [ERROR] frontend\index.html not found!
    echo Please ensure index.html is in the frontend directory
    pause
    exit /b 1
)

echo [OK] Frontend found
echo.

echo ========================================================================
echo.
echo                    STARTING SYSTEM COMPONENTS
echo.
echo ========================================================================
echo.
echo [1/2] Starting Backend API Server on port 5000...
echo       (This window will show server logs)
echo.
echo [2/2] Opening Frontend in your browser...
echo.
echo Note: Both will start automatically. To stop, close this window.
echo.
pause

REM Start backend
python launcher.py

pause
