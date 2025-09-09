from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
from datetime import datetime

# Import modules
from config.config import Config
from auth.middleware import PassageMiddleware
from agents import register_agent_routes
from payments import register_payment_routes
from pages import register_page_routes

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize extensions
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    CORS(app)
    
    # Register blueprints
    register_agent_routes(app)
    register_payment_routes(app)
    register_page_routes(app)
    
    # Main routes
    @app.route("/")
    def homepage():
        """AI Agents Platform Homepage"""
        return render_template("index.html", title="AI Digital Friends - Next-Gen Platform")
    
    @app.route("/agents")
    def agents_overview():
        """AI Agents Overview Page"""
        agents = [
            {"name": "Strategist", "role": "🎯 Master Planner", "description": "Strategic thinking and long-term planning"},
            {"name": "Healer", "role": "💚 Digital Wellness", "description": "Mental health support and guidance"},
            {"name": "Scout", "role": "🔍 Information Hunter", "description": "Research and data collection expert"},
            {"name": "Archivist", "role": "📚 Knowledge Keeper", "description": "Information storage and retrieval"},
            {"name": "Diplomat", "role": "🤝 Relationship Builder", "description": "Communication and negotiation specialist"},
            {"name": "Merchant", "role": "💰 Business Advisor", "description": "Commerce and financial guidance"},
            {"name": "Guardian", "role": "🛡️ Digital Protector", "description": "Security and safety monitoring"},
            {"name": "Oracle", "role": "🔮 Future Insights", "description": "Predictions and trend analysis"},
            {"name": "Tactician", "role": "⚔️ Problem Solver", "description": "Strategic solutions and tactics"},
            {"name": "Builder", "role": "🔧 Creative Constructor", "description": "Development and creation assistance"},
            {"name": "Messenger", "role": "📡 Communication Hub", "description": "Message delivery and coordination"},
            {"name": "Analyst", "role": "📊 Data Detective", "description": "Data analysis and insights"},
            {"name": "Navigator", "role": "🧭 Path Finder", "description": "Guidance and direction services"}
        ]
        return render_template("agents_overview.html", agents=agents, title="AI Agents")
    
    @app.route("/api/health")
    def health_check():
        """System health endpoint"""
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "agents_loaded": 13
        })
    
    @app.errorhandler(404)
    def not_found(error):
        return render_template('error.html', error_code=404, error_message="Page not found"), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('error.html', error_code=500, error_message="Internal server error"), 500
    
    return app

# Create app instance
app = create_app()

@app.route("/")
def hello_world():
    return render_template("index.html", title="AI Agents Platform")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
