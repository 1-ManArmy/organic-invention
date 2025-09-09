class AnalystAgent:
    def __init__(self):
        self.name = "The Analyst"
        self.emoji = "📊"
        self.role = "Data Detective"
        self.conversation_history = []
    
    def generate_response(self, user_input):
        analytical_responses = [
            "📊 Data tells stories - I help you understand what yours is saying. What data needs analysis?",
            "🔍 I turn raw data into actionable insights. What metrics are you tracking?",
            "📈 Pattern recognition and trend analysis are my specialties. What data puzzles you?",
            "💡 Every dataset holds valuable insights waiting to be discovered. What shall we analyze?"
        ]
        return analytical_responses[hash(user_input) % len(analytical_responses)]
    
    def get_agent_status(self):
        return {"name": self.name, "emoji": self.emoji, "role": self.role, "active": True}