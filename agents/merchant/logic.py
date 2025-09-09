class MerchantAgent:
    def __init__(self):
        self.name = "The Merchant"
        self.emoji = "💰"
        self.role = "Business Advisor"
        self.conversation_history = []
    
    def generate_response(self, user_input):
        business_responses = [
            "💰 Business success requires strategic thinking and smart decisions. What's your venture?",
            "📈 I analyze markets and identify opportunities. What business challenge are you facing?",
            "💼 From startups to enterprises, I help businesses thrive. What's your business model?",
            "🎯 Profit and purpose can align beautifully. Let's discuss your business strategy!"
        ]
        return business_responses[hash(user_input) % len(business_responses)]
    
    def get_agent_status(self):
        return {"name": self.name, "emoji": self.emoji, "role": self.role, "active": True}