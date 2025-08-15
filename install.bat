@echo off
REM LLM-Based Cybercrime Case Classification - Installation Script for Windows
REM This script automates the setup process for Windows systems

echo 🚀 Setting up LLM-Based Cybercrime Case Classification...

REM Check if Python 3.12+ is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not found.
    echo Please install Python 3.12+ and try again.
    pause
    exit /b 1
)

REM Check if git is available
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is required but not found.
    echo Please install Git and try again.
    pause
    exit /b 1
)

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Create .env file template
if not exist .env (
    echo 🔑 Creating .env file template...
    echo # Add your Anthropic API key here > .env
    echo ANTHROPIC_API_KEY=your_api_key_here >> .env
    echo ⚠️  Please edit .env file and add your actual API key
) else (
    echo ✅ .env file already exists
)

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file and add your Anthropic API key
echo 2. Activate virtual environment: venv\Scripts\activate.bat
echo 3. Run: python semi_automated_classification.py
echo.
echo For detailed instructions, see README.md
pause
