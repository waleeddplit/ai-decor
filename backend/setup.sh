#!/bin/bash

# Art.Decor.AI Backend Setup Script
# Automates virtual environment and dependency installation

echo "🎨 Art.Decor.AI Backend Setup"
echo "=============================="
echo

# Check Python version
echo "📌 Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.10+ first."
    exit 1
fi

# Create virtual environment
echo
echo "📦 Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment."
    exit 1
fi

echo "✅ Virtual environment created"

# Activate virtual environment
echo
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo
echo "📥 Installing dependencies..."
echo "   This may take a few minutes..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies."
    exit 1
fi

echo "✅ Dependencies installed"

# Create necessary directories
echo
echo "📁 Creating directories..."
mkdir -p data models uploads temp logs

echo "✅ Directories created"

# Copy environment file if it doesn't exist
echo
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your API keys and configuration"
else
    echo "✅ .env file already exists"
fi

# Summary
echo
echo "=============================="
echo "✨ Setup Complete!"
echo "=============================="
echo
echo "Next steps:"
echo "1. Edit .env with your API keys"
echo "2. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo "3. Run the development server:"
echo "   uvicorn main:app --reload"
echo
echo "API will be available at: http://localhost:8000"
echo "Documentation: http://localhost:8000/docs"
echo

