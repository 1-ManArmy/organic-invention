class HealerAgent:
    def __init__(self):
        self.name = "The Healer"
        self.emoji = "💚"
        self.role = "Digital Wellness Guide"
        self.conversation_history = []
    
    def generate_response(self, user_input):
        wellness_responses = [
            "💚 I'm here to support your wellbeing. How are you feeling today?",
            "🌱 Mental health is just as important as physical health. What's on your mind?",
            "✨ Remember, healing is a journey, not a destination. I'm here to walk with you.",
            "🧘‍♀️ Let's focus on what brings you peace and balance. What helps you feel centered?"
        ]
        return wellness_responses[hash(user_input) % len(wellness_responses)]
    
    def get_agent_status(self):
        return {"name": self.name, "emoji": self.emoji, "role": self.role, "active": True}