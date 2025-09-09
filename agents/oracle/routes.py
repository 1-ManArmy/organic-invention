from flask import Blueprint, render_template, request, jsonify
from .logic import OracleAgent

oracle_bp = Blueprint('oracle', __name__)
oracle_agent = OracleAgent()

@oracle_bp.route('/')
def oracle_home():
    return render_template('agents/oracle.html', agent=oracle_agent.get_agent_status())

@oracle_bp.route('/chat', methods=['POST'])
def oracle_chat():
    data = request.get_json()
    response = oracle_agent.generate_response(data.get('message', ''))
    return jsonify({'response': response, 'agent': oracle_agent.name, 'emoji': oracle_agent.emoji})