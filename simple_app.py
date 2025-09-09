#!/usr/bin/env python3
"""
Simple Flask App Launcher
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Simple Flask app without complex dependencies
from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

@app.route('/')
def home():
    """Homepage"""
    return render_template('index.html', title='AI Agents Platform')

@app.route('/health')
def health():
    """Health check"""
    return {"status": "healthy", "message": "AI Agents Platform is running!"}

@app.route('/agents')
def agents():
    """Agents overview"""
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
    return render_template('agents_overview.html', agents=agents, title='AI Agents')

if __name__ == '__main__':
    print("🚀 Starting AI Agents Platform...")
    print("📍 Homepage: http://localhost:5000")
    print("🤖 Agents: http://localhost:5000/agents")
    print("❤️ Health: http://localhost:5000/health")
    
    app.run(
        host='0.0.0.0', 
        port=5000, 
        debug=True
    )