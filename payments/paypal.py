"""
PayPal Payment Gateway Integration
"""
import requests
import json
from flask import current_app

class PayPalPayment:
    """PayPal payment processing"""
    
    def __init__(self):
        self.client_id = None
        self.client_secret = None
        self.mode = 'sandbox'  # 'sandbox' or 'live'
        self.base_url = None
        self.access_token = None
    
    def initialize(self):
        """Initialize PayPal with API credentials"""
        self.client_id = current_app.config.get('PAYPAL_CLIENT_ID')
        self.client_secret = current_app.config.get('PAYPAL_CLIENT_SECRET')
        self.mode = current_app.config.get('PAYPAL_MODE', 'sandbox')
        
        if self.mode == 'sandbox':
            self.base_url = 'https://api-m.sandbox.paypal.com'
        else:
            self.base_url = 'https://api-m.paypal.com'
    
    def get_access_token(self):
        """Get PayPal access token"""
        url = f"{self.base_url}/v1/oauth2/token"
        
        headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en_US'
        }
        
        data = 'grant_type=client_credentials'
        
        response = requests.post(
            url, 
            headers=headers, 
            data=data, 
            auth=(self.client_id, self.client_secret)
        )
        
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data['access_token']
            return True
        else:
            return False
    
    def create_payment(self, amount, currency='USD', description='AI Agents Subscription'):
        """Create PayPal payment"""
        if not self.access_token:
            if not self.get_access_token():
                return {'success': False, 'error': 'Failed to get access token'}
        
        url = f"{self.base_url}/v2/checkout/orders"
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        
        payment_data = {
            'intent': 'CAPTURE',
            'purchase_units': [{
                'amount': {
                    'currency_code': currency,
                    'value': str(amount)
                },
                'description': description
            }],
            'application_context': {
                'return_url': 'https://your-domain.com/payment/success',
                'cancel_url': 'https://your-domain.com/payment/cancel'
            }
        }
        
        response = requests.post(url, headers=headers, json=payment_data)
        
        if response.status_code == 201:
            order_data = response.json()
            return {
                'success': True,
                'order_id': order_data['id'],
                'approval_url': next(link['href'] for link in order_data['links'] if link['rel'] == 'approve')
            }
        else:
            return {
                'success': False,
                'error': f'PayPal API error: {response.text}'
            }
    
    def capture_payment(self, order_id):
        """Capture PayPal payment"""
        if not self.access_token:
            if not self.get_access_token():
                return {'success': False, 'error': 'Failed to get access token'}
        
        url = f"{self.base_url}/v2/checkout/orders/{order_id}/capture"
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        
        response = requests.post(url, headers=headers)
        
        if response.status_code == 201:
            capture_data = response.json()
            return {
                'success': True,
                'capture_id': capture_data['id'],
                'status': capture_data['status']
            }
        else:
            return {
                'success': False,
                'error': f'PayPal capture error: {response.text}'
            }
    
    def create_subscription(self, plan_id, subscriber_info):
        """Create PayPal subscription"""
        if not self.access_token:
            if not self.get_access_token():
                return {'success': False, 'error': 'Failed to get access token'}
        
        url = f"{self.base_url}/v1/billing/subscriptions"
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
            'Accept': 'application/json',
            'Prefer': 'return=representation'
        }
        
        subscription_data = {
            'plan_id': plan_id,
            'subscriber': subscriber_info,
            'application_context': {
                'brand_name': 'OneLastAI',
                'locale': 'en-US',
                'shipping_preference': 'NO_SHIPPING',
                'user_action': 'SUBSCRIBE_NOW',
                'payment_method': {
                    'payer_selected': 'PAYPAL',
                    'payee_preferred': 'IMMEDIATE_PAYMENT_REQUIRED'
                },
                'return_url': 'https://your-domain.com/subscription/success',
                'cancel_url': 'https://your-domain.com/subscription/cancel'
            }
        }
        
        response = requests.post(url, headers=headers, json=subscription_data)
        
        if response.status_code == 201:
            subscription = response.json()
            return {
                'success': True,
                'subscription_id': subscription['id'],
                'approval_url': next(link['href'] for link in subscription['links'] if link['rel'] == 'approve')
            }
        else:
            return {
                'success': False,
                'error': f'PayPal subscription error: {response.text}'
            }
    
    def handle_webhook(self, request_body, headers):
        """Handle PayPal webhook"""
        # PayPal webhook verification would go here
        # For now, we'll just parse the event
        try:
            event = json.loads(request_body)
            event_type = event.get('event_type')
            
            if event_type == 'PAYMENT.CAPTURE.COMPLETED':
                self._handle_payment_completed(event)
            elif event_type == 'BILLING.SUBSCRIPTION.CREATED':
                self._handle_subscription_created(event)
            elif event_type == 'BILLING.SUBSCRIPTION.CANCELLED':
                self._handle_subscription_cancelled(event)
            
            return {'success': True}
            
        except json.JSONDecodeError:
            return {'success': False, 'error': 'Invalid JSON'}
    
    def _handle_payment_completed(self, event):
        """Handle completed payment"""
        print(f"PayPal payment completed: {event}")
    
    def _handle_subscription_created(self, event):
        """Handle subscription created"""
        print(f"PayPal subscription created: {event}")
    
    def _handle_subscription_cancelled(self, event):
        """Handle subscription cancelled"""
        print(f"PayPal subscription cancelled: {event}")