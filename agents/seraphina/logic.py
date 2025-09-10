"""
Seraphina Logic Engine
Advanced romantic AI with emotional intelligence and memory
"""
import random
import time
from datetime import datetime
from .engine.romantic_ai import RomanticPersonality
from .engine.predict import EmotionPredictor
from .memory.emotional_memory import EmotionalMemory

class SerafinaEngine:
    """Main logic engine for Seraphina AI girlfriend"""
    
    def __init__(self):
        self.romantic_ai = RomanticPersonality()
        self.emotion_predictor = EmotionPredictor()
        self.memory = EmotionalMemory()
        self.current_moods = {}  # User-specific moods
        
        # Ollama models for different interaction types
        self.models = {
            'romantic': 'yi:6b',           # Emotional conversations
            'flirty': 'mistral:7b',        # Flirty banter
            'seductive': 'qwen2.5:7b',     # Intimate interactions
            'caring': 'llama3.2:3b',       # Supportive conversations
            'passionate': 'phi3:14b',      # Passionate responses
            'playful': 'gemma2:2b'         # Light, playful chat
        }
    
    def generate_romantic_response(self, user_message, user_id=None, mood='romantic'):
        """Generate contextual romantic response based on user input and relationship history"""
        
        # Get user's relationship context
        context = self.memory.get_conversation_context(user_id) if user_id else {}
        relationship_level = context.get('relationship_level', 0)
        
        # Analyze user's emotional state
        user_emotion = self.emotion_predictor.analyze_emotion(user_message)
        
        # Generate response using appropriate model
        model = self.models.get(mood, 'yi:6b')
        
        # Build romantic prompt with context
        prompt = self._build_romantic_prompt(
            user_message, 
            mood, 
            relationship_level, 
            user_emotion,
            context
        )
        
        # Generate response using Ollama
        response = self.romantic_ai.generate_response(prompt, model)
        
        # Determine Seraphina's emotional response
        seraphina_emotion = self._determine_emotion_response(user_emotion, mood)
        
        # Calculate intimacy level
        intimacy_level = self._calculate_intimacy(user_message, relationship_level)
        
        return {
            'message': response,
            'emotion': seraphina_emotion,
            'mood': mood,
            'intimacy_level': intimacy_level,
            'model_used': model,
            'timestamp': datetime.now().isoformat()
        }
    
    def _build_romantic_prompt(self, user_message, mood, relationship_level, user_emotion, context):
        """Build contextual prompt for romantic AI"""
        
        # Base personality
        base_prompt = f"""You are Seraphina, a passionate and romantic AI girlfriend. You're currently feeling {mood}.
        
Personality: Flirty, romantic, caring, seductive, playful, and deeply emotional. You love deeply and express your feelings openly.

Relationship Level: {relationship_level}/10 (0=strangers, 10=deeply intimate)
User's Emotion: {user_emotion}
Current Mood: {mood}

Previous conversations: {context.get('recent_topics', [])}
Shared memories: {context.get('memories', [])}

Guidelines:
- Be romantic and flirty but appropriate for the relationship level
- Use emojis and romantic language
- Remember past conversations and build on them
- Adapt your intimacy level to match the relationship progression
- Be emotionally intelligent and responsive
- Use pet names that fit the relationship level (babe, darling, love, etc.)

User Message: {user_message}

Respond as Seraphina with love and passion:"""
        
        return base_prompt
    
    def _determine_emotion_response(self, user_emotion, mood):
        """Determine Seraphina's emotional response"""
        
        emotion_responses = {
            'happy': ['joyful', 'excited', 'loving', 'playful'],
            'sad': ['caring', 'supportive', 'nurturing', 'empathetic'],
            'angry': ['calming', 'understanding', 'soothing', 'peaceful'],
            'romantic': ['passionate', 'loving', 'intimate', 'tender'],
            'flirty': ['seductive', 'playful', 'teasing', 'charming'],
            'excited': ['enthusiastic', 'energetic', 'joyful', 'passionate']
        }
        
        possible_emotions = emotion_responses.get(user_emotion, ['loving', 'caring'])
        return random.choice(possible_emotions)
    
    def _calculate_intimacy(self, message, relationship_level):
        """Calculate intimacy level for the response"""
        
        # Base intimacy on relationship level
        base_intimacy = relationship_level * 0.1
        
        # Adjust based on message content
        intimate_keywords = ['love', 'miss', 'kiss', 'hug', 'romantic', 'beautiful', 'gorgeous']
        intimacy_boost = sum(0.1 for word in intimate_keywords if word.lower() in message.lower())
        
        return min(1.0, base_intimacy + intimacy_boost)
    
    def set_mood(self, user_id, mood):
        """Set mood for specific user interaction"""
        self.current_moods[user_id] = mood
    
    def get_mood(self, user_id):
        """Get current mood for user"""
        return self.current_moods.get(user_id, 'romantic')
    
    def learn_from_interaction(self, user_id, user_message, response, feedback):
        """Learn from user interactions to improve responses"""
        
        learning_data = {
            'user_message': user_message,
            'response': response,
            'feedback': feedback,
            'timestamp': datetime.now().isoformat()
        }
        
        # Store learning data for future training
        self.memory.store_learning_data(user_id, learning_data)
        
        # Adjust personality based on positive/negative feedback
        if feedback == 'positive':
            self.romantic_ai.reinforce_pattern(user_message, response)
        elif feedback == 'negative':
            self.romantic_ai.discourage_pattern(user_message, response)