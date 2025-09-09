#!/bin/bash

# AI Agents Platform - Development Setup Script
# Quick setup for local development environment

set -e

echo "🛠️  AI Agents Platform - Development Setup"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[SETUP]${NC} $1"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Check Python version
check_python() {
    log "Checking Python installation..."
    
    if ! command -v python3 &> /dev/null; then
        error "Python 3 is required but not installed"
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    info "Python version: $PYTHON_VERSION"
}

# Create virtual environment
setup_venv() {
    log "Setting up virtual environment..."
    
    if [ -d "venv" ]; then
        warn "Virtual environment already exists. Recreating..."
        rm -rf venv
    fi
    
    python3 -m venv venv
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    info "✅ Virtual environment created"
}

# Install dependencies
install_dependencies() {
    log "Installing dependencies..."
    
    source venv/bin/activate
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
        info "✅ Requirements installed"
    else
        warn "requirements.txt not found, installing basic dependencies..."
        pip install flask flask-sqlalchemy flask-migrate psycopg2-binary python-keycloak gunicorn python-dotenv
    fi
}

# Setup environment file
setup_environment() {
    log "Setting up environment configuration..."
    
    if [ ! -f ".env" ]; then
        cat > .env << EOF
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=true
SECRET_KEY=dev-secret-key-change-in-production

# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/aiagents

# Passage Configuration (powered by 1Password)
PASSAGE_APP_ID=your_passage_app_id
PASSAGE_API_KEY=your_passage_api_key
PASSAGE_WEBHOOK_SECRET=your_passage_webhook_secret

# Payment Configuration
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key
STRIPE_SECRET_KEY=sk_test_your_stripe_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_CLIENT_SECRET=your_paypal_client_secret
PAYPAL_ENVIRONMENT=sandbox

LEMONSQUEEZY_API_KEY=your_lemonsqueezy_api_key
LEMONSQUEEZY_WEBHOOK_SECRET=your_lemonsqueezy_webhook_secret

# External APIs (Optional)
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
EOF
        info "✅ Environment file created (.env)"
        warn "Please update the .env file with your actual configuration values"
    else
        info "Environment file already exists"
    fi
}

# Setup database (if PostgreSQL is available)
setup_database() {
    log "Setting up database..."
    
    source venv/bin/activate
    
    # Check if PostgreSQL is available
    if command -v psql &> /dev/null; then
        info "PostgreSQL found, setting up database..."
        
        # Create database if it doesn't exist
        createdb aiagents 2>/dev/null || info "Database 'aiagents' already exists or couldn't be created"
        
        # Run migrations
        python models/migrations.py create
        info "✅ Database tables created"
        
        # Seed database for development
        python models/migrations.py seed
        info "✅ Database seeded with test data"
    else
        warn "PostgreSQL not found. You'll need to set up a database manually."
        info "Alternative: Use SQLite for development by changing DATABASE_URL in .env"
        info "SQLite URL: sqlite:///aiagents.db"
    fi
}

# Create development scripts
create_dev_scripts() {
    log "Creating development scripts..."
    
    # Create run script
    cat > run_dev.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
export FLASK_ENV=development
export FLASK_DEBUG=true
python manage.py
EOF
    chmod +x run_dev.sh
    
    # Create test script
    cat > run_tests.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
python -m pytest tests/ -v
EOF
    chmod +x run_tests.sh
    
    info "✅ Development scripts created (run_dev.sh, run_tests.sh)"
}

# Show completion message
show_completion() {
    echo ""
    echo "🎉 Development environment setup complete!"
    echo ""
    echo "Next steps:"
    echo "1. Update configuration in .env file"
    echo "2. Start the development server:"
    echo "   ./run_dev.sh"
    echo ""
    echo "or manually:"
    echo "   source venv/bin/activate"
    echo "   python manage.py"
    echo ""
    echo "📚 Available URLs:"
    echo "   - Homepage: http://localhost:5000"
    echo "   - Agents: http://localhost:5000/agents"
    echo "   - Dashboard: http://localhost:5000/dashboard (requires login)"
    echo ""
    echo "🔧 Development tools:"
    echo "   - Run tests: ./run_tests.sh"
    echo "   - Database migrations: python models/migrations.py [command]"
    echo ""
}

# Main setup function
main() {
    echo "Starting development environment setup..."
    
    check_python
    setup_venv
    install_dependencies
    setup_environment
    setup_database
    create_dev_scripts
    show_completion
}

# Run main function
main