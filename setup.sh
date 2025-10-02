#!/bin/bash

# NLP Word Analyzer - Quick Start Script

echo "🚀 NLP Word Analyzer - Quick Start"
echo "=================================="

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Setup Backend
echo "🐍 Setting up Backend (Python Flask + NLTK)..."
cd backend
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Backend dependencies installed successfully"
else
    echo "❌ Failed to install backend dependencies"
    exit 1
fi

# Setup Frontend
echo ""
echo "🌐 Setting up Frontend (Vue.js + Vuetify)..."
cd ../frontend
echo "📦 Installing Node.js dependencies..."
npm install

if [ $? -eq 0 ]; then
    echo "✅ Frontend dependencies installed successfully"
else
    echo "❌ Failed to install frontend dependencies"
    exit 1
fi

cd ..

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "To start the application:"
echo "1. Backend:  cd backend && python app.py"
echo "2. Frontend: cd frontend && npm run serve"
echo ""
echo "Then visit: http://localhost:8080"