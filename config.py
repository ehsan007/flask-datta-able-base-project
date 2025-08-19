"""
flask-datta-able-base - Configuration Management
Handles both environment variables (.env) and application settings (config.yaml)
"""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """
    Configuration class that loads settings from both .env and config.yaml
    
    Usage:
        config = Config()
        database_url = config.get_env('DATABASE_URL')
        app_name = config.get('app.name')
    """
    
    def __init__(self, config_file='config.yaml', env_file='.env'):
        """
        Initialize configuration
        
        Args:
            config_file: Path to YAML configuration file
            env_file: Path to environment variables file
        """
        self.config_file = Path(config_file)
        self.env_file = Path(env_file)
        
        # Load environment variables from .env file
        self._load_env_file()
        
        # Load application settings from YAML file
        self._load_yaml_config()
    
    def _load_env_file(self):
        """Load environment variables from .env file if it exists"""
        if self.env_file.exists():
            load_dotenv(self.env_file)
            print(f"✅ Loaded environment variables from {self.env_file}")
        else:
            print(f"⚠️  Environment file {self.env_file} not found. Using system environment variables only.")
    
    def _load_yaml_config(self):
        """Load application settings from YAML configuration file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as file:
                    self._yaml_config = yaml.safe_load(file) or {}
                print(f"✅ Loaded application settings from {self.config_file}")
            except yaml.YAMLError as e:
                print(f"❌ Error parsing YAML config file: {e}")
                self._yaml_config = {}
            except Exception as e:
                print(f"❌ Error loading config file: {e}")
                self._yaml_config = {}
        else:
            print(f"⚠️  Configuration file {self.config_file} not found. Using defaults.")
            self._yaml_config = {}
    
    def get_env(self, key, default=None, cast_type=str):
        """
        Get environment variable with optional type casting
        
        Args:
            key: Environment variable name
            default: Default value if not found
            cast_type: Type to cast the value to (str, int, bool, float)
        
        Returns:
            Environment variable value or default
        """
        value = os.getenv(key, default)
        
        if value is None:
            return None
        
        # Type casting
        if cast_type == bool:
            return str(value).lower() in ('true', '1', 'yes', 'on')
        elif cast_type in (int, float):
            try:
                return cast_type(value)
            except (ValueError, TypeError):
                return default
        
        return cast_type(value)
    
    def get(self, path, default=None):
        """
        Get configuration value using dot notation
        
        Args:
            path: Dot-separated path to the configuration value (e.g., 'app.name')
            default: Default value if not found
        
        Returns:
            Configuration value or default
        """
        keys = path.split('.')
        value = self._yaml_config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_section(self, section):
        """
        Get entire configuration section
        
        Args:
            section: Section name (e.g., 'database', 'logging')
        
        Returns:
            Dictionary containing section configuration
        """
        return self._yaml_config.get(section, {})
    
    def update_from_env(self, mapping):
        """
        Update configuration values from environment variables
        
        Args:
            mapping: Dictionary mapping config paths to env variable names
                    e.g., {'app.debug': 'FLASK_DEBUG', 'database.url': 'DATABASE_URL'}
        """
        for config_path, env_key in mapping.items():
            env_value = self.get_env(env_key)
            if env_value is not None:
                # Update the YAML config with environment value
                keys = config_path.split('.')
                target = self._yaml_config
                
                # Navigate to the parent dictionary
                for key in keys[:-1]:
                    if key not in target:
                        target[key] = {}
                    target = target[key]
                
                # Set the final value
                target[keys[-1]] = env_value
    
    def to_flask_config(self):
        """
        Convert configuration to Flask-compatible format
        
        Returns:
            Dictionary suitable for Flask app.config.update()
        """
        flask_config = {
            # Core Flask settings from environment
            'SECRET_KEY': self.get_env('SECRET_KEY', 'dev-secret-key-change-in-production'),
            'DEBUG': self.get_env('FLASK_DEBUG', False, bool),
            'TESTING': self.get('development.testing', False),
            
            # Upload settings
            'UPLOAD_FOLDER': self.get_env('UPLOAD_FOLDER', self.get('uploads.folder', 'uploads')),
            'MAX_CONTENT_LENGTH': self.get_env('MAX_CONTENT_LENGTH', 
                                               self.get('uploads.max_file_size', 16777216), int),
            
            # Database settings (if using database)
            'SQLALCHEMY_DATABASE_URI': self.get_env('DATABASE_URL'),
            'SQLALCHEMY_ECHO': self.get('database.echo', False),
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            
            # Session settings
            'PERMANENT_SESSION_LIFETIME': self.get('security.session.permanent_lifetime', 3600),
            'SESSION_COOKIE_SECURE': self.get('security.session.cookie_secure', False),
            'SESSION_COOKIE_HTTPONLY': self.get('security.session.cookie_httponly', True),
            'SESSION_COOKIE_SAMESITE': self.get('security.session.cookie_samesite', 'Lax'),
            
            # Template settings
            'TEMPLATES_AUTO_RELOAD': self.get('development.template_auto_reload', True),
            'EXPLAIN_TEMPLATE_LOADING': self.get('development.explain_template_loading', False),
        }
        
        # Remove None values
        return {k: v for k, v in flask_config.items() if v is not None}
    
    def is_development(self):
        """Check if running in development mode"""
        return self.get_env('FLASK_ENV') == 'development'
    
    def is_production(self):
        """Check if running in production mode"""
        return self.get_env('FLASK_ENV') == 'production'
    
    def is_testing(self):
        """Check if running in testing mode"""
        return self.get('development.testing', False)
    
    def __repr__(self):
        """String representation of config"""
        env_file_status = "✅" if self.env_file.exists() else "❌"
        yaml_file_status = "✅" if self.config_file.exists() else "❌"
        
        return (f"Config(env_file={env_file_status}{self.env_file}, "
                f"yaml_file={yaml_file_status}{self.config_file})")


# Global config instance
config = Config()


# Convenience functions for easy access
def get_env(key, default=None, cast_type=str):
    """Get environment variable"""
    return config.get_env(key, default, cast_type)


def get_config(path, default=None):
    """Get configuration value using dot notation"""
    return config.get(path, default)


def get_section(section):
    """Get entire configuration section"""
    return config.get_section(section)