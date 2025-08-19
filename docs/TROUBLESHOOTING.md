# Troubleshooting Guide - Flask Base Project

## Common Issues and Solutions

### 🚀 **Application Startup Issues**

#### Application Won't Start
**Symptoms:**
- `ModuleNotFoundError: No module named 'flask'`
- `ImportError: Cannot import name 'app'`

**Solutions:**
```bash
# 1. Check virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# 4. Verify app.py exists
ls -la app.py
```

#### Port Already in Use
**Symptoms:**
- `OSError: [Errno 98] Address already in use`

**Solutions:**
```bash
# Find process using port 5000
sudo lsof -i :5000
# or
sudo netstat -tulpn | grep :5000

# Kill the process
kill -9 <process_id>

# Or use different port
python app.py  # Will try different port automatically
# or specify port manually in app.py: app.run(port=5001)
```

#### Environment Variable Issues
**Symptoms:**
- Application starts but features not working
- Configuration errors

**Solutions:**
```bash
# 1. Check if .env file exists
ls -la .env

# 2. Verify environment variables are loaded
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('SECRET_KEY:', os.getenv('SECRET_KEY', 'NOT SET'))
"

# 3. Create .env file if missing
echo "SECRET_KEY=dev-secret-key" > .env
echo "FLASK_ENV=development" >> .env
```

---

### 🎨 **Frontend and CSS Issues**

#### CSS Not Loading/Updating
**Symptoms:**
- Styles not applied
- Tailwind classes not working
- Old styles showing

**Solutions:**
```bash
# 1. Check if Tailwind build is running
npm run build-css

# 2. Verify output.css is being generated
ls -la static/css/output.css

# 3. For production, rebuild CSS
npm run build-css-prod

# 4. Clear browser cache
# Ctrl+F5 or Cmd+Shift+R

# 5. Check if Node.js and npm are installed
node --version
npm --version
```

#### JavaScript Errors
**Symptoms:**
- Browser console errors
- HTMX not working
- Alpine.js components not interactive

**Solutions:**
```javascript
// 1. Check browser console for specific errors (F12)

// 2. Verify HTMX is loaded
console.log(window.htmx);

// 3. Verify Alpine.js is loaded
console.log(window.Alpine);

// 4. Common fixes:
// - Check for typos in x-data attributes
// - Ensure proper HTML structure
// - Verify JavaScript syntax
```

#### HTMX Requests Failing
**Symptoms:**
- `415 Unsupported Media Type`
- Dynamic content not updating

**Solutions:**
```python
# 1. Check Flask route accepts correct methods
@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    return jsonify({'status': 'ok'})

# 2. Verify content type handling
from flask import request
if request.content_type == 'application/json':
    data = request.get_json()
```

---

### 🗄️ **Database Issues**

#### Database File Not Found
**Symptoms:**
- `No such file or directory: instance/app.db`
- Database connection errors

**Solutions:**
```bash
# 1. Create instance directory
mkdir -p instance

# 2. Create database tables
python -c "
from app import app
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/app.db'
db = SQLAlchemy()
db.init_app(app)
with app.app_context():
    db.create_all()
    print('Database created successfully')
"
```

#### Database Schema Issues
**Symptoms:**
- `Table doesn't exist`
- Column errors

**Solutions:**
```python
# Recreate database (WARNING: This deletes all data)
from app import app
from flask_sqlalchemy import SQLAlchemy

with app.app_context():
    db.drop_all()  # Remove all tables
    db.create_all()  # Recreate tables
    print("Database schema updated")
```

---

### 📁 **File Upload Issues**

#### File Upload Fails
**Symptoms:**
- `413 Request Entity Too Large`
- Upload button not responding

**Solutions:**
```python
# 1. Check file size limits in app.py
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# 2. Verify upload directory exists
import os
os.makedirs('uploads', exist_ok=True)

# 3. Check file type restrictions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

#### File Processing Errors
**Symptoms:**
- Uploaded files not processed
- Text extraction fails

**Solutions:**
```bash
# 1. Install additional dependencies for file processing
pip install python-docx PyPDF2

# 2. Test file processing manually
python -c "
import os
print('Upload directory exists:', os.path.exists('uploads'))
print('Upload directory contents:', os.listdir('uploads'))
"
```

---

### 🌐 **Development Server Issues**

#### Templates Not Updating
**Symptoms:**
- Changes to HTML templates not showing
- Old template content appearing

**Solutions:**
```python
# 1. Enable template auto-reload in app.py
app.config['TEMPLATES_AUTO_RELOAD'] = True

# 2. Clear browser cache
# 3. Restart Flask development server
```

#### Static Files Not Serving
**Symptoms:**
- CSS/JS files return 404
- Images not loading

**Solutions:**
```python
# 1. Verify static folder structure
# static/
#   scss/
#     main.scss
#     components/
#   css/
#     main.css
#   js/

# 2. Check static URL configuration
from flask import url_for
print(url_for('static', filename='css/main.css'))

# 3. Verify Flask static folder setting
app = Flask(__name__, static_folder='static')
```

---

### 🔧 **Development Environment Issues**

#### Virtual Environment Problems
**Symptoms:**
- Wrong Python version
- Package import errors

**Solutions:**
```bash
# 1. Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Verify virtual environment is active
which python
which pip

# 3. Check Python version
python --version
```

#### Dependency Issues
**Symptoms:**
- `ModuleNotFoundError`
- Version conflicts

**Solutions:**
```bash
# 1. Check installed packages
pip list

# 2. Update requirements.txt
pip freeze > requirements.txt

# 3. Install missing dependencies
pip install flask flask-sqlalchemy

# 4. Check for version conflicts
pip check
```

---

### 🖥️ **VS Code Development Issues**

#### Extensions Not Working
**Symptoms:**
- No Python syntax highlighting
- No Bootstrap/SCSS IntelliSense

**Solutions:**
```bash
# 1. Install recommended extensions
# - Python
# - Live Sass Compiler
# - Auto Rename Tag

# 2. Verify Python interpreter
# Ctrl+Shift+P -> "Python: Select Interpreter"
# Choose venv/bin/python

# 3. Reload VS Code window
# Ctrl+Shift+P -> "Developer: Reload Window"
```

#### Debugging Not Working
**Symptoms:**
- F5 doesn't start debugger
- Breakpoints not hitting

**Solutions:**
```json
// Check .vscode/launch.json exists and is configured correctly
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Flask",
            "type": "python",
            "request": "launch",
            "program": "app.py",
            "env": {
                "FLASK_ENV": "development",
                "FLASK_DEBUG": "1"
            },
            "console": "integratedTerminal"
        }
    ]
}
```

---

### 🚨 **Production Issues**

#### Application Not Starting in Production
**Symptoms:**
- Gunicorn errors
- Service fails to start

**Solutions:**
```bash
# 1. Test gunicorn directly
gunicorn --bind 0.0.0.0:5000 app:app

# 2. Check systemd service logs
sudo journalctl -u flask-base-project -f

# 3. Verify environment variables
sudo -u flaskapp env | grep FLASK

# 4. Check file permissions
ls -la /home/flaskapp/app/
```

#### High Memory Usage
**Symptoms:**
- Server running out of memory
- Application killed by OOM

**Solutions:**
```bash
# 1. Monitor memory usage
htop
free -h

# 2. Optimize gunicorn workers
# In systemd service file or gunicorn command:
--workers 2 --threads 2

# 3. Add swap if needed (temporary fix)
sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

### 🔍 **Debugging Tools and Commands**

#### Application Debugging
```python
# 1. Enable debug mode
export FLASK_DEBUG=1
python app.py

# 2. Add print statements for debugging
print(f"Debug info: {variable}")

# 3. Use Flask's logger
from flask import current_app
current_app.logger.info("Debug message")
```

#### Database Debugging
```python
# 1. Check database connection
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

try:
    db.session.execute('SELECT 1')
    print("Database connection: OK")
except Exception as e:
    print(f"Database error: {e}")

# 2. Inspect database tables
print("Database tables:", db.engine.table_names())
```

#### Network Debugging
```bash
# 1. Check if port is accessible
telnet localhost 5000
curl http://localhost:5000

# 2. Check process listening on port
sudo lsof -i :5000

# 3. Test API endpoints
curl -X GET http://localhost:5000/api/hello
curl -X POST -H "Content-Type: application/json" -d '{"test":"data"}' http://localhost:5000/api/data
```

---

## 📞 **Getting Help**

### Information to Collect Before Reporting Issues
1. **Error message** (full error text)
2. **Steps to reproduce** the issue
3. **Environment details**:
   ```bash
   python --version
   pip list
   uname -a  # Linux/Mac
   systeminfo  # Windows
   ```
4. **Configuration** (remove sensitive data like API keys)
5. **Log output** showing the error

### Useful Commands for Issue Reports
```bash
# System information
python --version
pip list | grep flask
node --version
npm --version

# Application status
python -c "import app; print('App imports successfully')"
python -c "from flask import Flask; print('Flask available')"

# File structure
ls -la
ls -la static/
ls -la templates/
```

---

### Quick Health Check Script
Create `health_check.py` for quick diagnostics:
```python
#!/usr/bin/env python3
import os
import sys

def health_check():
    print("🏥 Flask Base Project Health Check")
    print("=" * 40)
    
    # Check Python version
    print(f"✓ Python version: {sys.version}")
    
    # Check virtual environment
    venv_active = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print(f"{'✓' if venv_active else '✗'} Virtual environment: {'Active' if venv_active else 'Not active'}")
    
    # Check required files
    files_to_check = ['app.py', 'requirements.txt', 'package.json', 'static/css/input.css']
    for file in files_to_check:
        exists = os.path.exists(file)
        print(f"{'✓' if exists else '✗'} {file}: {'Found' if exists else 'Missing'}")
    
    # Check directories
    dirs_to_check = ['static', 'templates', 'uploads', 'instance']
    for dir in dirs_to_check:
        exists = os.path.exists(dir)
        print(f"{'✓' if exists else '✗'} {dir}/: {'Found' if exists else 'Missing'}")
    
    # Try importing Flask
    try:
        import flask
        print(f"✓ Flask: {flask.__version__}")
    except ImportError:
        print("✗ Flask: Not installed")
    
    # Check CSS build
    css_built = os.path.exists('static/css/output.css')
    print(f"{'✓' if css_built else '✗'} CSS built: {'Yes' if css_built else 'Run: npm run build-css'}")

if __name__ == '__main__':
    health_check()
```

Run with: `python health_check.py`

---

*Flask Base Project - Troubleshoot with confidence*