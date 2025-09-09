# 🚀 AI Agents Platform

A comprehensive AI Agents platform built with Flask, featuring 13 unique AI personalities, passwordless authentication via Passage (powered by 1Password), and enterprise-grade security.

## ✨ Features

### 🤖 13 AI Agents
- **Strategist** - Master planner for tactical thinking
- **Healer** - Digital wellness and mental health support
- **Scout** - Information hunter and research expert
- **Archivist** - Knowledge keeper and information storage
- **Diplomat** - Relationship builder and negotiation specialist
- **Merchant** - Business advisor and financial guidance
- **Guardian** - Digital protector and security monitoring
- **Oracle** - Future insights and trend analysis
- **Tactician** - Strategic problem solver
- **Builder** - Creative constructor and development assistant
- **Messenger** - Communication hub and coordination
- **Analyst** - Data detective and insights specialist
- **Navigator** - Path finder and guidance services

### 🔐 Security & Authentication
- **Passwordless Authentication** via magic links
- **Passage Integration** powered by 1Password
- **Enterprise Security** with webhook validation
- **Role-based Access Control**

### 💳 Payment Processing
- **Multiple Gateways**: Stripe, PayPal, LemonSqueezy
- **Subscription Management** with automated billing
- **Webhook Processing** for real-time updates

### 📊 Advanced Features
- **User Dashboard** with analytics and insights
- **Legal Compliance** (GDPR, CCPA, Privacy Policy)
- **Database Models** with PostgreSQL support
- **Production Ready** deployment configuration

## 🚀 Quick Start

### Development Setup
```bash
# Run the setup script
./setup_dev.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py
```

### Alternative Running Methods
```bash
# Using Flask CLI
flask --debug run

# Using the cinematic boot manager
python manage.py

# Using app.py directly
python app.py
```

### Environment Configuration
Create a `.env` file with:
```bash
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql://user:password@localhost/aiagents

# Passage Authentication (powered by 1Password)
PASSAGE_APP_ID=your_passage_app_id
PASSAGE_API_KEY=your_passage_api_key
PASSAGE_WEBHOOK_SECRET=your_passage_webhook_secret

# Payment Gateways
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key
STRIPE_SECRET_KEY=sk_test_your_stripe_key
PAYPAL_CLIENT_ID=your_paypal_client_id
LEMONSQUEEZY_API_KEY=your_lemonsqueezy_api_key
```

## 🏗️ Architecture

### Directory Structure
```
├── agents/              # 13 AI agent implementations
│   ├── strategist/      # Strategic planning agent
│   ├── healer/          # Wellness and mental health
│   ├── scout/           # Research and data collection
│   └── ...             # 10 more specialized agents
├── auth/               # Passage authentication system
├── config/             # Configuration management
├── models/             # Database models and migrations
├── pages/              # Dashboard and legal pages
├── payments/           # Payment gateway integrations
├── server/             # Production server configuration
├── static/             # CSS and static assets
├── templates/          # HTML templates
├── manage.py           # Cinematic boot manager
├── app.py              # Main Flask application
└── deploy.sh           # Production deployment script
```

### Technology Stack
- **Backend**: Flask, SQLAlchemy, PostgreSQL
- **Authentication**: Passage (1Password)
- **Payments**: Stripe, PayPal, LemonSqueezy
- **Server**: Gunicorn, Nginx
- **Deployment**: Vercel, Docker-ready

## 🌟 AI Agents System

Each agent has its own personality, capabilities, and specialized functions:

### Strategic Intelligence
- **Strategist**: Long-term planning and tactical analysis
- **Tactician**: Immediate problem-solving and strategic solutions
- **Navigator**: Guidance and direction services

### Knowledge Management
- **Archivist**: Information storage and retrieval
- **Scout**: Research and data collection
- **Analyst**: Data analysis and insights

### Communication & Relations
- **Diplomat**: Communication and negotiation
- **Messenger**: Message delivery and coordination
- **Oracle**: Predictions and future insights

### Support & Development
- **Healer**: Mental health and wellness support
- **Builder**: Development and creation assistance
- **Guardian**: Security and safety monitoring
- **Merchant**: Business and financial advisory

## 🔐 Security Features

- **Passwordless Authentication**: No passwords to manage or store
- **Magic Link Login**: Secure email-based authentication
- **1Password Integration**: Enterprise-grade security infrastructure
- **Webhook Validation**: Cryptographic signature verification
- **Session Management**: Secure token handling and revocation
- **Role-based Access**: Granular permission system

## 💳 Payment Integration

### Supported Gateways
- **Stripe**: Credit cards, subscriptions, one-time payments
- **PayPal**: PayPal payments and subscriptions
- **LemonSqueezy**: Digital product sales and subscriptions

### Features
- **Automated Billing**: Subscription management
- **Webhook Processing**: Real-time payment updates
- **Multiple Currencies**: Global payment support
- **Secure Processing**: PCI-compliant payment handling

## 📊 Dashboard & Analytics

- **User Analytics**: Conversation trends and usage patterns
- **Agent Insights**: Performance metrics and preferences
- **Subscription Management**: Plan details and billing history
- **Security Monitoring**: Login activity and session management

## 🎨 User Interface

- **Modern Design**: Responsive and mobile-friendly
- **Section-based Homepage**: Modular content organization
- **Agent-specific Interfaces**: Unique UI for each AI personality
- **Professional Login**: Beautiful passwordless authentication

## 🚀 Deployment

### Production Deployment
```bash
# Run the deployment script
./deploy.sh

# Or use individual commands
./deploy.sh backup    # Create backup
./deploy.sh health    # Check health
./deploy.sh restart   # Restart services
./deploy.sh logs      # View logs
```

### Vercel Deployment
The project includes Vercel configuration for serverless deployment:
```bash
vercel --prod
```

### Docker Support
Docker-ready architecture with production-optimized configurations.

## 📝 Legal Compliance

- **GDPR Compliance**: European data protection regulations
- **CCPA Compliance**: California privacy requirements
- **Privacy Policy**: Comprehensive privacy documentation
- **Terms of Service**: Clear terms and conditions
- **Accessibility**: WCAG 2.1 Level AA compliance
- **Cookie Policy**: Transparent cookie usage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Passage** for passwordless authentication
- **1Password** for enterprise security
- **Flask** community for the amazing framework
- **AI research community** for inspiration

## 🔗 Links

- **Repository**: https://github.com/1-ManArmy/FlaskProject
- **Issues**: https://github.com/1-ManArmy/FlaskProject/issues

---

⭐ **Star this repository if you found it helpful!**

Built with ❤️ by [1-ManArmy](https://github.com/1-ManArmy)spaces ♥️ Flask

Welcome to your shiny new Codespace running Flask! We've got everything fired up and running for you to explore Flask.

You've got a blank canvas to work on from a git perspective as well. There's a single initial commit with the what you're seeing right now - where you go from here is up to you!

Everything you do here is contained within this one codespace. There is no repository on GitHub yet. If and when you’re ready you can click "Publish Branch" and we’ll create your repository and push up your project. If you were just exploring then and have no further need for this code then you can simply delete your codespace and it's gone forever.

To run this application:

```
flask --debug run
```
