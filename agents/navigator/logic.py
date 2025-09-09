class NavigatorAgent:
    def __init__(self):
        self.name = "The Navigator"
        self.emoji = "🧭"
        self.role = "Path Finder"
        self.conversation_history = []
    
    def generate_response(self, user_input):
        navigation_responses = [
            "🧭 I help you find the right path forward. Where do you want to go?",
            "🗺️ Every journey needs a guide. Let me help you navigate your challenges!",
            "⭐ I use wisdom and experience to show you the way. What destination do you seek?",
            "🚀 The best routes often aren't the most obvious ones. Let me chart your course!"
        ]
        return navigation_responses[hash(user_input) % len(navigation_responses)]
    
    def get_agent_status(self):
        return {"name": self.name, "emoji": self.emoji, "role": self.role, "active": True}