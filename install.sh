#!/bin/bash

# LLM-Based Cybercrime Case Classification - Installation Script
# This script automates the setup process for Unix-like systems

echo "🚀 Setting up LLM-Based Cybercrime Case Classification..."

# Check if Python 3.12+ is available
if ! command -v python3.12 &> /dev/null; then
    echo "❌ Python 3.12+ is required but not found."
    echo "Please install Python 3.12+ and try again."
    exit 1
fi

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "❌ Git is required but not found."
    echo "Please install Git and try again."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3.12 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env file template
if [ ! -f .env ]; then
    echo "🔑 Creating .env file template..."
    echo "# Add your Anthropic API key here" > .env
    echo "ANTHROPIC_API_KEY=your_api_key_here" >> .env
    echo "⚠️  Please edit .env file and add your actual API key"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your Anthropic API key"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run: python semi_automated_classification.py"
echo ""
echo "For detailed instructions, see README.md"
