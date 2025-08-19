# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development
```bash
# Start development server
python app.py
# or 
./run.sh

# Kill app running on configured port
./kill_app.sh

# Start production server 
python start.py
# or
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Testing
```bash
# Run test files (add your test files here)
python test_*.py

# Run unit tests (create tests/unit/ directory as needed)
python tests/unit/test_*.py

# Run integration tests (create tests/integration/ directory as needed)
python tests/integration/test_*.py
```

### Deployment
```bash
# Setup deployment environment
./deploy.sh

# Production deployment with reverse proxy
gunicorn -w 4 -b 0.0.0.0:5000 app:app --daemon --pid /var/run/flask_datta_able_base.pid
```

## Architecture Overview

flask-datta-able-base is a modern web application template designed for rapid prototyping and proof-of-concept development. It provides a clean, extensible foundation with modern frontend technologies.

### Core Architecture Pattern
```
Flask App Factory → Services Layer → Database Layer → Frontend (HTMX + Bootstrap + Datta Able)
```

### Project Structure

**Main Application** (`app.py`)
- Flask application factory pattern
- Configurable routing and middleware
- Environment-based configuration

**Static Assets** (`static/`)
- Bootstrap SCSS build pipeline
- JavaScript modules for enhanced interactivity
- Asset optimization for production

**Templates** (`templates/`)
- Jinja2 template inheritance
- HTMX integration patterns
- Alpine.js component structure

### Route Structure
- `/` - Main application routes
- `/api/*` - REST API endpoints
- `/static/*` - Static asset serving

## Product Management Approach

### Feature Development Process

When implementing any new feature, Claude Code should act as a hands-on product manager and follow this collaborative process:

#### 1. Requirements Discovery
Before writing any code, ask clarifying questions to understand:
- **User Goals**: What problem are we solving?
- **Success Criteria**: How will we know this feature works well?
- **Scope Boundaries**: What's included and what's not?
- **Technical Constraints**: Any specific requirements or limitations?

#### 2. Feature Planning
Collaborate with the user to:
- **Define Core Functionality**: What are the must-have features?
- **Identify User Flows**: How will users interact with this feature?
- **Determine Data Requirements**: What data needs to be stored/processed?
- **Plan Integration Points**: How does this connect to existing features?

#### 3. Implementation Confirmation
Before coding, present a clear plan including:
- **Feature Specification**: Detailed description of what will be built
- **Technical Approach**: High-level implementation strategy
- **File Structure**: Which files will be created/modified
- **Testing Strategy**: How the feature will be validated

#### 4. Iterative Development
During implementation:
- **Regular Check-ins**: Confirm direction at key milestones
- **Show Progress**: Demonstrate working features as they're built
- **Gather Feedback**: Adjust based on user input
- **Document Decisions**: Keep track of choices made and why

### Example Interaction Pattern

**User Request**: "Add user authentication to the app"

**Product Manager Response**: 
1. "I'd like to understand your authentication needs better. Are you looking for:
   - Simple email/password login?
   - Social login (Google, GitHub, etc.)?
   - Role-based access control?
   - Session management preferences?"

2. After discussion: "Based on our conversation, I'll implement email/password authentication with session management. This will include:
   - User registration/login forms
   - Password hashing and validation
   - Session management
   - Protected route decorators
   - Basic user profile management
   
   Does this align with your vision?"

3. Upon confirmation: Proceed with implementation using TodoWrite tool for tracking progress.

### Key Principles
- **User-Centric**: Always start with user needs, not technical solutions
- **Collaborative**: Treat the user as a product partner, not just a client
- **Iterative**: Build in small, testable increments
- **Transparent**: Clearly communicate what's being built and why
- **Flexible**: Be ready to adjust based on feedback and new insights

## Development Patterns

### Service Initialization Pattern
Services should be initialized in Flask app factory with dependency injection:
```python
# Example service initialization
service.init_app(app)
```

### Configuration Management
Environment-based configuration with fallbacks:
```python
app.config['SETTING'] = os.getenv('SETTING', 'default_value')
```

### Frontend Integration Pattern
- HTMX for dynamic content updates
- Bootstrap 5 for responsive UI components
- Custom SCSS for Datta Able styling

## Configuration

flask-datta-able-base uses a **hybrid configuration system** combining:
- **`.env` file** for secrets and environment-specific variables 
- **`config.yaml` file** for application settings and non-sensitive configuration

### Quick Setup
```bash
# 1. Copy environment template and customize
cp .env.example .env
nano .env  # Add your secrets and API keys

# 2. Customize application settings
nano config.yaml  # Adjust app settings as needed
```

### Environment Variables (.env)
```bash
# Core Flask settings
SECRET_KEY=your-super-secret-key
FLASK_ENV=development
FLASK_DEBUG=true

# Database (if using)
DATABASE_URL=sqlite:///app.db

# External APIs (examples)
# OPENAI_API_KEY=sk-...
# STRIPE_SECRET_KEY=sk_test_...

# File uploads
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

### Application Settings (config.yaml)
```yaml
app:
  name: "Your App Name"
  version: "1.0.0"
  features:
    file_uploads: true
    api_enabled: true

# Add your custom settings
custom:
  company:
    name: "Your Company"
    support_email: "support@company.com"
```

### Using Configuration in Code
```python
from config import config, get_env, get_config

# Get environment variables
secret_key = get_env('SECRET_KEY')
debug_mode = get_env('FLASK_DEBUG', False, bool)

# Get application settings
app_name = get_config('app.name', 'flask-datta-able-base')
features = get_config('app.features', {})

# Check environment
if config.is_development():
    # Development specific code
    pass
```

### Development vs Production
- **Development**: `python app.py` (debug=True, auto-reload)
- **Production**: `python start.py` or gunicorn (debug=False, stable)

## Git Commit Guidelines
- Keep commit messages professional and focused on the actual changes
- Use standard commit message format: brief summary, then detailed description if needed
- Focus on what was changed and why

## Testing Strategy

### Test Organization
- `tests/unit/` - Individual component testing
- `tests/integration/` - End-to-end workflow testing
- Root-level `test_*.py` - Quick prototype tests

### Test Categories
- **Unit Tests**: Individual function and class testing
- **Integration Tests**: Component interaction testing
- **API Tests**: Endpoint functionality verification

## Frontend Architecture

### Template Structure
- **Base Template** (`templates/base.html`): Main layout and dependencies
- **Page Templates**: Specific page implementations
- **Component Templates**: Reusable HTMX components

### CSS Build Process
```bash
# Development (with watch mode)
npm run build-css

# Production (minified)
npm run build-css-prod
```

### JavaScript Architecture
- Minimal JavaScript footprint using Alpine.js
- HTMX for most dynamic interactions
- Custom JS only when necessary

## Customization Guidelines

### Adding New Features
1. Create service modules in appropriate directories
2. Add routes following RESTful conventions
3. Update templates using established patterns
4. Add tests for new functionality

### Database Integration
- Use SQLAlchemy for ORM if database is needed
- Follow migration patterns for schema changes
- Implement proper connection management

### API Development
- Follow REST conventions for endpoint design
- Implement proper error handling and status codes
- Add request validation and response formatting

## Deployment Considerations

### Production Checklist
- Set `FLASK_ENV=production`
- Configure proper secret keys
- Set up reverse proxy (nginx recommended)
- Configure logging and monitoring
- Implement backup strategies if using database

This base project is designed to be a starting point that you can rapidly extend for specific use cases while maintaining clean architecture and development practices.