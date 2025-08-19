# Flask Base Project - Detailed Documentation

A modern Flask web application template designed for rapid prototyping, proof-of-concepts, and full-scale web application development. This project combines Flask's simplicity with modern frontend technologies to provide a robust foundation for web projects.

## Overview

Flask Base Project is a production-ready template that eliminates the setup overhead typically associated with starting new web projects. It provides a carefully curated stack of modern technologies with sensible defaults, comprehensive documentation, and automated tooling.

## Features

### 🚀 **Modern Technology Stack**
- **Flask**: Python web framework with application factory pattern
- **HTMX**: Dynamic HTML updates without complex JavaScript
- **Alpine.js**: Lightweight JavaScript framework for reactivity
- **Tailwind CSS**: Utility-first CSS framework with build pipeline
- **VS Code Integration**: Complete development environment setup

### 🛠 **Development Ready**
- Auto-reloading development server
- CSS build pipeline with watch mode
- Debugging configurations
- Automated setup scripts
- Comprehensive documentation

### 📦 **Production Ready**
- Environment-based configuration
- Production deployment guides
- Security best practices
- Performance optimization
- Health check endpoints

## Project Structure

```
flask_base_project/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── package.json                # Node.js dependencies
├── tailwind.config.js          # Tailwind CSS configuration
├── setup.sh                    # Project setup script
├── run.sh                      # Development server script
├── static/
│   ├── css/
│   │   ├── input.css          # Tailwind CSS source
│   │   └── output.css         # Generated CSS
│   └── js/                    # Custom JavaScript files
├── templates/
│   ├── base.html             # Base template
│   ├── index.html            # Homepage template
│   └── dashboard.html        # Example page
├── docs/                     # Documentation
│   ├── README.md             # This file
│   ├── DEVELOPMENT_GUIDE.md  # Development workflows
│   ├── DEPLOYMENT.md         # Production deployment
│   ├── TROUBLESHOOTING.md    # Issue resolution
│   ├── PROJECT_OVERVIEW.md   # Business context
│   └── GUIDELINES.md         # Development standards
├── uploads/                  # File upload directory
├── instance/                 # Instance-specific files
├── tests/                    # Test files
└── flask_base_project.code-workspace  # VS Code workspace
```

## Quick Start

### Automated Setup (Recommended)
```bash
# 1. Clone or download the project
git clone <repository-url>
cd flask_base_project

# 2. Run automated setup
./setup.sh

# 3. Start development server
./run.sh
```

### Manual Setup
```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Node.js dependencies
npm install

# 4. Build CSS
npm run build-css-prod

# 5. Run application
python app.py
```

Visit `http://localhost:5000` to see your application.

## Development Workflow

### Daily Development
```bash
# Terminal 1: Start CSS build with watch mode
npm run build-css

# Terminal 2: Start Flask development server
./run.sh
# or
python app.py
```

### Key Commands
```bash
# CSS build (development with watch)
npm run build-css

# CSS build (production minified)
npm run build-css-prod

# Run development server
python app.py

# Run with specific port
python app.py --port 5001
```

## Technology Integration

### Flask Backend
- Application factory pattern for scalability
- Environment-based configuration
- RESTful API design patterns
- Service layer architecture

### Frontend Technologies
- **HTMX**: Server-side rendered dynamic content
- **Alpine.js**: Reactive components without build complexity
- **Tailwind CSS**: Utility-first styling with customization

### Development Environment
- **VS Code Integration**: Debugging, extensions, tasks
- **Automated Scripts**: Setup, development server, CSS build
- **Hot Reloading**: Templates and Python code auto-reload

## Customization

### Adding New Pages
1. Create template in `templates/`
2. Add route in `app.py`
3. Update navigation in `base.html`

### Database Integration (Optional)
```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy()
db.init_app(app)
```

### API Development
```python
@app.route('/api/items', methods=['GET', 'POST'])
def api_items():
    if request.method == 'GET':
        return jsonify({'items': []})
    # Handle POST request
    return jsonify({'message': 'Created'}), 201
```

### Custom Styling
```css
/* static/css/input.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {
  .btn-primary {
    @apply bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded;
  }
}
```

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive production deployment guides including:
- Docker deployment
- Traditional server setup
- Cloud platform deployment
- Security configuration
- Performance optimization

## Testing

```bash
# Run tests (when test files are created)
python -m pytest tests/

# Test with coverage
python -m pytest --cov=. tests/
```

## VS Code Integration

This project includes complete VS Code configuration:

### Recommended Extensions
- Python
- Live Sass Compiler
- Auto Rename Tag
- HTML CSS Support

### Debug Configuration
Press `F5` to start debugging with the included launch configuration.

## Common Use Cases

### Rapid Prototyping
- MVP development
- Client demos
- Concept validation

### Internal Tools
- Admin dashboards
- Business applications
- Data visualization tools

### API Development
- RESTful services
- Microservices
- Integration platforms

### Learning Projects
- Modern web development
- Full-stack applications
- Production deployment

## Support

### Documentation
- [DEVELOPMENT_GUIDE.md](DEVELOPMENT_GUIDE.md) - Detailed development patterns
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions
- [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) - Business context and use cases

### Quick Health Check
```python
# Run health_check.py for diagnostic information
python health_check.py  # (Create this from TROUBLESHOOTING.md)
```

## License

This template is designed to be freely used as a starting point for your projects. Customize it according to your needs and licensing requirements.

---

*Flask Base Project - Your foundation for modern web development*