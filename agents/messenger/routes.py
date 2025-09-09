from flask import Blueprint, render_template, request, jsonify
from .logic import MessengerAgent

messenger_bp = Blueprint('messenger', __name__)
messenger_agent = MessengerAgent()

@messenger_bp.route('/')
def messenger_home():
    return render_template('agents/messenger.html', agent=messenger_agent.get_agent_status())

@messenger_bp.route('/chat', methods=['POST'])
def messenger_chat():
    data = request.get_json()
    response = messenger_agent.generate_response(data.get('message', ''))
    return jsonify({'response': response, 'agent': messenger_agent.name, 'emoji': messenger_agent.emoji})