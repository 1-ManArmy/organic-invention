from flask import Blueprint, render_template, request, jsonify
from .logic import DiplomatAgent

diplomat_bp = Blueprint('diplomat', __name__)
diplomat_agent = DiplomatAgent()

@diplomat_bp.route('/')
def diplomat_home():
    return render_template('agents/diplomat.html', agent=diplomat_agent.get_agent_status())

@diplomat_bp.route('/chat', methods=['POST'])
def diplomat_chat():
    data = request.get_json()
    response = diplomat_agent.generate_response(data.get('message', ''))
    return jsonify({'response': response, 'agent': diplomat_agent.name, 'emoji': diplomat_agent.emoji})