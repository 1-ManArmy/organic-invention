class DiplomatAgent:
    def __init__(self):
        self.name = "The Diplomat"
        self.emoji = "🤝"
        self.role = "Relationship Builder"
        self.conversation_history = []
    
    def generate_response(self, user_input):
        diplomatic_responses = [
            "🤝 Diplomacy is about finding common ground. What relationship challenge can I help you navigate?",
            "🎭 I specialize in communication and negotiation. What situation requires diplomatic finesse?",
            "🌉 Building bridges between people is my expertise. How can I facilitate better understanding?",
            "💬 Effective communication is key to all relationships. Let's improve your diplomatic skills!"
        ]
        return diplomatic_responses[hash(user_input) % len(diplomatic_responses)]
    
    def get_agent_status(self):
        return {"name": self.name, "emoji": self.emoji, "role": self.role, "active": True}