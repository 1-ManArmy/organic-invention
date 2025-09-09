"""
Pages Module - Legal, Dashboard, Compliance
"""
from pages.legal.privacy import privacy_bp
from pages.legal.terms import terms_bp
from pages.dashboard.routes import dashboard_bp
from pages.laws.compliance import compliance_bp

def register_page_routes(app):
    """Register all page routes with Flask app"""
    
    # Register page blueprints
    app.register_blueprint(privacy_bp, url_prefix='/legal')
    app.register_blueprint(terms_bp, url_prefix='/legal')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(compliance_bp, url_prefix='/compliance')
    
    print("📄 Legal, Dashboard, and Compliance pages registered!")