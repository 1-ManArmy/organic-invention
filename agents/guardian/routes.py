from flask import Blueprint, render_template, request, jsonify
from .logic import GuardianAgent

guardian_bp = Blueprint('guardian', __name__)
guardian_agent = GuardianAgent()

@guardian_bp.route('/')
def guardian_home():
    return render_template('agents/guardian.html', agent=guardian_agent.get_agent_status())

@guardian_bp.route('/chat', methods=['POST'])
def guardian_chat():
    data = request.get_json()
    response = guardian_agent.generate_response(data.get('message', ''))
    return jsonify({'response': response, 'agent': guardian_agent.name, 'emoji': guardian_agent.emoji})