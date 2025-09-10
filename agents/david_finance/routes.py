"""
David - Financial Advisor & Investment Guide Routes
"""
from flask import Blueprint, render_template, request, jsonify, session
from datetime import datetime
import json

david_finance_bp = Blueprint('david_finance', __name__)

@david_finance_bp.route('/')
def david_finance_home():
    """David Finance main page"""
    user_profile = session.get('user_profile', {
        'session_count': 0,
        'experience_level': 'Beginner',
        'progress_level': 0
    })
    
    return render_template('agents/david_finance/david_finance.html',
                         title="David - Financial Advisor & Investment Guide",
                         user_profile=user_profile)

@david_finance_bp.route('/chat', methods=['POST'])
def david_finance_chat():
    """Handle chat messages with David"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        mood = data.get('mood', 'analytical')
        mode = data.get('mode', 'text')
        
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['invest', 'portfolio', 'stock', 'market']):
            response = "Excellent! I thrive on investment analysis. 📊 Let me help you build a diversified portfolio that aligns with your risk tolerance and financial goals. Market conditions are always changing, but solid fundamentals and strategic thinking create lasting wealth."
        elif any(word in message_lower for word in ['budget', 'save', 'expense', 'money']):
            response = "Smart budgeting is the foundation of financial success! 💰 Let's analyze your income, expenses, and identify opportunities to optimize your cash flow. Every dollar saved is a dollar that can work for you through strategic investments."
        elif any(word in message_lower for word in ['retirement', 'plan', 'future', 'goal']):
            response = "Strategic financial planning is crucial for long-term success! Let's approach this methodically - I'll analyze your current situation, project future needs, and develop a comprehensive plan based on solid financial principles and risk management."
        elif any(word in message_lower for word in ['analysis', 'data', 'trend', 'research']):
            response = "Data-driven decision making is my specialty! I can process market data, identify trends, perform statistical analysis, and generate actionable insights for informed financial decisions. What specific metrics would you like me to analyze?"
        else:
            mood_responses = {
                'analytical': f"Let me provide a thorough analysis of '{message}'. I'll examine all variables and present data-driven recommendations.",
                'confident': f"Absolutely confident we can address '{message}' with strategic planning and sound financial principles!",
                'strategic': f"Taking a strategic approach to '{message}'. Let's assess risks, opportunities, and develop a winning plan.",
                'cautious': f"I appreciate your question about '{message}'. Let's proceed carefully with thorough risk assessment.",
                'optimistic': f"The opportunities around '{message}' look promising! Let's explore the potential with calculated optimism.",
                'realistic': f"Approaching '{message}' with realistic expectations and practical solutions based on market realities."
            }
            response = mood_responses.get(mood, "Ready to dive deep into financial analysis. I'll provide you with data-driven insights and logical solutions backed by thorough research. 📈")
        
        if 'user_profile' not in session:
            session['user_profile'] = {'session_count': 0}
        session['user_profile']['session_count'] = session['user_profile'].get('session_count', 0) + 1
        
        return jsonify({
            'success': True,
            'message': response,
            'mood': mood,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@david_finance_bp.route('/save-session', methods=['POST'])
def save_session():
    """Save chat session"""
    try:
        session_data = request.get_json()
        session['david_finance_session'] = session_data
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500