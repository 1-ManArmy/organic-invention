"""
AI Agent Chat Interface
"""
from flask import Blueprint, render_template, request, jsonify, session
import json
import random
from datetime import datetime

# Create a simple chat blueprint for testing
chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

# Mock AI responses for demonstration
AGENT_RESPONSES = {
    'strategist': [
        "Let me analyze this strategic opportunity... Based on current market conditions, I recommend a three-phase approach.",
        "From a strategic perspective, we should consider the long-term implications and competitive advantages.",
        "This requires careful planning. Let me outline a comprehensive strategy for you."
    ],
    'healer': [
        "I sense you might be feeling overwhelmed. Let's take a moment to breathe and center ourselves.",
        "Your wellbeing is important. How are you feeling today? Let's work through this together.",
        "Remember, it's okay to take breaks. Mental health is just as important as physical health."
    ],
    'scout': [
        "I've been gathering intelligence on this topic. Here's what I've discovered...",
        "Let me scout out the best resources and information for you.",
        "My reconnaissance shows several interesting data points we should investigate."
    ]
}

@chat_bp.route('/<agent_id>')
def chat_interface(agent_id):
    """Chat interface for specific agent"""
    from agents import AGENTS_REGISTRY
    
    if agent_id not in AGENTS_REGISTRY:
        return "Agent not found", 404
    
    agent_info = AGENTS_REGISTRY[agent_id]
    return render_template('chat/interface.html', 
                         agent=agent_info, 
                         agent_id=agent_id,
                         title=f'Chat with {agent_info["name"]}')

@chat_bp.route('/<agent_id>/message', methods=['POST'])
def send_message(agent_id):
    """Send message to agent"""
    data = request.get_json()
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400
    
    # Mock AI response
    responses = AGENT_RESPONSES.get(agent_id, [
        "Interesting question! Let me think about that...",
        "That's a great point. Here's my perspective...",
        "I can help you with that. Let me analyze this..."
    ])
    
    ai_response = random.choice(responses)
    
    # In a real implementation, you would:
    # 1. Send user_message to your AI service (OpenAI, Anthropic, etc.)
    # 2. Get the AI response
    # 3. Store the conversation in the database
    # 4. Return the response
    
    return jsonify({
        'success': True,
        'response': ai_response,
        'timestamp': datetime.now().isoformat(),
        'agent': agent_id
    })

@chat_bp.route('/test')
def test_chat():
    """Test chat functionality"""
    return jsonify({
        'status': 'Chat system operational',
        'available_agents': list(AGENT_RESPONSES.keys()),
        'features': [
            'Real-time messaging',
            'Agent personality responses',
            'Message history',
            'Multi-agent support'
        ]
    })