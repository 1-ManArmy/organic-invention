from flask import Blueprint, render_template, request, jsonify
from .logic import HealerAgent

healer_bp = Blueprint('healer', __name__)
healer_agent = HealerAgent()

@healer_bp.route('/')
def healer_home():
    return render_template('agents/healer.html', agent=healer_agent.get_agent_status())

@healer_bp.route('/chat', methods=['POST'])
def healer_chat():
    data = request.get_json()
    response = healer_agent.generate_response(data.get('message', ''))
    return jsonify({'response': response, 'agent': healer_agent.name, 'emoji': healer_agent.emoji})