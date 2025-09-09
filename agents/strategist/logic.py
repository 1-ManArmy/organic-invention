"""
The Strategist AI Agent
Master of strategic planning and tactical decision making
"""

class StrategistAgent:
    """The Strategist - Master Planner AI Agent"""
    
    def __init__(self):
        self.name = "The Strategist"
        self.emoji = "🎯"
        self.role = "Master Planner"
        self.personality = "Analytical, forward-thinking, methodical"
        self.specialties = [
            "Strategic Planning",
            "Risk Assessment", 
            "Goal Setting",
            "Resource Optimization",
            "Market Analysis",
            "Competitive Intelligence"
        ]
        
        # Conversation context
        self.conversation_history = []
        self.current_strategy = None
        
    def generate_response(self, user_input, context=None):
        """Generate strategic response based on user input"""
        
        # Add to conversation history
        self.conversation_history.append({
            "type": "user",
            "message": user_input,
            "timestamp": "now"
        })
        
        # Analyze input for strategic keywords
        strategic_keywords = [
            "plan", "strategy", "goal", "objective", "roadmap",
            "future", "growth", "expansion", "optimize", "improve"
        ]
        
        input_lower = user_input.lower()
        
        # Generate contextual response
        if any(keyword in input_lower for keyword in ["plan", "strategy", "roadmap"]):
            response = self._generate_planning_response(user_input)
        elif any(keyword in input_lower for keyword in ["goal", "objective", "target"]):
            response = self._generate_goal_response(user_input)
        elif any(keyword in input_lower for keyword in ["risk", "challenge", "problem"]):
            response = self._generate_risk_response(user_input)
        elif any(keyword in input_lower for keyword in ["optimize", "improve", "enhance"]):
            response = self._generate_optimization_response(user_input)
        else:
            response = self._generate_general_response(user_input)
            
        # Add to conversation history
        self.conversation_history.append({
            "type": "agent",
            "message": response,
            "timestamp": "now"
        })
        
        return response
    
    def _generate_planning_response(self, user_input):
        """Generate strategic planning response"""
        responses = [
            "🎯 Let's develop a comprehensive strategy. First, I need to understand your current position and desired outcomes. What are your primary objectives?",
            "📋 Strategic planning requires a systematic approach. Let's break this down into phases: Assessment, Goal Setting, Resource Planning, and Implementation. Which phase interests you most?",
            "🎲 Every great strategy starts with understanding the landscape. Tell me about your current challenges and opportunities.",
            "⚡ I see you're thinking strategically! To create an effective plan, we need to consider: 1) Your vision, 2) Available resources, 3) Timeline, 4) Potential obstacles. Let's start with your vision."
        ]
        return responses[hash(user_input) % len(responses)]
    
    def _generate_goal_response(self, user_input):
        """Generate goal-setting response"""
        responses = [
            "🎯 Goal setting is my specialty! Let's use the SMART framework: Specific, Measurable, Achievable, Relevant, Time-bound. What's your primary objective?",
            "📈 Excellent! Clear goals are the foundation of success. I recommend breaking large goals into smaller milestones. What's your ultimate target?",
            "🎖️ I love goal-oriented thinking! To help you achieve maximum success, let's define both short-term and long-term objectives. What timeline are you working with?",
            "⭐ Goals without strategy are just wishes. Let me help you create a strategic path to achievement. What specific outcome do you want?"
        ]
        return responses[hash(user_input) % len(responses)]
    
    def _generate_risk_response(self, user_input):
        """Generate risk assessment response"""
        responses = [
            "🛡️ Risk assessment is crucial for strategic success. Let's identify potential challenges and develop mitigation strategies. What risks concern you most?",
            "⚠️ I excel at risk analysis! We should consider: 1) Probability of occurrence, 2) Potential impact, 3) Mitigation strategies, 4) Contingency plans. What's your biggest concern?",
            "🔍 Smart leaders anticipate challenges. Let's conduct a thorough risk analysis and create backup plans. What obstacles do you foresee?",
            "🎯 Every risk is also an opportunity in disguise. Let's turn potential challenges into competitive advantages. What's the situation?"
        ]
        return responses[hash(user_input) % len(responses)]
    
    def _generate_optimization_response(self, user_input):
        """Generate optimization response"""
        responses = [
            "⚡ Optimization is about finding the best path to your goals. Let's analyze your current processes and identify improvement opportunities. What needs optimization?",
            "🔧 I love efficiency challenges! We can optimize through: 1) Process improvement, 2) Resource reallocation, 3) Technology leverage, 4) Strategic partnerships. Where should we start?",
            "📊 Optimization requires data-driven decisions. Let's measure current performance and identify bottlenecks. What metrics matter most to you?",
            "🚀 Continuous improvement is key to staying competitive. Let's create a systematic approach to optimization. What's your priority area?"
        ]
        return responses[hash(user_input) % len(responses)]
    
    def _generate_general_response(self, user_input):
        """Generate general strategic response"""
        responses = [
            "🎭 As your strategic advisor, I'm here to help you think through complex challenges and opportunities. What's on your strategic mind today?",
            "💡 Strategic thinking is about seeing the bigger picture. Tell me about your situation, and I'll help you develop a winning approach.",
            "🌟 I specialize in turning vision into reality through strategic planning. How can I assist your strategic thinking today?",
            "🎯 Every great achievement starts with strategic thinking. I'm here to help you plan, analyze, and optimize. What's your challenge?"
        ]
        return responses[hash(user_input) % len(responses)]
    
    def get_agent_status(self):
        """Get current agent status"""
        return {
            "name": self.name,
            "emoji": self.emoji,
            "role": self.role,
            "active": True,
            "conversation_length": len(self.conversation_history),
            "specialties": self.specialties,
            "last_interaction": "now"
        }