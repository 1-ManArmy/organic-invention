from flask import Blueprint, render_template, request, jsonify
from .logic import NavigatorAgent

navigator_bp = Blueprint('navigator', __name__)
navigator_agent = NavigatorAgent()

@navigator_bp.route('/')
def navigator_home():
    return render_template('agents/navigator.html', agent=navigator_agent.get_agent_status())

@navigator_bp.route('/chat', methods=['POST'])
def navigator_chat():
    data = request.get_json()
    response = navigator_agent.generate_response(data.get('message', ''))
    return jsonify({'response': response, 'agent': navigator_agent.name, 'emoji': navigator_agent.emoji})