from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask_bcrypt import Bcrypt
from datetime import datetime
import os
from functools import wraps
from config import config, get_env, get_config

app = Flask(__name__)

# Load configuration from both .env and config.yaml
app.config.update(config.to_flask_config())

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = config.get_env('DATABASE_URL', 'sqlite:///datta_able.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = config.get_env('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt(app)

# Import models and initialize database reference
from models import init_db, create_default_data
User, ActivityLog, Setting = init_db(db)

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))

# Create uploads directory if it doesn't exist
upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')
os.makedirs(upload_folder, exist_ok=True)

# Create database tables
with app.app_context():
    db.create_all()
    create_default_data()

# Template globals - make config functions available in templates
@app.template_global()
def get_env_var(key, default=None):
    """Template helper to get environment variables"""
    return get_env(key, default)

@app.template_global() 
def get_app_config(path, default=None):
    """Template helper to get application config values"""
    return get_config(path, default)

@app.template_global()
def current_year():
    """Template helper to get current year"""
    return datetime.now().year

# Custom decorator for optional authentication
def optional_auth_required(f):
    """
    Decorator that checks if authentication should be bypassed.
    If DISABLE_AUTH is True in environment, skips authentication.
    Otherwise, requires login as normal.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if auth is disabled in development
        disable_auth = get_env('DISABLE_AUTH', 'false').lower() == 'true'
        
        if disable_auth:
            # If auth is disabled, create a mock admin user for the session
            # This allows pages to work without breaking
            if not current_user.is_authenticated:
                # You can either redirect to login or create a mock user session
                # For maximum compatibility, we'll redirect with a warning
                flash('⚠️ DEVELOPMENT MODE: Authentication disabled!', 'warning')
                # Let the request continue - the template will handle missing current_user gracefully
            return f(*args, **kwargs)
        else:
            # Normal authentication required
            return login_required(f)(*args, **kwargs)
    
    return decorated_function

# Routes
@app.route('/')
def index():
    """Main landing page showcasing the flask-datta-able-base."""
    # Check if auth is disabled in development
    disable_auth = get_env('DISABLE_AUTH', 'false').lower() == 'true'
    
    if current_user.is_authenticated or disable_auth:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
@optional_auth_required
def dashboard():
    """Admin dashboard"""
    # Get stats for dashboard
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    admin_users = User.query.filter_by(is_admin=True).count()
    recent_activities = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_users=total_users,
                         active_users=active_users,
                         admin_users=admin_users,
                         recent_activities=recent_activities)

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me') == 'on'
        
        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('auth/login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact an administrator.', 'error')
                return render_template('auth/login.html')
            
            login_user(user, remember=remember_me)
            user.last_login = datetime.utcnow()
            
            # Log activity
            activity = ActivityLog(
                user_id=user.id,
                action='login',
                description=f'User {user.username} logged in',
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent')
            )
            db.session.add(activity)
            db.session.commit()
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('auth/login.html')

@app.route('/logout')
@optional_auth_required
def logout():
    """User logout"""
    # Log activity
    activity = ActivityLog(
        user_id=current_user.id,
        action='logout',
        description=f'User {current_user.username} logged out',
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )
    db.session.add(activity)
    db.session.commit()
    
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    # Check if registration is enabled
    if not Setting.get_setting('user_registration', True):
        flash('User registration is currently disabled.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not all([username, email, first_name, last_name, password, confirm_password]):
            flash('All fields are required.', 'error')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('auth/register.html')
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
            return render_template('auth/register.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            is_admin=False
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Log activity
        activity = ActivityLog(
            user_id=user.id,
            action='register',
            description=f'User {user.username} registered',
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(activity)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html')

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": config.get('app.version', '1.0.0'),
        "app_name": config.get('app.name', 'flask-datta-able-base'),
        "environment": config.get_env('FLASK_ENV', 'development'),
        "features": {
            "file_uploads": config.get('app.features.file_uploads', True),
            "api_enabled": config.get('app.features.api_enabled', True),
            "health_check": config.get('app.features.health_check', True)
        }
    })

@app.route('/api/hello', methods=['GET', 'POST'])
def hello():
    """Simple API endpoint for testing HTMX functionality."""
    if request.method == 'POST':
        name = request.form.get('name', 'World')
        return f'<p class="text-success fw-bold">Hello, {name}! 👋</p>'
    return jsonify({'message': 'Hello from flask-datta-able-base!'})

@app.route('/api/llm-status')
def llm_status():
    """Check LLM API configuration and availability."""
    from llm_utils import check_llm_setup
    
    try:
        setup_info = check_llm_setup()
        return jsonify({
            'status': 'success',
            'llm_setup': setup_info,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# Admin routes for sidebar navigation
@app.route('/users')
@optional_auth_required
def users():
    """User management page"""
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('admin/users.html', users=users)

@app.route('/buttons')
@login_required  
def buttons():
    """Buttons demo page"""
    return render_template('admin/buttons.html')

@app.route('/cards')
@login_required
def cards():
    """Cards demo page"""
    return render_template('admin/cards.html')

@app.route('/colors')
@login_required
def colors():
    """Colors demo page"""
    return render_template('admin/colors.html')

@app.route('/borders')
@login_required
def borders():
    """Borders demo page"""
    return render_template('admin/borders.html')

@app.route('/animations')
@login_required
def animations():
    """Animations demo page"""
    return render_template('admin/animations.html')

@app.route('/other')
@login_required
def other():
    """Other utilities demo page"""
    return render_template('admin/other.html')

@app.route('/tables')
@login_required
def tables():
    """Tables demo page"""
    return render_template('admin/tables.html')

@app.route('/charts')
@login_required
def charts():
    """Charts demo page"""
    return render_template('admin/charts.html')

# User management CRUD operations
@app.route('/users/create', methods=['GET', 'POST'])
@optional_auth_required
def create_user():
    """Create new user"""
    # Check admin privileges (skip if auth is disabled)
    disable_auth = get_env('DISABLE_AUTH', 'false').lower() == 'true'
    if not disable_auth and not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        is_admin = request.form.get('is_admin') == 'on'
        is_active = request.form.get('is_active') == 'on'
        
        # Validation
        if not all([username, email, first_name, last_name, password]):
            flash('All fields are required.', 'error')
            return render_template('admin/user_form.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return render_template('admin/user_form.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'error')
            return render_template('admin/user_form.html')
        
        # Create user
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin,
            is_active=is_active
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'User {username} created successfully.', 'success')
        return redirect(url_for('users'))
    
    return render_template('admin/user_form.html', user=None)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@optional_auth_required
def edit_user(user_id):
    """Edit user"""
    # Check admin privileges (skip if auth is disabled)
    disable_auth = get_env('DISABLE_AUTH', 'false').lower() == 'true'
    if not disable_auth and not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form.get('username', user.username)
        user.email = request.form.get('email', user.email)
        user.first_name = request.form.get('first_name', user.first_name)
        user.last_name = request.form.get('last_name', user.last_name)
        user.is_admin = request.form.get('is_admin') == 'on'
        user.is_active = request.form.get('is_active') == 'on'
        
        # Update password if provided
        password = request.form.get('password')
        if password:
            user.set_password(password)
        
        user.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash(f'User {user.username} updated successfully.', 'success')
        return redirect(url_for('users'))
    
    return render_template('admin/user_form.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
@optional_auth_required
def delete_user(user_id):
    """Delete user"""
    # Check admin privileges (skip if auth is disabled)
    disable_auth = get_env('DISABLE_AUTH', 'false').lower() == 'true'
    if not disable_auth and not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    
    # Prevent self-deletion (skip check if auth is disabled)
    disable_auth = get_env('DISABLE_AUTH', 'false').lower() == 'true'
    if not disable_auth and current_user.is_authenticated and user.id == current_user.id:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('users'))
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {username} deleted successfully.', 'success')
    return redirect(url_for('users'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)