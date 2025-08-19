#!/bin/bash

# flask-datta-able-base Project Setup Script
# This script sets up the development environment

set -e  # Exit on any error

echo "🚀 Setting up flask-datta-able-base project..."

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

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

print_success "Python 3 found: $(python3 --version)"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js first."
    exit 1
fi

print_success "Node.js found: $(node --version)"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed. Please install npm first."
    exit 1
fi

print_success "npm found: $(npm --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install Python requirements
if [ -f "requirements.txt" ]; then
    print_status "Installing Python dependencies from requirements.txt..."
    pip install -r requirements.txt
    print_success "Python dependencies installed"
else
    print_error "requirements.txt not found!"
    exit 1
fi

# Install Node.js dependencies
if [ -f "package.json" ]; then
    print_status "Installing Node.js dependencies..."
    npm install
    print_success "Node.js dependencies installed"
else
    print_error "package.json not found!"
    exit 1
fi

# Build SCSS
print_status "Building SCSS..."
npm run build-css-prod
print_success "SCSS built successfully"

# Create main.css if it doesn't exist (fallback)
if [ ! -f "static/css/main.css" ]; then
    print_warning "main.css not found, creating empty file..."
    mkdir -p static/css
    touch static/css/main.css
fi

# Check if all required files exist
print_status "Verifying project structure..."

required_files=("app.py" "models.py" "templates/admin/base.html" "static/scss/main.scss")
missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    print_error "Missing required files:"
    for file in "${missing_files[@]}"; do
        echo "  - $file"
    done
    exit 1
fi

print_success "All required files found"

# Initialize database
print_status "Initializing database..."
if python init_db.py; then
    print_success "Database initialized successfully"
else
    print_warning "Database initialization failed or already exists"
fi

# Display setup completion
echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "   1. Activate virtual environment: source venv/bin/activate"
echo "   2. Run the development server: python app.py"
echo "   3. Open your browser to: http://localhost:5000"
echo ""
echo "🔧 Development commands:"
echo "   • Watch CSS changes: npm run build-css"
echo "   • Build production CSS: npm run build-css-prod"
echo "   • Debug in VS Code: Press F5"
echo ""
echo "📁 Project ready at: $(pwd)"