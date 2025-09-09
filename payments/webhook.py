"""
Payment Webhook Handlers
"""
from flask import Blueprint, request, jsonify
from .stripe import StripePayment
from .paypal import PayPalPayment
from .lemonsqueezy import LemonSqueezyPayment

webhook_bp = Blueprint('webhooks', __name__)

# Initialize payment processors
stripe_payment = StripePayment()
paypal_payment = PayPalPayment()
lemonsqueezy_payment = LemonSqueezyPayment()

@webhook_bp.route('/stripe', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhooks"""
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    
    result = stripe_payment.handle_webhook(payload, sig_header)
    
    if result['success']:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'error': result['error']}), 400

@webhook_bp.route('/paypal', methods=['POST'])
def paypal_webhook():
    """Handle PayPal webhooks"""
    payload = request.get_data(as_text=True)
    headers = dict(request.headers)
    
    result = paypal_payment.handle_webhook(payload, headers)
    
    if result['success']:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'error': result['error']}), 400

@webhook_bp.route('/lemonsqueezy', methods=['POST'])
def lemonsqueezy_webhook():
    """Handle LemonSqueezy webhooks"""
    payload = request.get_data(as_text=True)
    signature = request.headers.get('X-Signature')
    
    result = lemonsqueezy_payment.handle_webhook(payload, signature)
    
    if result['success']:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'error': result['error']}), 400

@webhook_bp.route('/test', methods=['GET'])
def test_webhooks():
    """Test webhook endpoint"""
    return jsonify({
        'message': 'Webhook endpoints are active',
        'endpoints': [
            '/webhooks/stripe',
            '/webhooks/paypal', 
            '/webhooks/lemonsqueezy'
        ]
    })