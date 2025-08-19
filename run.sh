#!/bin/bash

# flask-datta-able-base Project Run Script
# This script runs the Flask development server using the virtual environment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_error "Virtual environment not found!"
    print_status "Please run ./setup.sh first to set up the project"
    exit 1
fi

# Check if Flask app exists
if [ ! -f "app.py" ]; then
    print_error "app.py not found!"
    exit 1
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Check if Flask is installed
if ! python -c "import flask" 2>/dev/null; then
    print_error "Flask is not installed in the virtual environment!"
    print_status "Please run ./setup.sh to install dependencies"
    exit 1
fi

# Quick health check
print_status "Verifying Flask application..."

# Check if CSS is built
if [ ! -f "static/css/main.css" ]; then
    print_warning "SCSS output not found, building..."
    if [ -f "package.json" ] && command -v npm &> /dev/null; then
        npm run build-css-prod
        print_success "SCSS built successfully"
    else
        print_warning "Cannot build SCSS - creating empty main.css"
        mkdir -p static/css
        touch static/css/main.css
    fi
fi

# Display startup information
echo ""
echo "🚀 Starting Flask development server..."
echo "📍 Application: app.py"
echo "🌐 URL: http://localhost:5000"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Set Flask environment variables
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=1

# Run Flask application
# Check if database exists and initialize if needed
if [ ! -f "instance/app.db" ]; then
    print_warning "Database not found, initializing..."
    mkdir -p instance
    if python init_db.py; then
        print_success "Database initialized successfully"
    else
        print_warning "Database initialization failed"
    fi
fi

print_success "Server starting..."
python app.py