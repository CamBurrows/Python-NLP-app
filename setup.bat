@echo off
REM NLP Word Analyzer - Quick Start Script for Windows

echo 🚀 NLP Word Analyzer - Quick Start
echo ==================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ first.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed
echo.

REM Setup Backend
echo 🐍 Setting up Backend (Python Flask + NLTK)...
cd backend
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install backend dependencies
    pause
    exit /b 1
)

echo ✅ Backend dependencies installed successfully

REM Setup Frontend
echo.
echo 🌐 Setting up Frontend (Vue.js + Vuetify)...
cd ..\frontend
echo 📦 Installing Node.js dependencies...
npm install --legacy-peer-deps

if errorlevel 1 (
    echo ❌ Failed to install frontend dependencies
    pause
    exit /b 1
)

echo ✅ Frontend dependencies installed successfully

cd ..

echo.
echo 🎉 Setup Complete!
echo.
echo To start the application:
echo 1. Backend:  cd backend ^&^& python app.py
echo 2. Frontend: cd frontend ^&^& npm run serve
echo.
echo Then visit: http://localhost:8080

pause