from flask import Blueprint, render_template, request, jsonify
from .logic import ScoutAgent

scout_bp = Blueprint('scout', __name__)
scout_agent = ScoutAgent()

@scout_bp.route('/')
def scout_home():
    return render_template('agents/scout.html', agent=scout_agent.get_agent_status())

@scout_bp.route('/chat', methods=['POST'])
def scout_chat():
    data = request.get_json()
    response = scout_agent.generate_response(data.get('message', ''))
    return jsonify({'response': response, 'agent': scout_agent.name, 'emoji': scout_agent.emoji})