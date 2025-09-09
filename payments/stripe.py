"""
Stripe Payment Gateway Integration
"""
import stripe
from flask import current_app, request, jsonify
import json

class StripePayment:
    """Stripe payment processing"""
    
    def __init__(self):
        self.public_key = None
        self.secret_key = None
        self.webhook_secret = None
        
    def initialize(self):
        """Initialize Stripe with API keys"""
        self.public_key = current_app.config.get('STRIPE_PUBLIC_KEY')
        self.secret_key = current_app.config.get('STRIPE_SECRET_KEY')
        self.webhook_secret = current_app.config.get('STRIPE_WEBHOOK_SECRET')
        
        if self.secret_key:
            stripe.api_key = self.secret_key
    
    def create_payment_intent(self, amount, currency='usd', metadata=None):
        """Create Stripe payment intent"""
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Stripe uses cents
                currency=currency,
                metadata=metadata or {},
                automatic_payment_methods={
                    'enabled': True,
                }
            )
            
            return {
                'success': True,
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id
            }
            
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_subscription(self, customer_id, price_id, metadata=None):
        """Create Stripe subscription"""
        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{'price': price_id}],
                metadata=metadata or {},
                expand=['latest_invoice.payment_intent']
            )
            
            return {
                'success': True,
                'subscription_id': subscription.id,
                'client_secret': subscription.latest_invoice.payment_intent.client_secret
            }
            
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_customer(self, email, name=None, metadata=None):
        """Create Stripe customer"""
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata=metadata or {}
            )
            
            return {
                'success': True,
                'customer_id': customer.id
            }
            
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def handle_webhook(self, payload, sig_header):
        """Handle Stripe webhook"""
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, self.webhook_secret
            )
            
            # Handle different event types
            if event['type'] == 'payment_intent.succeeded':
                payment_intent = event['data']['object']
                self._handle_successful_payment(payment_intent)
                
            elif event['type'] == 'customer.subscription.created':
                subscription = event['data']['object']
                self._handle_subscription_created(subscription)
                
            elif event['type'] == 'customer.subscription.updated':
                subscription = event['data']['object']
                self._handle_subscription_updated(subscription)
                
            elif event['type'] == 'invoice.payment_failed':
                invoice = event['data']['object']
                self._handle_payment_failed(invoice)
            
            return {'success': True}
            
        except ValueError as e:
            return {'success': False, 'error': 'Invalid payload'}
        except stripe.error.SignatureVerificationError as e:
            return {'success': False, 'error': 'Invalid signature'}
    
    def _handle_successful_payment(self, payment_intent):
        """Handle successful payment"""
        # Update user's subscription or credits
        # This would typically update your database
        print(f"Payment succeeded: {payment_intent['id']}")
    
    def _handle_subscription_created(self, subscription):
        """Handle new subscription"""
        # Activate user's subscription
        print(f"Subscription created: {subscription['id']}")
    
    def _handle_subscription_updated(self, subscription):
        """Handle subscription update"""
        # Update user's subscription status
        print(f"Subscription updated: {subscription['id']}")
    
    def _handle_payment_failed(self, invoice):
        """Handle failed payment"""
        # Handle failed payment, possibly downgrade account
        print(f"Payment failed for invoice: {invoice['id']}")
    
    def get_prices(self):
        """Get all Stripe prices"""
        try:
            prices = stripe.Price.list(active=True)
            return {
                'success': True,
                'prices': prices.data
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e)
            }