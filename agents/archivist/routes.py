from flask import Blueprint, render_template, request, jsonify
from .logic import ArchivistAgent

archivist_bp = Blueprint('archivist', __name__)
archivist_agent = ArchivistAgent()

@archivist_bp.route('/')
def archivist_home():
    return render_template('agents/archivist.html', agent=archivist_agent.get_agent_status())

@archivist_bp.route('/chat', methods=['POST'])
def archivist_chat():
    data = request.get_json()
    response = archivist_agent.generate_response(data.get('message', ''))
    return jsonify({'response': response, 'agent': archivist_agent.name, 'emoji': archivist_agent.emoji})