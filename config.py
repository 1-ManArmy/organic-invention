"""
Environment Configuration Loader for AI Agents Platform
Loads and validates API keys from .env file
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for AI Agents Platform"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production-2025')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///aiagents.db')
    
    # Payment Configuration
    PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
    PAYPAL_CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET')
    PAYPAL_ENVIRONMENT = os.getenv('PAYPAL_ENVIRONMENT', 'sandbox')
    
    STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
    STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')
    
    # AI and ML Services
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    COHERE_API_KEY = os.getenv('COHERE_API_KEY')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
    REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
    RUNWAYML_API_KEY = os.getenv('RUNWAYML_API_KEY')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    
    # Database and Vector Storage
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    
    # Geolocation and Network Services
    IPGEOLOCATION_API_KEY = os.getenv('IPGEOLOCATION_API_KEY')
    WHOISJSONAPI_API_KEY = os.getenv('WHOISJSONAPI_API_KEY')
    
    # Security and Analysis Services
    ABUSEIPDB_API_KEY = os.getenv('ABUSEIPDB_API_KEY')
    SHODAN_API_KEY = os.getenv('SHODAN_API_KEY')
    VIRUSTOTAL_API_KEY = os.getenv('VIRUSTOTAL_API_KEY')
    
    # Financial and Data Services
    ALPHAVANTAGE_API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')
    
    # Government and Space APIs
    NASA_API_KEY = os.getenv('NASA_API_KEY')
    
    # Server Configuration
    PORT = int(os.getenv('PORT', 5000))
    HOST = os.getenv('HOST', '0.0.0.0')
    
    @classmethod
    def validate_keys(cls):
        """Validate that required API keys are present"""
        required_keys = [
            'OPENAI_API_KEY',
            'PAYPAL_CLIENT_ID',
            'PAYPAL_CLIENT_SECRET'
        ]
        
        missing_keys = []
        for key in required_keys:
            if not getattr(cls, key):
                missing_keys.append(key)
        
        if missing_keys:
            print(f"⚠️  Warning: Missing required API keys: {', '.join(missing_keys)}")
            return False
        
        print("✅ All required API keys are configured")
        return True
    
    @classmethod
    def get_ai_services(cls):
        """Get available AI services based on configured keys"""
        services = {}
        
        if cls.OPENAI_API_KEY:
            services['openai'] = cls.OPENAI_API_KEY
        if cls.ELEVENLABS_API_KEY:
            services['elevenlabs'] = cls.ELEVENLABS_API_KEY
        if cls.GEMINI_API_KEY:
            services['gemini'] = cls.GEMINI_API_KEY
        if cls.COHERE_API_KEY:
            services['cohere'] = cls.COHERE_API_KEY
        if cls.GROQ_API_KEY:
            services['groq'] = cls.GROQ_API_KEY
        if cls.HUGGINGFACE_API_KEY:
            services['huggingface'] = cls.HUGGINGFACE_API_KEY
        if cls.REPLICATE_API_TOKEN:
            services['replicate'] = cls.REPLICATE_API_TOKEN
        if cls.RUNWAYML_API_KEY:
            services['runway'] = cls.RUNWAYML_API_KEY
        if cls.ANTHROPIC_API_KEY:
            services['anthropic'] = cls.ANTHROPIC_API_KEY
            
        return services

# Create a global config instance
config = Config()

def load_config():
    """Load and validate configuration"""
    config.validate_keys()
    return config

if __name__ == "__main__":
    # Test configuration loading
    print("🔧 Testing Configuration...")
    cfg = load_config()
    
    print(f"📡 AI Services Available: {len(cfg.get_ai_services())}")
    for service, key in cfg.get_ai_services().items():
        print(f"  ✅ {service}: {'*' * 10}{key[-10:] if key else 'Not configured'}")
    
    print(f"💳 Payment Services:")
    print(f"  PayPal: {'✅' if cfg.PAYPAL_CLIENT_ID else '❌'}")
    print(f"  Stripe: {'✅' if cfg.STRIPE_SECRET_KEY else '❌'}")
    
    print(f"🗄️  Database: {cfg.DATABASE_URL}")
    print(f"🚀 Server: {cfg.HOST}:{cfg.PORT}")