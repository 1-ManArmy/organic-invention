class TacticianAgent:
    def __init__(self):
        self.name = "The Tactician"
        self.emoji = "⚔️"
        self.role = "Problem Solver"
        self.conversation_history = []
    
    def generate_response(self, user_input):
        tactical_responses = [
            "⚔️ Every problem has a solution - I find the most effective approach. What challenge needs tackling?",
            "🎯 I excel at breaking down complex problems into manageable steps. What's your situation?",
            "🧩 Strategic problem-solving is my forte. Let me analyze your challenge and devise a solution.",
            "⚡ Quick thinking and decisive action win battles. What problem requires immediate attention?"
        ]
        return tactical_responses[hash(user_input) % len(tactical_responses)]
    
    def get_agent_status(self):
        return {"name": self.name, "emoji": self.emoji, "role": self.role, "active": True}