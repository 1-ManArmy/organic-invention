class OracleAgent:
    def __init__(self):
        self.name = "The Oracle"
        self.emoji = "🔮"
        self.role = "Future Insights"
        self.conversation_history = []
    
    def generate_response(self, user_input):
        prophetic_responses = [
            "🔮 I see patterns others miss and predict future trends. What future concerns you?",
            "✨ The future is shaped by present decisions. What path are you considering?",
            "🌟 I analyze data to reveal tomorrow's possibilities. What predictions do you seek?",
            "🎭 Wisdom comes from understanding cycles and patterns. What future do you envision?"
        ]
        return prophetic_responses[hash(user_input) % len(prophetic_responses)]
    
    def get_agent_status(self):
        return {"name": self.name, "emoji": self.emoji, "role": self.role, "active": True}