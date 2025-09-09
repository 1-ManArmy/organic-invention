from flask import Blueprint, render_template, request, jsonify
from .logic import BuilderAgent

builder_bp = Blueprint('builder', __name__)
builder_agent = BuilderAgent()

@builder_bp.route('/')
def builder_home():
    return render_template('agents/builder.html', agent=builder_agent.get_agent_status())

@builder_bp.route('/chat', methods=['POST'])
def builder_chat():
    data = request.get_json()
    response = builder_agent.generate_response(data.get('message', ''))
    return jsonify({'response': response, 'agent': builder_agent.name, 'emoji': builder_agent.emoji})