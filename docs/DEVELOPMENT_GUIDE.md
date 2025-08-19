# Development Guide - flask-datta-able-base

## Quick Start

### Prerequisites
- **Python 3.8+** (recommended: 3.10+)
- **Node.js and npm** (for Sass/Bootstrap build pipeline)
- **pip** package manager
- **Git** for version control

### 1. Clone and Setup
```bash
git clone <repository-url>
cd flask-datta-able-base

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies for Sass/Bootstrap
npm install
```

### 2. Build SCSS
```bash
# Development mode (with watch)
npm run build-css

# Production mode (minified)
npm run build-css-prod
```

### 3. Environment Configuration
Create `.env` file in project root (optional):
```env
# Basic Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=true

# Database Configuration
DATABASE_URL=sqlite:///instance/app.db

# Add your environment variables here
# API_KEY=your-api-key
```

### 4. Run Development Server
```bash
# Option 1: Direct Python (recommended for development)
python app.py

# Option 2: Using run script
./run.sh

# Option 3: Using gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 5. Access Application
- **Web Interface**: http://localhost:5000
- **API Base**: http://localhost:5000/api

## Project Structure

```
flask-datta-able-base/
├── app.py                    # Main Flask application
├── models.py                 # Database models (SQLAlchemy)
├── setup.sh                  # Project setup script
├── run.sh                    # Development server script
├── requirements.txt          # Python dependencies
├── package.json              # Node.js dependencies (Bootstrap, Sass)
├── static/                   # Frontend assets
│   ├── scss/                # SCSS source files
│   │   ├── main.scss        # Main SCSS file
│   │   └── components/      # Component styles
│   ├── css/                 # Generated CSS files
│   └── js/                  # Custom JavaScript files
├── templates/               # Jinja2 templates
│   ├── admin/               # Admin dashboard templates
│   │   ├── base.html       # Admin base template
│   │   └── dashboard.html  # Admin dashboard
│   └── auth/                # Authentication templates
├── docs/                   # Documentation
├── tests/                  # Test files
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── uploads/                # File upload directory
├── instance/               # Instance-specific files (database)
└── venv/                   # Virtual environment
```

## Development Workflow

### 1. **Daily Development**
```bash
# Terminal 1: Start SCSS build with watch mode
npm run build-css

# Terminal 2: Start Flask development server
python app.py

# Now you can:
# - Edit templates in templates/admin/ or templates/auth/
# - Edit styles in static/scss/main.scss
# - Edit Python code in app.py, models.py or other modules
# - Changes auto-reload in development mode
```

### 2. **Feature Development**
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes...

# Run tests (if you have them)
python -m pytest tests/

# Commit changes
git add .
git commit -m "Add: your feature description"
```

### 3. **Testing**
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/unit/test_your_feature.py

# Run with coverage
python -m pytest --cov=. tests/
```

## Key Development Patterns

### 1. **Adding New Routes**
```python
# Add to app.py
@app.route('/your-endpoint')
def your_view():
    return render_template('your_template.html')

# Or create route modules for larger apps
# app/routes/your_blueprint.py
from flask import Blueprint, render_template

your_bp = Blueprint('your_feature', __name__)

@your_bp.route('/your-endpoint')
def your_view():
    return render_template('your_template.html')

# Register in app.py
app.register_blueprint(your_bp, url_prefix='/api')
```

### 2. **Adding New Templates**
```html
<!-- templates/your_page.html -->
{% extends "base.html" %}

{% block title %}Your Page Title{% endblock %}

{% block content %}
<div class="container-fluid">
    <h1 class="h3 mb-4">Your Content Here</h1>
    
    <!-- HTMX Example -->
    <button hx-get="/api/data" 
            hx-target="#results"
            class="btn btn-primary">
        Load Data
    </button>
    
    <div id="results"></div>
</div>
{% endblock %}
```

### 3. **Database Integration (Optional)**
```python
# If you need database functionality
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
db.init_app(app)

# Define models
class YourModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        }

# Create tables
with app.app_context():
    db.create_all()
```

### 4. **API Development**
```python
# RESTful API endpoints
@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify({'items': []})

@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    # Process data
    return jsonify({'message': 'Created'}), 201

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    # Get specific item
    return jsonify({'item': {}})
```

### 5. **Frontend Components (HTMX + Bootstrap)**
```html
<!-- Interactive component with HTMX -->
<div class="card">
    <div class="card-header">
        <h5 class="card-title">Data Table Example</h5>
    </div>
    <div class="card-body">
        <button hx-get="/api/users" 
                hx-target="#user-table"
                hx-indicator="#loading"
                class="btn btn-primary mb-3">
            Load Users
        </button>
        
        <div id="loading" class="htmx-indicator">
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
        
        <div id="user-table"></div>
    </div>
</div>
```

## Customization

### 1. **Styling with Bootstrap SCSS**
```scss
/* static/scss/main.scss */
@import "../../node_modules/bootstrap/scss/functions";
@import "../../node_modules/bootstrap/scss/variables";

// Custom variables
$primary: #04a9f5;
$secondary: #6c757d;
$success: #2ed8b6;

@import "../../node_modules/bootstrap/scss/bootstrap";

/* Your custom styles */
.sidebar {
  background: linear-gradient(135deg, $primary 0%, darken($primary, 10%) 100%);
}
```

### 2. **Sass Configuration**
```json
// package.json scripts
{
  "scripts": {
    "build-css": "sass --watch static/scss/main.scss:static/css/main.css",
    "build-css-prod": "sass --no-source-map --style=compressed static/scss/main.scss:static/css/main.css"
  }
}
```

### 3. **Environment-Based Configuration**
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///app.db')

app.config.from_object(Config)
```

## Production Deployment

### 1. **Prepare for Production**
```bash
# Build production SCSS
npm run build-css-prod

# Set environment variables
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key

# Install production server
pip install gunicorn
```

### 2. **Run with Gunicorn**
```bash
# Basic production server
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# With additional configuration
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 --keepalive 5 app:app
```

### 3. **Using Process Managers**
```bash
# Using systemd, supervisor, or PM2
# Create service files as needed for your deployment environment
```

## VS Code Integration

This project includes VS Code configuration:

### Recommended Extensions
- Python
- Live Sass
- Auto Rename Tag
- HTML CSS Support
- Path Intellisense

### Debug Configuration
Press `F5` to start debugging with the included launch configuration.

## Testing Strategy

### 1. **Unit Tests**
```python
# tests/unit/test_app.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage(client):
    rv = client.get('/')
    assert b'flask-datta-able-base' in rv.data
```

### 2. **Integration Tests**
```python
# tests/integration/test_api.py
def test_api_endpoint(client):
    rv = client.get('/api/hello')
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'message' in data
```

## Common Tasks

### Adding a New Page
1. Create template in `templates/`
2. Add route in `app.py`
3. Update navigation in `base.html` if needed
4. Add any needed CSS classes

### Adding API Endpoints
1. Define route with appropriate HTTP method
2. Add request validation
3. Implement business logic
4. Return appropriate JSON responses
5. Write tests

### Styling Updates
1. Edit `static/scss/main.scss`
2. Use Bootstrap utility classes in templates
3. Rebuild SCSS with `npm run build-css`

## Troubleshooting

### Common Issues
- **SCSS not updating**: Make sure `npm run build-css` is running
- **Import errors**: Check virtual environment activation
- **Port already in use**: Change port in `app.py` or kill existing process
- **Template not found**: Check template path and filename
- **Database errors**: Ensure instance directory exists and database is initialized

### Debug Mode
```python
# Enable debug mode for detailed error messages
app.run(debug=True, port=5000)
```

---

*flask-datta-able-base - Start building admin dashboards immediately with modern web technologies*