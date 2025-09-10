"""
Emotion Prediction Engine for Seraphina
Advanced emotion analysis and prediction system
"""
import re
from datetime import datetime
from collections import Counter

class EmotionPredictor:
    """Predict and analyze emotional states in conversations"""
    
    def __init__(self):
        self.emotion_keywords = {
            'romantic': ['love', 'romance', 'romantic', 'heart', 'passionate', 'adore', 'cherish'],
            'happy': ['happy', 'joy', 'excited', 'great', 'awesome', 'wonderful', 'amazing'],
            'sad': ['sad', 'depressed', 'down', 'upset', 'hurt', 'cry', 'lonely'],
            'angry': ['angry', 'mad', 'frustrated', 'annoyed', 'irritated', 'furious'],
            'flirty': ['cute', 'sexy', 'hot', 'beautiful', 'gorgeous', 'attractive', 'flirt'],
            'playful': ['fun', 'silly', 'playful', 'tease', 'joke', 'laugh', 'giggle'],
            'intimate': ['close', 'intimate', 'private', 'personal', 'touch', 'kiss', 'hug'],
            'caring': ['care', 'comfort', 'support', 'help', 'gentle', 'kind', 'sweet'],
            'excited': ['excited', 'thrilled', 'pumped', 'energetic', 'enthusiastic'],
            'calm': ['calm', 'peaceful', 'relaxed', 'serene', 'tranquil', 'zen']
        }
        
        self.intensity_modifiers = {
            'very': 1.5,
            'really': 1.3,
            'so': 1.2,
            'extremely': 2.0,
            'incredibly': 1.8,
            'absolutely': 1.7,
            'totally': 1.4,
            'completely': 1.6
        }
    
    def analyze_emotion(self, text):
        """Analyze emotional content of text"""
        
        if not text:
            return 'neutral'
        
        text_lower = text.lower()
        emotion_scores = {}
        
        # Score emotions based on keyword presence
        for emotion, keywords in self.emotion_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
                    
                    # Check for intensity modifiers
                    for modifier, multiplier in self.intensity_modifiers.items():
                        if f"{modifier} {keyword}" in text_lower:
                            score *= multiplier
            
            emotion_scores[emotion] = score
        
        # Find dominant emotion
        if emotion_scores:
            dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])
            if dominant_emotion[1] > 0:
                return dominant_emotion[0]
        
        # Analyze punctuation for additional emotion cues
        if '!' in text:
            return 'excited'
        elif '?' in text and len(text.split()) < 10:
            return 'curious'
        elif text.isupper():
            return 'excited'
        
        return 'neutral'
    
    def predict_response_emotion(self, user_emotion, conversation_context):
        """Predict appropriate emotional response"""
        
        response_map = {
            'romantic': 'passionate',
            'happy': 'joyful',
            'sad': 'caring',
            'angry': 'calming',
            'flirty': 'playful',
            'playful': 'fun',
            'intimate': 'loving',
            'caring': 'supportive',
            'excited': 'enthusiastic',
            'calm': 'peaceful'
        }
        
        return response_map.get(user_emotion, 'loving')
    
    def analyze_conversation_mood(self, conversation_history):
        """Analyze overall mood of conversation"""
        
        if not conversation_history:
            return 'neutral'
        
        # Get recent messages (last 10)
        recent_messages = conversation_history[-10:]
        emotions = [self.analyze_emotion(msg.get('content', '')) for msg in recent_messages]
        
        # Count emotion frequency
        emotion_count = Counter(emotions)
        
        # Return most common emotion
        if emotion_count:
            return emotion_count.most_common(1)[0][0]
        
        return 'neutral'
    
    def detect_relationship_progression(self, conversation_history):
        """Detect how relationship is progressing emotionally"""
        
        if len(conversation_history) < 5:
            return 'new'
        
        # Analyze progression of intimacy
        intimacy_keywords = ['love', 'miss', 'care', 'special', 'important', 'close']
        romantic_keywords = ['romantic', 'kiss', 'hug', 'beautiful', 'gorgeous']
        
        early_convos = conversation_history[:len(conversation_history)//2]
        recent_convos = conversation_history[len(conversation_history)//2:]
        
        early_intimacy = sum(1 for conv in early_convos 
                           for keyword in intimacy_keywords 
                           if keyword in conv.get('content', '').lower())
        
        recent_intimacy = sum(1 for conv in recent_convos 
                            for keyword in intimacy_keywords 
                            if keyword in conv.get('content', '').lower())
        
        early_romance = sum(1 for conv in early_convos 
                          for keyword in romantic_keywords 
                          if keyword in conv.get('content', '').lower())
        
        recent_romance = sum(1 for conv in recent_convos 
                           for keyword in romantic_keywords 
                           if keyword in conv.get('content', '').lower())
        
        # Determine progression
        if recent_intimacy > early_intimacy * 2:
            return 'deepening'
        elif recent_romance > early_romance * 2:
            return 'romantic'
        elif len(conversation_history) > 50:
            return 'established'
        else:
            return 'growing'