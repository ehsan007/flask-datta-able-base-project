"""
Database models for flask-datta-able-base
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Global database instance - will be set by init_db()
db = None

def init_db(database):
    """Initialize database reference and create model classes"""
    global db, User, ActivityLog, Setting
    db = database
    
    class User(db.Model, UserMixin):
        """User model for authentication"""
        __tablename__ = 'users'
        
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(20), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        first_name = db.Column(db.String(50), nullable=False)
        last_name = db.Column(db.String(50), nullable=False)
        password_hash = db.Column(db.String(128), nullable=False)
        is_active = db.Column(db.Boolean, default=True)
        is_admin = db.Column(db.Boolean, default=False)
        avatar = db.Column(db.String(200), default='https://via.placeholder.com/150')
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        last_login = db.Column(db.DateTime)
        
        def set_password(self, password):
            """Set password hash"""
            self.password_hash = generate_password_hash(password)
        
        def check_password(self, password):
            """Check password against hash"""
            return check_password_hash(self.password_hash, password)
        
        @property
        def full_name(self):
            """Get user's full name"""
            return f"{self.first_name} {self.last_name}"
        
        @property 
        def password(self):
            """Prevent password from being accessed"""
            raise AttributeError('password is not a readable attribute')
            
        @password.setter
        def password(self, password):
            """Set password hash"""
            self.set_password(password)
        
        def to_dict(self):
            """Convert user to dictionary"""
            return {
                'id': self.id,
                'username': self.username,
                'email': self.email,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'full_name': self.full_name,
                'is_active': self.is_active,
                'is_admin': self.is_admin,
                'avatar': self.avatar,
                'created_at': self.created_at.isoformat() if self.created_at else None,
                'last_login': self.last_login.isoformat() if self.last_login else None
            }
        
        def __repr__(self):
            return f'<User {self.username}>'

    class ActivityLog(db.Model):
        """Activity log for tracking user actions"""
        __tablename__ = 'activity_logs'
        
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
        action = db.Column(db.String(100), nullable=False)
        description = db.Column(db.Text)
        ip_address = db.Column(db.String(45))
        user_agent = db.Column(db.Text)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        
        # Relationship
        user = db.relationship('User', backref=db.backref('activity_logs', lazy=True))
        
        def to_dict(self):
            """Convert activity log to dictionary"""
            return {
                'id': self.id,
                'user_id': self.user_id,
                'username': self.user.username if self.user else 'System',
                'action': self.action,
                'description': self.description,
                'ip_address': self.ip_address,
                'user_agent': self.user_agent,
                'created_at': self.created_at.isoformat() if self.created_at else None
            }
        
        def __repr__(self):
            return f'<ActivityLog {self.action}>'

    class Setting(db.Model):
        """Application settings"""
        __tablename__ = 'settings'
        
        id = db.Column(db.Integer, primary_key=True)
        key = db.Column(db.String(100), unique=True, nullable=False)
        value = db.Column(db.Text)
        description = db.Column(db.Text)
        is_public = db.Column(db.Boolean, default=False)  # Whether setting can be viewed by non-admins
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        @staticmethod
        def get_value(key, default=None):
            """Get setting value by key"""
            setting = Setting.query.filter_by(key=key).first()
            return setting.value if setting else default
        
        @staticmethod 
        def set_value(key, value, description=None):
            """Set setting value by key"""
            setting = Setting.query.filter_by(key=key).first()
            if setting:
                setting.value = value
                if description:
                    setting.description = description
                setting.updated_at = datetime.utcnow()
            else:
                setting = Setting(key=key, value=value, description=description)
                db.session.add(setting)
            db.session.commit()
            return setting
        
        def to_dict(self):
            """Convert setting to dictionary"""
            return {
                'id': self.id,
                'key': self.key,
                'value': self.value,
                'description': self.description,
                'is_public': self.is_public,
                'created_at': self.created_at.isoformat() if self.created_at else None,
                'updated_at': self.updated_at.isoformat() if self.updated_at else None
            }
        
        def __repr__(self):
            return f'<Setting {self.key}>'

    # Make classes available globally
    globals()['User'] = User
    globals()['ActivityLog'] = ActivityLog  
    globals()['Setting'] = Setting
    
    return User, ActivityLog, Setting

def create_default_data():
    """Create default data for the application"""
    if not db:
        return
        
    # Check if we already have data
    if User.query.first():
        return
    
    # Create admin user if it doesn't exist
    admin = User(
        username='admin',
        email='admin@example.com', 
        first_name='Admin',
        last_name='User',
        is_admin=True,
        is_active=True
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Create default settings
    default_settings = [
        ('app_name', 'flask-datta-able-base', 'Application name'),
        ('app_version', '1.0.0', 'Application version'),
        ('maintenance_mode', 'false', 'Enable maintenance mode'),
        ('allow_registration', 'true', 'Allow new user registration'),
        ('max_file_size', '16777216', 'Maximum file upload size in bytes'),
    ]
    
    for key, value, description in default_settings:
        if not Setting.query.filter_by(key=key).first():
            setting = Setting(key=key, value=value, description=description)
            db.session.add(setting)
    
    # Create initial activity log
    log = ActivityLog(
        user_id=None,
        action='system_init',
        description='System initialized with default data',
        ip_address='127.0.0.1'
    )
    db.session.add(log)
    
    db.session.commit()

# For backward compatibility, provide empty classes when db is None
if db is None:
    class User:
        pass
    class ActivityLog:
        pass
    class Setting:
        pass