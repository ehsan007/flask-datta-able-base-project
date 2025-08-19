#!/usr/bin/env python3
"""
Database initialization script for flask-datta-able-base
Creates all database tables defined in models.py
"""

import os
import sys

def init_database():
    """Initialize the database with all tables"""
    try:
        # Import Flask and create a minimal app for database operations
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from config import config
        
        # Create minimal Flask app
        app = Flask(__name__)
        app.config.update(config.to_flask_config())
        
        # Ensure absolute path for SQLite database
        db_path = os.path.abspath('instance/app.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = config.get_env('SECRET_KEY', 'dev-secret-key')
        
        print(f"✓ Database path: {db_path}")
        
        # Initialize database
        db = SQLAlchemy(app)
        
        # Import and initialize models with the db instance
        from models import init_db, User, ActivityLog, Setting
        
        with app.app_context():
            # Initialize models and get the proper classes
            UserModel, ActivityLogModel, SettingModel = init_db(db)
            
            # Create all tables
            db.create_all()
            print("✓ Database tables created")
            
            # Check if admin user exists, create if not
            admin_user = UserModel.query.filter_by(username='admin').first()
            if not admin_user:
                admin_user = UserModel(
                    username='admin',
                    email='admin@example.com',
                    first_name='Admin',
                    last_name='User',
                    is_admin=True,
                    is_active=True
                )
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                print("✓ Created admin user (username: admin, password: admin123)")
            else:
                print("✓ Admin user already exists")
            
            # Create default settings
            default_settings = [
                ('app_name', 'flask-datta-able-base'),
                ('app_version', '1.0.0'),
                ('maintenance_mode', 'false'),
                ('allow_registration', 'true'),
            ]
            
            settings_created = 0
            for key, value in default_settings:
                if not SettingModel.query.filter_by(key=key).first():
                    setting = SettingModel(key=key, value=value)
                    db.session.add(setting)
                    settings_created += 1
            
            db.session.commit()
            if settings_created > 0:
                print(f"✓ Created {settings_created} default settings")
            else:
                print("✓ Default settings already exist")
            
            # Show table count
            user_count = UserModel.query.count()
            setting_count = SettingModel.query.count()
            activity_count = ActivityLogModel.query.count()
            print(f"✓ Database ready: Users ({user_count}), Settings ({setting_count}), Activity Logs ({activity_count})")
            
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Make sure Flask and dependencies are installed in your virtual environment")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    print("🗄️ Initializing flask-datta-able-base database...")
    
    # Make sure we're in the right directory
    if not os.path.exists('app.py'):
        print("✗ Error: app.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Create instance directory if it doesn't exist
    instance_dir = os.path.abspath('instance')
    os.makedirs(instance_dir, exist_ok=True)
    print(f"✓ Instance directory ready: {instance_dir}")
    
    init_database()