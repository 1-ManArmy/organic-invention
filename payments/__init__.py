"""
Payment Gateway Integration Module
"""
from payments.stripe import StripePayment
from payments.paypal import PayPalPayment
from payments.lemonsqueezy import LemonSqueezyPayment

def register_payment_routes(app):
    """Register payment routes with Flask app"""
    from payments.webhook import webhook_bp
    
    app.register_blueprint(webhook_bp, url_prefix='/webhooks')
    
    print("💳 Payment gateways registered: Stripe, PayPal, LemonSqueezy")

# Payment gateway instances
stripe_payment = StripePayment()
paypal_payment = PayPalPayment()
lemonsqueezy_payment = LemonSqueezyPayment()

# Pricing plans
PRICING_PLANS = {
    "free": {
        "name": "Free Explorer",
        "price": 0,
        "credits": 100,
        "agents_limit": 3,
        "features": [
            "Access to 3 AI Agents",
            "100 monthly conversations",
            "Basic support",
            "Community access"
        ]
    },
    "starter": {
        "name": "AI Enthusiast",
        "price": 9.99,
        "credits": 1000,
        "agents_limit": 7,
        "features": [
            "Access to 7 AI Agents",
            "1,000 monthly conversations",
            "Priority support",
            "Advanced analytics",
            "Custom agent personalities"
        ]
    },
    "pro": {
        "name": "AI Professional",
        "price": 29.99,
        "credits": 5000,
        "agents_limit": 13,
        "features": [
            "Access to all 13 AI Agents",
            "5,000 monthly conversations",
            "24/7 premium support",
            "Advanced analytics & insights",
            "Custom agent training",
            "API access",
            "White-label options"
        ]
    },
    "enterprise": {
        "name": "AI Enterprise", 
        "price": 99.99,
        "credits": "unlimited",
        "agents_limit": "unlimited",
        "features": [
            "Unlimited AI Agent access",
            "Unlimited conversations",
            "Dedicated success manager",
            "Custom integrations",
            "On-premise deployment",
            "Advanced security features",
            "SLA guarantees"
        ]
    }
}