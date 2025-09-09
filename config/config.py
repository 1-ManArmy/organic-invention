"""
Configuration settings for OneLastAI Global Platform
"""
import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'onelastai-super-secret-key-2025'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://localhost/onelastai_platform'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    
    # Redis configuration
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # Keycloak configuration
    KEYCLOAK_SERVER_URL = os.environ.get('KEYCLOAK_SERVER_URL') or 'http://localhost:8080'
    KEYCLOAK_REALM = os.environ.get('KEYCLOAK_REALM') or 'onelastai'
    KEYCLOAK_CLIENT_ID = os.environ.get('KEYCLOAK_CLIENT_ID') or 'ai-platform'
    KEYCLOAK_CLIENT_SECRET = os.environ.get('KEYCLOAK_CLIENT_SECRET') or 'your-client-secret'
    
    # Payment gateway settings
    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')
    
    PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID')
    PAYPAL_CLIENT_SECRET = os.environ.get('PAYPAL_CLIENT_SECRET')
    PAYPAL_MODE = os.environ.get('PAYPAL_MODE', 'sandbox')  # 'sandbox' or 'live'
    
    LEMONSQUEEZY_API_KEY = os.environ.get('LEMONSQUEEZY_API_KEY')
    LEMONSQUEEZY_STORE_ID = os.environ.get('LEMONSQUEEZY_STORE_ID')
    LEMONSQUEEZY_WEBHOOK_SECRET = os.environ.get('LEMONSQUEEZY_WEBHOOK_SECRET')
    
    # Session configuration
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'onelastai:'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Security settings
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'json'}
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # AI Agent settings
    AGENT_RESPONSE_TIMEOUT = 30  # seconds
    MAX_CONVERSATION_LENGTH = 100  # messages
    AGENT_RATE_LIMIT = '100/hour'  # requests per hour
    
    # Analytics & Monitoring
    GOOGLE_ANALYTICS_ID = os.environ.get('GOOGLE_ANALYTICS_ID')
    SENTRY_DSN = os.environ.get('SENTRY_DSN')
    
    # Feature flags
    ENABLE_AI_AGENTS = True
    ENABLE_PAYMENTS = True
    ENABLE_ANALYTICS = True
    ENABLE_MONITORING = True

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}