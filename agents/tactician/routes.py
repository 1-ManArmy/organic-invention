from flask import Blueprint, render_template, request, jsonify
from .logic import TacticianAgent

tactician_bp = Blueprint('tactician', __name__)
tactician_agent = TacticianAgent()

@tactician_bp.route('/')
def tactician_home():
    return render_template('agents/tactician.html', agent=tactician_agent.get_agent_status())

@tactician_bp.route('/chat', methods=['POST'])
def tactician_chat():
    data = request.get_json()
    response = tactician_agent.generate_response(data.get('message', ''))
    return jsonify({'response': response, 'agent': tactician_agent.name, 'emoji': tactician_agent.emoji})