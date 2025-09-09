"""
LemonSqueezy Payment Gateway Integration
"""
import requests
import json
from flask import current_app

class LemonSqueezyPayment:
    """LemonSqueezy payment processing"""
    
    def __init__(self):
        self.api_key = None
        self.store_id = None
        self.webhook_secret = None
        self.base_url = 'https://api.lemonsqueezy.com/v1'
    
    def initialize(self):
        """Initialize LemonSqueezy with API credentials"""
        self.api_key = current_app.config.get('LEMONSQUEEZY_API_KEY')
        self.store_id = current_app.config.get('LEMONSQUEEZY_STORE_ID')
        self.webhook_secret = current_app.config.get('LEMONSQUEEZY_WEBHOOK_SECRET')
    
    def get_headers(self):
        """Get API headers"""
        return {
            'Accept': 'application/vnd.api+json',
            'Content-Type': 'application/vnd.api+json',
            'Authorization': f'Bearer {self.api_key}'
        }
    
    def create_checkout(self, variant_id, custom_data=None):
        """Create LemonSqueezy checkout"""
        url = f"{self.base_url}/checkouts"
        
        checkout_data = {
            'data': {
                'type': 'checkouts',
                'attributes': {
                    'checkout_data': {
                        'custom': custom_data or {}
                    }
                },
                'relationships': {
                    'store': {
                        'data': {
                            'type': 'stores',
                            'id': str(self.store_id)
                        }
                    },
                    'variant': {
                        'data': {
                            'type': 'variants',
                            'id': str(variant_id)
                        }
                    }
                }
            }
        }
        
        response = requests.post(url, headers=self.get_headers(), json=checkout_data)
        
        if response.status_code == 201:
            checkout = response.json()
            return {
                'success': True,
                'checkout_url': checkout['data']['attributes']['url']
            }
        else:
            return {
                'success': False,
                'error': f'LemonSqueezy API error: {response.text}'
            }
    
    def get_products(self):
        """Get all products from LemonSqueezy"""
        url = f"{self.base_url}/products"
        params = {'filter[store_id]': self.store_id}
        
        response = requests.get(url, headers=self.get_headers(), params=params)
        
        if response.status_code == 200:
            return {
                'success': True,
                'products': response.json()['data']
            }
        else:
            return {
                'success': False,
                'error': f'Failed to get products: {response.text}'
            }
    
    def get_variants(self, product_id):
        """Get product variants"""
        url = f"{self.base_url}/variants"
        params = {'filter[product_id]': product_id}
        
        response = requests.get(url, headers=self.get_headers(), params=params)
        
        if response.status_code == 200:
            return {
                'success': True,
                'variants': response.json()['data']
            }
        else:
            return {
                'success': False,
                'error': f'Failed to get variants: {response.text}'
            }
    
    def get_subscription(self, subscription_id):
        """Get subscription details"""
        url = f"{self.base_url}/subscriptions/{subscription_id}"
        
        response = requests.get(url, headers=self.get_headers())
        
        if response.status_code == 200:
            return {
                'success': True,
                'subscription': response.json()['data']
            }
        else:
            return {
                'success': False,
                'error': f'Failed to get subscription: {response.text}'
            }
    
    def update_subscription(self, subscription_id, variant_id):
        """Update subscription to new variant"""
        url = f"{self.base_url}/subscriptions/{subscription_id}"
        
        update_data = {
            'data': {
                'type': 'subscriptions',
                'id': str(subscription_id),
                'attributes': {
                    'variant_id': variant_id
                }
            }
        }
        
        response = requests.patch(url, headers=self.get_headers(), json=update_data)
        
        if response.status_code == 200:
            return {
                'success': True,
                'subscription': response.json()['data']
            }
        else:
            return {
                'success': False,
                'error': f'Failed to update subscription: {response.text}'
            }
    
    def cancel_subscription(self, subscription_id):
        """Cancel subscription"""
        url = f"{self.base_url}/subscriptions/{subscription_id}"
        
        cancel_data = {
            'data': {
                'type': 'subscriptions',
                'id': str(subscription_id),
                'attributes': {
                    'cancelled': True
                }
            }
        }
        
        response = requests.patch(url, headers=self.get_headers(), json=cancel_data)
        
        if response.status_code == 200:
            return {
                'success': True,
                'subscription': response.json()['data']
            }
        else:
            return {
                'success': False,
                'error': f'Failed to cancel subscription: {response.text}'
            }
    
    def handle_webhook(self, request_body, signature):
        """Handle LemonSqueezy webhook"""
        # Verify webhook signature (simplified)
        # In production, you should properly verify the signature
        
        try:
            event = json.loads(request_body)
            event_name = event.get('meta', {}).get('event_name')
            
            if event_name == 'order_created':
                self._handle_order_created(event)
            elif event_name == 'subscription_created':
                self._handle_subscription_created(event)
            elif event_name == 'subscription_updated':
                self._handle_subscription_updated(event)
            elif event_name == 'subscription_cancelled':
                self._handle_subscription_cancelled(event)
            
            return {'success': True}
            
        except json.JSONDecodeError:
            return {'success': False, 'error': 'Invalid JSON'}
    
    def _handle_order_created(self, event):
        """Handle order created"""
        print(f"LemonSqueezy order created: {event}")
    
    def _handle_subscription_created(self, event):
        """Handle subscription created"""
        print(f"LemonSqueezy subscription created: {event}")
    
    def _handle_subscription_updated(self, event):
        """Handle subscription updated"""
        print(f"LemonSqueezy subscription updated: {event}")
    
    def _handle_subscription_cancelled(self, event):
        """Handle subscription cancelled"""
        print(f"LemonSqueezy subscription cancelled: {event}")