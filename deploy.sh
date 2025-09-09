#!/bin/bash

# AI Agents Platform Deployment Script
# Production deployment automation

set -e  # Exit on any error

echo "🚀 Starting AI Agents Platform Deployment..."

# Configuration
APP_NAME="ai-agents-platform"
APP_DIR="/var/www/aiagentsplatform"
PYTHON_VERSION="3.9"
VENV_DIR="$APP_DIR/venv"
BACKUP_DIR="/var/backups/aiagentsplatform"
LOG_FILE="/var/log/deploy-aiagents.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a $LOG_FILE
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a $LOG_FILE
    exit 1
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a $LOG_FILE
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a $LOG_FILE
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   error "This script should not be run as root for security reasons"
fi

# Check system requirements
check_requirements() {
    log "🔍 Checking system requirements..."
    
    # Check Python version
    if ! command -v python3 &> /dev/null; then
        error "Python 3 is not installed"
    fi
    
    # Check PostgreSQL
    if ! command -v psql &> /dev/null; then
        warn "PostgreSQL client not found. Make sure database is accessible."
    fi
    
    # Check Nginx
    if ! command -v nginx &> /dev/null; then
        warn "Nginx not found. Web server configuration may be needed."
    fi
    
    log "✅ System requirements check completed"
}

# Create backup
create_backup() {
    log "📦 Creating application backup..."
    
    if [ -d "$APP_DIR" ]; then
        TIMESTAMP=$(date +%Y%m%d_%H%M%S)
        BACKUP_NAME="aiagents_backup_$TIMESTAMP"
        
        sudo mkdir -p $BACKUP_DIR
        sudo tar -czf "$BACKUP_DIR/$BACKUP_NAME.tar.gz" -C "$APP_DIR" . || error "Backup creation failed"
        
        log "✅ Backup created: $BACKUP_DIR/$BACKUP_NAME.tar.gz"
    else
        info "No existing application directory found. Skipping backup."
    fi
}

# Setup application directory
setup_app_directory() {
    log "📁 Setting up application directory..."
    
    sudo mkdir -p $APP_DIR
    sudo chown $USER:$USER $APP_DIR
    
    # Copy application files
    if [ -d "$(pwd)" ]; then
        rsync -av --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' --exclude='.env' . $APP_DIR/
        log "✅ Application files copied"
    else
        error "Source directory not found"
    fi
}

# Setup Python virtual environment
setup_virtualenv() {
    log "🐍 Setting up Python virtual environment..."
    
    if [ -d "$VENV_DIR" ]; then
        rm -rf $VENV_DIR
    fi
    
    python3 -m venv $VENV_DIR || error "Virtual environment creation failed"
    source $VENV_DIR/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install dependencies
    if [ -f "$APP_DIR/requirements.txt" ]; then
        pip install -r $APP_DIR/requirements.txt || error "Requirements installation failed"
        log "✅ Python requirements installed"
    else
        error "requirements.txt not found"
    fi
}

# Setup database
setup_database() {
    log "🗄️  Setting up database..."
    
    source $VENV_DIR/bin/activate
    cd $APP_DIR
    
    # Check if DATABASE_URL is set
    if [ -z "$DATABASE_URL" ]; then
        warn "DATABASE_URL not set. Make sure to configure database connection."
        return
    fi
    
    # Run migrations
    python models/migrations.py create || warn "Database table creation failed"
    python models/migrations.py seed || warn "Database seeding failed"
    
    log "✅ Database setup completed"
}

# Setup Nginx configuration
setup_nginx() {
    log "🌐 Setting up Nginx configuration..."
    
    if ! command -v nginx &> /dev/null; then
        warn "Nginx not installed. Skipping web server configuration."
        return
    fi
    
    # Copy Nginx configuration
    if [ -f "$APP_DIR/server/nginx.conf" ]; then
        sudo cp $APP_DIR/server/nginx.conf /etc/nginx/sites-available/$APP_NAME
        sudo ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/
        
        # Test Nginx configuration
        sudo nginx -t || error "Nginx configuration test failed"
        
        log "✅ Nginx configuration updated"
    else
        warn "Nginx configuration file not found"
    fi
}

# Setup systemd service
setup_systemd() {
    log "⚙️  Setting up systemd service..."
    
    # Create systemd service file
    cat > /tmp/$APP_NAME.service << EOF
[Unit]
Description=AI Agents Platform
After=network.target

[Service]
Type=notify
User=$USER
Group=$USER
WorkingDirectory=$APP_DIR
Environment=PATH=$VENV_DIR/bin
ExecStart=$VENV_DIR/bin/gunicorn --config server/gunicorn.conf.py app:app
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

    sudo mv /tmp/$APP_NAME.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable $APP_NAME
    
    log "✅ Systemd service configured"
}

# Setup SSL certificates (Let's Encrypt)
setup_ssl() {
    log "🔒 Setting up SSL certificates..."
    
    if ! command -v certbot &> /dev/null; then
        warn "Certbot not installed. Install it to enable SSL."
        return
    fi
    
    # This would typically be run interactively
    info "Run the following command to setup SSL:"
    info "sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com"
}

# Start services
start_services() {
    log "🎬 Starting services..."
    
    # Start application
    sudo systemctl start $APP_NAME || error "Failed to start application service"
    
    # Restart Nginx if available
    if command -v nginx &> /dev/null; then
        sudo systemctl restart nginx || warn "Failed to restart Nginx"
    fi
    
    log "✅ Services started successfully"
}

# Health check
health_check() {
    log "🏥 Performing health check..."
    
    sleep 5  # Wait for services to start
    
    # Check if application is responding
    if curl -f http://localhost:5000/health > /dev/null 2>&1; then
        log "✅ Application health check passed"
    else
        error "Application health check failed"
    fi
}

# Main deployment function
main() {
    log "🚀 Starting deployment of AI Agents Platform"
    
    check_requirements
    create_backup
    setup_app_directory
    setup_virtualenv
    setup_database
    setup_nginx
    setup_systemd
    setup_ssl
    start_services
    health_check
    
    log "🎉 Deployment completed successfully!"
    log "🌐 Your AI Agents Platform should be accessible at your configured domain"
    
    info "Next steps:"
    info "1. Configure your domain name in the Nginx configuration"
    info "2. Set up SSL certificates with Let's Encrypt"
    info "3. Configure environment variables in /etc/environment or systemd service"
    info "4. Set up monitoring and log rotation"
    info "5. Configure backup schedules"
}

# Handle script arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "backup")
        create_backup
        ;;
    "health")
        health_check
        ;;
    "restart")
        sudo systemctl restart $APP_NAME
        sudo systemctl restart nginx
        log "✅ Services restarted"
        ;;
    "logs")
        sudo journalctl -u $APP_NAME -f
        ;;
    *)
        echo "Usage: $0 [deploy|backup|health|restart|logs]"
        echo "  deploy  - Full deployment (default)"
        echo "  backup  - Create backup only"
        echo "  health  - Run health check"
        echo "  restart - Restart services"
        echo "  logs    - View application logs"
        exit 1
        ;;
esac