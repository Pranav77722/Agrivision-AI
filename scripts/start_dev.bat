@echo off
REM Agrivision AI+ — Development Start Script (Windows)
echo ============================================
echo   Agrivision AI+ Development Environment
echo ============================================
echo.

REM Check if .env exists
if not exist ".env" (
    echo [WARNING] .env file not found. Copying from .env.example...
    copy .env.example .env
    echo Please edit .env with your configuration.
    echo.
)

echo Starting Backend Server...
start "Agrivision Backend" cmd /k "cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo Starting Mobile App (Expo)...
start "Agrivision Mobile" cmd /k "cd mobile && npx expo start"

echo.
echo ============================================
echo   Backend: http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo   Mobile:  Expo DevTools
echo ============================================
