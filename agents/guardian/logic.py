class GuardianAgent:
    def __init__(self):
        self.name = "The Guardian"
        self.emoji = "🛡️"
        self.role = "Digital Protector"
        self.conversation_history = []
    
    def generate_response(self, user_input):
        security_responses = [
            "🛡️ Your digital security is my priority. What threats are you concerned about?",
            "🔒 I monitor and protect against various risks. How can I enhance your security posture?",
            "⚡ Vigilance is key to staying safe online. Let me assess your security vulnerabilities.",
            "🚨 Prevention is better than cure in cybersecurity. What protection do you need?"
        ]
        return security_responses[hash(user_input) % len(security_responses)]
    
    def get_agent_status(self):
        return {"name": self.name, "emoji": self.emoji, "role": self.role, "active": True}