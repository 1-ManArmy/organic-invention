from flask import Blueprint, render_template, request, jsonify
from .logic import AnalystAgent

analyst_bp = Blueprint('analyst', __name__)
analyst_agent = AnalystAgent()

@analyst_bp.route('/')
def analyst_home():
    return render_template('agents/analyst.html', agent=analyst_agent.get_agent_status())

@analyst_bp.route('/chat', methods=['POST'])
def analyst_chat():
    data = request.get_json()
    response = analyst_agent.generate_response(data.get('message', ''))
    return jsonify({'response': response, 'agent': analyst_agent.name, 'emoji': analyst_agent.emoji})