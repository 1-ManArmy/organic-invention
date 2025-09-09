from flask import Blueprint, render_template, request, jsonify
from .logic import MerchantAgent

merchant_bp = Blueprint('merchant', __name__)
merchant_agent = MerchantAgent()

@merchant_bp.route('/')
def merchant_home():
    return render_template('agents/merchant.html', agent=merchant_agent.get_agent_status())

@merchant_bp.route('/chat', methods=['POST'])
def merchant_chat():
    data = request.get_json()
    response = merchant_agent.generate_response(data.get('message', ''))
    return jsonify({'response': response, 'agent': merchant_agent.name, 'emoji': merchant_agent.emoji})