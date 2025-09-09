"""
Strategist Agent Routes
"""
from flask import Blueprint, render_template, request, jsonify, session
from .logic import StrategistAgent

strategist_bp = Blueprint('strategist', __name__)

# Initialize agent instance
strategist_agent = StrategistAgent()

@strategist_bp.route('/')
def strategist_home():
    """Strategist agent homepage"""
    return render_template('agents/strategist.html', agent=strategist_agent.get_agent_status())

@strategist_bp.route('/chat', methods=['POST'])
def strategist_chat():
    """Handle chat with Strategist agent"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Generate response
        response = strategist_agent.generate_response(user_message)
        
        return jsonify({
            'response': response,
            'agent': strategist_agent.name,
            'emoji': strategist_agent.emoji,
            'timestamp': 'now'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@strategist_bp.route('/status')
def strategist_status():
    """Get Strategist agent status"""
    return jsonify(strategist_agent.get_agent_status())

@strategist_bp.route('/reset', methods=['POST'])
def strategist_reset():
    """Reset Strategist agent conversation"""
    strategist_agent.conversation_history = []
    strategist_agent.current_strategy = None
    
    return jsonify({
        'message': 'Strategist agent reset successfully',
        'status': strategist_agent.get_agent_status()
    })