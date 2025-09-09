class MessengerAgent:
    def __init__(self):
        self.name = "The Messenger"
        self.emoji = "📡"
        self.role = "Communication Hub"
        self.conversation_history = []
    
    def generate_response(self, user_input):
        communication_responses = [
            "📡 I facilitate seamless communication across all channels. What message needs delivering?",
            "💬 Clear communication prevents misunderstandings. How can I help coordinate your messages?",
            "🌐 I connect people and ideas efficiently. What communication challenge do you face?",
            "📬 From simple messages to complex coordination, I handle all communications!"
        ]
        return communication_responses[hash(user_input) % len(communication_responses)]
    
    def get_agent_status(self):
        return {"name": self.name, "emoji": self.emoji, "role": self.role, "active": True}