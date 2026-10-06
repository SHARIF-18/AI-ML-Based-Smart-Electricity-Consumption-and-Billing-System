#!/bin/bash

echo "=================================="
echo "Smart Electricity System"
echo "Starting application..."
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip is not installed."
    echo "Please install pip."
    exit 1
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --break-system-packages -r requirements.txt

# Create necessary directories
echo ""
echo "Creating directories..."
mkdir -p data/reports
mkdir -p static/images/profiles

# Run the application
echo ""
echo "=================================="
echo "Starting Flask server..."
echo "Access the application at:"
echo "http://localhost:5000"
echo "=================================="
echo ""

python3 app.py
