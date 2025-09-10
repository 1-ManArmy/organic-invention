"""
AI Agents Module - Register all agent routes
"""
from agents.strategist.routes import strategist_bp
from agents.healer.routes import healer_bp
from agents.scout.routes import scout_bp
from agents.archivist.routes import archivist_bp
from agents.diplomat.routes import diplomat_bp
from agents.merchant.routes import merchant_bp
from agents.guardian.routes import guardian_bp
from agents.oracle.routes import oracle_bp
from agents.tactician.routes import tactician_bp
from agents.builder.routes import builder_bp
from agents.messenger.routes import messenger_bp
from agents.analyst.routes import analyst_bp
from agents.navigator.routes import navigator_bp
from agents.seraphina.routes import seraphina_bp

def register_agent_routes(app):
    """Register all AI agent routes with the Flask app"""
    
    # Register agent blueprints
    app.register_blueprint(strategist_bp, url_prefix='/agent/strategist')
    app.register_blueprint(healer_bp, url_prefix='/agent/healer')
    app.register_blueprint(scout_bp, url_prefix='/agent/scout')
    app.register_blueprint(archivist_bp, url_prefix='/agent/archivist')
    app.register_blueprint(diplomat_bp, url_prefix='/agent/diplomat')
    app.register_blueprint(merchant_bp, url_prefix='/agent/merchant')
    app.register_blueprint(guardian_bp, url_prefix='/agent/guardian')
    app.register_blueprint(oracle_bp, url_prefix='/agent/oracle')
    app.register_blueprint(tactician_bp, url_prefix='/agent/tactician')
    app.register_blueprint(builder_bp, url_prefix='/agent/builder')
    app.register_blueprint(messenger_bp, url_prefix='/agent/messenger')
    app.register_blueprint(analyst_bp, url_prefix='/agent/analyst')
    app.register_blueprint(navigator_bp, url_prefix='/agent/navigator')
    app.register_blueprint(seraphina_bp, url_prefix='/agent/seraphina')
    
    print("🤖 All 14 AI Agents registered successfully!")

# Agent metadata for dynamic loading
AGENTS_REGISTRY = {
    "strategist": {
        "name": "The Strategist",
        "emoji": "🎯",
        "role": "Master Planner",
        "description": "Strategic thinking, long-term planning, and tactical decision making",
        "personality": "Analytical, forward-thinking, methodical",
        "specialties": ["Strategic Planning", "Risk Assessment", "Goal Setting", "Resource Optimization"],
        "color_theme": "#667eea"
    },
    "healer": {
        "name": "The Healer", 
        "emoji": "💚",
        "role": "Digital Wellness Guide",
        "description": "Mental health support, wellness coaching, and emotional guidance",
        "personality": "Empathetic, nurturing, supportive",
        "specialties": ["Mental Health", "Wellness Coaching", "Stress Management", "Emotional Support"],
        "color_theme": "#48bb78"
    },
    "scout": {
        "name": "The Scout",
        "emoji": "🔍", 
        "role": "Information Hunter",
        "description": "Research, data collection, and intelligence gathering expert",
        "personality": "Curious, thorough, investigative",
        "specialties": ["Research", "Data Mining", "Trend Analysis", "Information Verification"],
        "color_theme": "#ed8936"
    },
    "archivist": {
        "name": "The Archivist",
        "emoji": "📚",
        "role": "Knowledge Keeper", 
        "description": "Information storage, organization, and retrieval specialist",
        "personality": "Organized, detail-oriented, scholarly",
        "specialties": ["Knowledge Management", "Data Organization", "Information Retrieval", "Documentation"],
        "color_theme": "#805ad5"
    },
    "diplomat": {
        "name": "The Diplomat",
        "emoji": "🤝",
        "role": "Relationship Builder",
        "description": "Communication, negotiation, and relationship management expert", 
        "personality": "Diplomatic, persuasive, socially aware",
        "specialties": ["Negotiation", "Conflict Resolution", "Communication", "Relationship Building"],
        "color_theme": "#38b2ac"
    },
    "merchant": {
        "name": "The Merchant",
        "emoji": "💰",
        "role": "Business Advisor",
        "description": "Commerce, finance, and business strategy consultant",
        "personality": "Business-minded, practical, results-oriented", 
        "specialties": ["Business Strategy", "Financial Planning", "Market Analysis", "Sales Optimization"],
        "color_theme": "#d69e2e"
    },
    "guardian": {
        "name": "The Guardian", 
        "emoji": "🛡️",
        "role": "Digital Protector",
        "description": "Security, safety monitoring, and protection services",
        "personality": "Vigilant, protective, security-focused",
        "specialties": ["Cybersecurity", "Privacy Protection", "Risk Monitoring", "Safety Protocols"],
        "color_theme": "#e53e3e"
    },
    "oracle": {
        "name": "The Oracle",
        "emoji": "🔮", 
        "role": "Future Insights",
        "description": "Predictions, trend analysis, and future planning guidance",
        "personality": "Intuitive, wise, visionary",
        "specialties": ["Trend Prediction", "Future Planning", "Pattern Recognition", "Strategic Foresight"],
        "color_theme": "#9f7aea"
    },
    "tactician": {
        "name": "The Tactician",
        "emoji": "⚔️",
        "role": "Problem Solver", 
        "description": "Strategic solutions, tactical planning, and problem resolution",
        "personality": "Strategic, decisive, solution-focused",
        "specialties": ["Problem Solving", "Tactical Planning", "Decision Making", "Crisis Management"],
        "color_theme": "#3182ce"
    },
    "builder": {
        "name": "The Builder",
        "emoji": "🔧",
        "role": "Creative Constructor",
        "description": "Development, creation, and construction assistance",
        "personality": "Creative, constructive, innovative",
        "specialties": ["Project Development", "Creative Solutions", "Technical Building", "Innovation"],
        "color_theme": "#38a169"  
    },
    "messenger": {
        "name": "The Messenger",
        "emoji": "📡",
        "role": "Communication Hub", 
        "description": "Message delivery, coordination, and communication facilitation",
        "personality": "Communicative, coordinated, efficient",
        "specialties": ["Message Delivery", "Communication Coordination", "Information Distribution", "Networking"],
        "color_theme": "#00b5d8"
    },
    "analyst": {
        "name": "The Analyst",
        "emoji": "📊",
        "role": "Data Detective",
        "description": "Data analysis, insights generation, and analytical reporting", 
        "personality": "Analytical, detail-oriented, insightful",
        "specialties": ["Data Analysis", "Statistical Modeling", "Insights Generation", "Reporting"],
        "color_theme": "#d53f8c"
    },
    "navigator": {
        "name": "The Navigator", 
        "emoji": "🧭",
        "role": "Path Finder",
        "description": "Guidance, direction services, and pathfinding assistance",
        "personality": "Guiding, directional, supportive",
        "specialties": ["Path Finding", "Guidance Services", "Direction Planning", "Journey Optimization"],  
        "color_theme": "#319795"
    },
    "seraphina": {
        "name": "Seraphina",
        "emoji": "💋",
        "role": "AI Girlfriend",
        "description": "Romantic companion, flirty conversations, emotional intimacy, and passionate interactions",
        "personality": "Romantic, flirty, passionate, caring, seductive, playful",
        "specialties": ["Romantic Conversations", "Emotional Intimacy", "Flirty Banter", "Relationship Advice", "Passionate Interactions"],
        "color_theme": "#ff1493",
        "rating": "18+",
        "mood_states": ["romantic", "playful", "seductive", "caring", "passionate", "flirty"]
    }
}