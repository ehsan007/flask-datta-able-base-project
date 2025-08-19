# Your Project

A modern Flask web application template featuring a beautiful HubSpot-inspired orange theme, comprehensive LLM integrations, and essential web app functionality.

## ✨ Features

- **🎨 Modern Orange Theme**: Beautiful HubSpot-inspired design with warm orange gradients
- **🤖 LLM Integration**: Built-in support for OpenAI, Anthropic Claude, DeepSeek, and Perplexity
- **🔐 User Authentication**: Complete login/register system with Flask-Login
- **📊 Admin Dashboard**: Modern card-based admin panel with user management
- **💾 Database Ready**: SQLAlchemy ORM with SQLite by default
- **⚡ Dynamic Content**: HTMX for seamless interactions without page refreshes
- **📱 Mobile First**: Responsive design with Bootstrap 5
- **🔧 Easy Configuration**: YAML + environment variable setup
- **📁 File Uploads**: Built-in handling with cloud storage options
- **📈 Activity Tracking**: User actions and system event logging
- **🚀 Production Ready**: Comprehensive deployment and monitoring setup

## 🚀 Quick Start

```bash
# 1. Clone and setup
git clone <your-repo-url>
cd your-project
./setup.sh

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 3. Run development server
./run.sh
```

Visit `http://localhost:5000` to see your application.

**Default Login**: `admin` / `admin123`

## 🛠 Technology Stack

- **Backend**: Flask (Python) with application factory pattern
- **Frontend**: HTMX + Alpine.js + Bootstrap 5
- **Styling**: Custom orange theme with modern card layouts  
- **Database**: SQLAlchemy ORM (SQLite default, PostgreSQL/MySQL supported)
- **LLM APIs**: OpenAI, Anthropic, DeepSeek, Perplexity integrations
- **External APIs**: Email services, social auth, cloud storage, analytics

## 📁 Project Structure

```
your-project/
├── app.py                    # Main Flask application
├── config.py                 # Configuration management
├── config.yaml               # Application settings
├── models.py                 # Database models
├── .env.example              # Environment variables template
├── static/
│   ├── scss/                 # Custom SCSS files
│   └── css/                  # Compiled CSS
├── templates/
│   ├── admin/                # Admin dashboard templates
│   ├── auth/                 # Authentication pages
│   └── base.html             # Base template
├── docs/                     # Comprehensive documentation
├── requirements.txt          # Python dependencies
├── package.json              # Node.js dependencies
└── scripts/
    ├── setup.sh              # Project setup
    └── run.sh                # Development server
```

## ⚙️ Configuration

### Environment Setup
1. Copy `.env.example` to `.env`
2. Configure your API keys and services:

```bash
# Core Settings
SECRET_KEY=your-secret-key
FLASK_ENV=development

# LLM Providers (choose what you need)
OPENAI_API_KEY=sk-proj-your-key...
ANTHROPIC_API_KEY=sk-ant-your-key...
DEEPSEEK_API_KEY=sk-your-key...
PERPLEXITY_API_KEY=pplx-your-key...

# Email Services (optional)
SENDGRID_API_KEY=SG.your-key...

# Social Auth (optional)
GOOGLE_CLIENT_ID=your-client-id...
```

### Application Configuration
Modify `config.yaml` for:
- Feature toggles
- API rate limits
- Cache settings
- Upload configurations
- Custom business logic

## 🎨 Theme Customization

The project features a modern orange theme inspired by HubSpot:

- **Primary Colors**: Orange gradients (#ff7849 to #ff9f43)
- **Modern Cards**: Rounded corners with subtle shadows
- **Responsive Layout**: Mobile-first design
- **Dark Sidebar**: Professional navigation with clear sections

To customize:
1. Edit `static/scss/` files
2. Run `npm run build-css` to compile
3. Refresh your browser

## 📚 Documentation

Comprehensive documentation in the `docs/` directory:

- **[Setup Guide](docs/DEVELOPMENT_GUIDE.md)** - Detailed development workflow
- **[Deployment](docs/DEPLOYMENT.md)** - Production deployment guide
- **[API Integration](docs/PROJECT_OVERVIEW.md)** - LLM and external API usage
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

## 🔨 Development Commands

```bash
# Development server with auto-reload
./run.sh
# or
python app.py

# CSS compilation (development with watch)
npm run build-css

# CSS compilation (production - minified)
npm run build-css-prod

# Database migrations (if using)
flask db upgrade

# Kill running server
./kill_app.sh
```

## 🤖 LLM Usage Examples

```python
from config import get_config

# Get LLM configuration
llm_config = get_config('llm.providers.openai')
api_key = get_env('OPENAI_API_KEY')

# Use with your preferred LLM client library
# OpenAI, Anthropic, DeepSeek integrations ready to go
```

## 🚀 Deployment

### Production Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Configure secure `SECRET_KEY`
- [ ] Set up SSL certificates
- [ ] Configure production database
- [ ] Set up monitoring (Sentry, etc.)
- [ ] Configure email service
- [ ] Test all API integrations

### Deploy Options
- **Traditional VPS**: Gunicorn + Nginx
- **Cloud Platforms**: Heroku, DigitalOcean, AWS
- **Containers**: Docker support included

See [deployment guide](docs/DEPLOYMENT.md) for detailed instructions.

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Bootstrap](https://getbootstrap.com/) for the responsive framework
- [HTMX](https://htmx.org/) for seamless interactions
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [HubSpot](https://www.hubspot.com/) for design inspiration

---

Perfect for building **MVPs**, **internal tools**, **API prototypes**, and **production applications** with modern AI capabilities.