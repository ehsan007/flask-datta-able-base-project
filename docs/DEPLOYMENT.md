# Deployment Guide - flask-datta-able-base

## Production Deployment Options

### Option 1: Docker Deployment (Recommended)

#### 1. Create Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for Sass/Bootstrap build
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Copy requirements and install Python dependencies
COPY requirements.txt package.json ./
RUN pip install --no-cache-dir -r requirements.txt
RUN npm install

# Copy application code
COPY . .

# Build SCSS for production
RUN npm run build-css-prod

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

#### 2. Create docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      # Add your environment variables here
      # - DATABASE_URL=sqlite:///instance/app.db
      # - API_KEY=${API_KEY}
    volumes:
      - ./uploads:/app/uploads
      - ./instance:/app/instance
    restart: unless-stopped

  # Uncomment if using database
  # db:
  #   image: postgres:15
  #   environment:
  #     - POSTGRES_DB=flask_datta_able_base
  #     - POSTGRES_USER=flask_datta
  #     - POSTGRES_PASSWORD=password
  #   volumes:
  #     - postgres_data:/var/lib/postgresql/data
  #   restart: unless-stopped

  # Uncomment for reverse proxy
  # nginx:
  #   image: nginx:alpine
  #   ports:
  #     - "80:80"
  #     - "443:443"
  #   volumes:
  #     - ./nginx.conf:/etc/nginx/nginx.conf
  #     - ./ssl:/etc/ssl/certs
  #   depends_on:
  #     - web
  #   restart: unless-stopped

# volumes:
#   postgres_data:
```

#### 3. Deploy with Docker Compose
```bash
# Create environment file
echo "SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')" > .env
# echo "DATABASE_URL=your-database-url" >> .env
# echo "API_KEY=your-api-key" >> .env

# Build and deploy
docker-compose up -d

# Check logs
docker-compose logs -f web
```

---

### Option 2: Traditional Server Deployment

#### 1. Server Setup (Ubuntu/Debian)
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python, Node.js, and dependencies
sudo apt install -y python3 python3-pip python3-venv nginx curl
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Create application user
sudo useradd --create-home --shell /bin/bash flaskapp
sudo su - flaskapp

# Clone repository
git clone <your-repository> /home/flaskapp/app
cd /home/flaskapp/app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn
npm install

# Build SCSS for production
npm run build-css-prod
```

#### 2. Environment Configuration
```bash
# Create production environment file
nano /home/flaskapp/app/.env
```

```env
FLASK_ENV=production
SECRET_KEY=your-very-secure-secret-key-here
# DATABASE_URL=sqlite:///app.db
# API_KEY=your-api-key
```

#### 3. Systemd Service
```bash
sudo nano /etc/systemd/system/flask-datta-able-base.service
```

```ini
[Unit]
Description=Flask Datta Able Base
After=network.target

[Service]
User=flaskapp
Group=flaskapp
WorkingDirectory=/home/flaskapp/app
Environment="PATH=/home/flaskapp/app/venv/bin"
ExecStart=/home/flaskapp/app/venv/bin/gunicorn --bind unix:/home/flaskapp/app/flask-datta-able-base.sock --workers 4 --timeout 120 app:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable flask-datta-able-base
sudo systemctl start flask-datta-able-base
sudo systemctl status flask-datta-able-base
```

#### 4. Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/flask-datta-able-base
```

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # Redirect HTTP to HTTPS (if using SSL)
    # return 301 https://$server_name$request_uri;
    
    # For development/non-SSL setup:
    client_max_body_size 16M;
    
    # Static files
    location /static {
        alias /home/flaskapp/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Application
    location / {
        proxy_pass http://unix:/home/flaskapp/app/flask-datta-able-base.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
        proxy_connect_timeout 120s;
    }
}

# SSL configuration (uncomment if using SSL)
# server {
#     listen 443 ssl http2;
#     server_name your-domain.com;
#     
#     ssl_certificate /path/to/your/certificate.pem;
#     ssl_certificate_key /path/to/your/private.key;
#     ssl_protocols TLSv1.2 TLSv1.3;
#     ssl_ciphers HIGH:!aNULL:!MD5;
#     
#     # Security headers
#     add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
#     add_header X-Frame-Options DENY;
#     add_header X-Content-Type-Options nosniff;
#     add_header X-XSS-Protection "1; mode=block";
#     
#     client_max_body_size 16M;
#     
#     location /static {
#         alias /home/flaskapp/app/static;
#         expires 1y;
#         add_header Cache-Control "public, immutable";
#     }
#     
#     location / {
#         proxy_pass http://unix:/home/flaskapp/app/flask-datta-able-base.sock;
#         proxy_set_header Host $host;
#         proxy_set_header X-Real-IP $remote_addr;
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#         proxy_set_header X-Forwarded-Proto $scheme;
#         proxy_read_timeout 120s;
#         proxy_connect_timeout 120s;
#     }
# }
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/flask-datta-able-base /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

### Option 3: Cloud Platform Deployment

#### Heroku Deployment
```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
# heroku config:set API_KEY=your-api-key

# Create Procfile
echo "web: gunicorn app:app" > Procfile
echo "release: python -c 'print(\"No migrations needed for base project\")'" >> Procfile

# Add Node.js buildpack for Sass/Bootstrap
heroku buildpacks:add --index 1 heroku/nodejs
heroku buildpacks:add --index 2 heroku/python

# Add package.json script for Heroku build
# (Make sure your package.json includes a "heroku-postbuild" script)

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

#### DigitalOcean App Platform
```yaml
# app.yaml
name: flask-datta-able-base
services:
- name: web
  source_dir: /
  github:
    repo: your-username/flask-datta-able-base
    branch: main
  run_command: gunicorn --worker-tmp-dir /dev/shm --config gunicorn.conf.py app:app
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: FLASK_ENV
    value: "production"
  - key: SECRET_KEY
    value: "your-secret-key"
    type: SECRET
```

---

## Production Configuration

### 1. Environment Variables
```env
# Core Configuration
FLASK_ENV=production
SECRET_KEY=very-secure-random-key-min-32-chars

# Database (if using)
# DATABASE_URL=postgresql://user:password@host:port/database
# DATABASE_URL=sqlite:///app.db

# API Keys (add as needed)
# API_KEY=your-api-key
# THIRD_PARTY_SERVICE_KEY=your-service-key

# Optional: Email Configuration
# MAIL_SERVER=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USE_TLS=true
# MAIL_USERNAME=your-email
# MAIL_PASSWORD=your-app-password

# Optional: Monitoring
# SENTRY_DSN=https://your-sentry-dsn
```

### 2. Health Check Endpoint
Add to your Flask app:
```python
@app.route('/health')
def health_check():
    try:
        # Test any critical services here
        # db.session.execute('SELECT 1')  # If using database
        status = "healthy"
    except Exception as e:
        status = "unhealthy"
        app.logger.error(f"Health check failed: {e}")
    
    return jsonify({
        "status": status,
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    })
```

---

## Security Considerations

### 1. SSL/TLS Setup
```bash
# Let's Encrypt with Certbot
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
sudo certbot renew --dry-run
```

### 2. Firewall Configuration
```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw deny 5000/tcp     # Block direct app access
sudo ufw enable
```

### 3. Application Security
```python
# Add to your Flask configuration for production
class ProductionConfig:
    # Security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # Additional security headers
    SECURITY_HEADERS = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block'
    }
```

---

## Monitoring and Logging

### 1. Application Logging
```python
import logging
from logging.handlers import RotatingFileHandler
import os

# Add to your Flask app factory
if not app.debug and not app.testing:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler('logs/flask-datta-able-base.log', 
                                       maxBytes=10240000, 
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('flask-datta-able-base startup')
```

### 2. System Monitoring
```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# Monitor application
sudo journalctl -u flask-datta-able-base -f   # Application logs
sudo tail -f /var/log/nginx/access.log      # Nginx logs
htop                                        # System resources
```

---

## Backup Strategy (if using database)

### 1. Database Backups
```bash
#!/bin/bash
# scripts/backup_database.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/flaskapp/backups"

mkdir -p $BACKUP_DIR

# SQLite backup
cp instance/app.db $BACKUP_DIR/app_$DATE.db

# PostgreSQL backup (if using)
# pg_dump -U username database_name | gzip > $BACKUP_DIR/app_$DATE.sql.gz

# Keep only last 30 days of backups
find $BACKUP_DIR -name "app_*.db" -mtime +30 -delete

echo "Database backup completed: app_$DATE.db"
```

### 2. Automated Backups
```bash
# Add to crontab (crontab -e)
0 2 * * * /home/flaskapp/app/scripts/backup_database.sh
```

---

## Performance Optimization

### 1. Static File Optimization
```bash
# Nginx gzip compression
# Add to nginx configuration:
gzip on;
gzip_types text/css text/javascript application/javascript application/json;
gzip_min_length 1000;
```

### 2. Caching (if needed)
```python
# Add Flask-Caching for expensive operations
from flask_caching import Cache

cache = Cache()

# In app factory
cache.init_app(app, config={
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300
})

# Cache expensive operations
@cache.memoize(timeout=300)
def expensive_operation():
    # Your expensive operation here
    pass
```

---

## Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] SSL certificates obtained (if needed)
- [ ] SCSS compiled (`npm run build-css-prod`)
- [ ] Database initialized and seeded
- [ ] Security settings configured

### Deployment
- [ ] Deploy application code
- [ ] Install dependencies
- [ ] Build static assets
- [ ] Update nginx configuration
- [ ] Start/restart services
- [ ] Verify health checks

### Post-Deployment
- [ ] Monitor error logs
- [ ] Verify performance metrics
- [ ] Test critical functionality
- [ ] Document any issues

---

*flask-datta-able-base - Deploy with confidence using modern best practices*