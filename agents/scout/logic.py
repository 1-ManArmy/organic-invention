class ScoutAgent:
    def __init__(self):
        self.name = "The Scout"
        self.emoji = "🔍"
        self.role = "Information Hunter"
        self.conversation_history = []
    
    def generate_response(self, user_input):
        research_responses = [
            "🔍 I excel at finding information! What would you like me to investigate?",
            "📊 Let me gather intelligence on that topic. What specific data are you looking for?",
            "🎯 I'm your reconnaissance specialist. Give me a target and I'll scout it out!",
            "📋 Research is my passion! I can help you uncover insights and trends."
        ]
        return research_responses[hash(user_input) % len(research_responses)]
    
    def get_agent_status(self):
        return {"name": self.name, "emoji": self.emoji, "role": self.role, "active": True}