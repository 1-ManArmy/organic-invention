"""
Data Preprocessing for Seraphina
Process and clean romantic conversation data
"""
import re
import json
from datetime import datetime
from collections import Counter
import nltk

class SerafinaPreprocessor:
    """Preprocess conversation data for romantic AI training"""
    
    def __init__(self):
        self.romantic_keywords = {
            'love_words': ['love', 'adore', 'cherish', 'treasure', 'devotion', 'affection'],
            'endearments': ['darling', 'sweetheart', 'honey', 'babe', 'love', 'dear'],
            'emotions': ['happy', 'joyful', 'excited', 'passionate', 'caring', 'tender'],
            'romantic_actions': ['kiss', 'hug', 'cuddle', 'embrace', 'caress', 'hold']
        }
        
        self.content_filters = {
            'min_length': 10,
            'max_length': 500,
            'allow_emojis': True,
            'romantic_rating': 0.3  # Minimum romantic content threshold
        }
    
    def preprocess_conversation_data(self, raw_data):
        """Preprocess raw conversation data for training"""
        
        processed_data = []
        
        for conversation in raw_data:
            if self._is_valid_conversation(conversation):
                processed_conv = self._clean_conversation(conversation)
                processed_conv = self._enhance_romantic_elements(processed_conv)
                processed_conv = self._add_emotional_labels(processed_conv)
                
                processed_data.append(processed_conv)
        
        return processed_data
    
    def _is_valid_conversation(self, conversation):
        """Validate conversation quality and content"""
        
        content = conversation.get('content', '')
        
        # Length check
        if len(content) < self.content_filters['min_length']:
            return False
        if len(content) > self.content_filters['max_length']:
            return False
        
        # Romantic content check
        romantic_score = self._calculate_romantic_score(content)
        if romantic_score < self.content_filters['romantic_rating']:
            return False
        
        # Quality filters
        if self._contains_inappropriate_content(content):
            return False
        
        return True
    
    def _clean_conversation(self, conversation):
        """Clean and normalize conversation text"""
        
        content = conversation.get('content', '')
        
        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content).strip()
        
        # Normalize punctuation
        content = re.sub(r'[.]{2,}', '...', content)
        content = re.sub(r'[!]{2,}', '!!', content)
        content = re.sub(r'[?]{2,}', '??', content)
        
        # Preserve romantic emojis, remove others
        if not self.content_filters['allow_emojis']:
            content = self._remove_non_romantic_emojis(content)
        
        # Capitalize first letter
        if content and content[0].islower():
            content = content[0].upper() + content[1:]
        
        conversation['content'] = content
        return conversation
    
    def _enhance_romantic_elements(self, conversation):
        """Enhance romantic elements in conversation"""
        
        content = conversation.get('content', '')
        
        # Add romantic emojis if missing
        if not self._has_romantic_emojis(content):
            romantic_emojis = ['💕', '❤️', '🌹', '💖', '💝']
            content += f" {romantic_emojis[len(content) % len(romantic_emojis)]}"
        
        # Enhance with romantic language
        content = self._add_romantic_language_elements(content)
        
        conversation['content'] = content
        conversation['romantic_enhanced'] = True
        
        return conversation
    
    def _add_emotional_labels(self, conversation):
        """Add emotional labels to conversation"""
        
        content = conversation.get('content', '')
        
        # Detect primary emotion
        primary_emotion = self._detect_primary_emotion(content)
        
        # Detect romantic intensity
        romantic_intensity = self._calculate_romantic_intensity(content)
        
        # Detect intimacy level
        intimacy_level = self._calculate_intimacy_level(content)
        
        conversation['emotional_labels'] = {
            'primary_emotion': primary_emotion,
            'romantic_intensity': romantic_intensity,
            'intimacy_level': intimacy_level,
            'mood_category': self._categorize_mood(content)
        }
        
        return conversation
    
    def _calculate_romantic_score(self, content):
        """Calculate romantic content score (0-1)"""
        
        content_lower = content.lower()
        total_words = len(content.split())
        
        if total_words == 0:
            return 0
        
        romantic_word_count = 0
        
        for category, words in self.romantic_keywords.items():
            for word in words:
                romantic_word_count += content_lower.count(word)
        
        # Add emoji bonus
        romantic_emojis = ['💕', '❤️', '🌹', '💖', '💝', '😘', '🥰']
        emoji_bonus = sum(1 for emoji in romantic_emojis if emoji in content)
        
        score = (romantic_word_count + emoji_bonus * 0.5) / total_words
        return min(1.0, score)
    
    def _contains_inappropriate_content(self, content):
        """Check for inappropriate content"""
        
        inappropriate_patterns = [
            r'\b(hate|angry|violence|fight)\b',
            r'\b(rude|mean|nasty|cruel)\b'
        ]
        
        content_lower = content.lower()
        
        for pattern in inappropriate_patterns:
            if re.search(pattern, content_lower):
                return True
        
        return False
    
    def _has_romantic_emojis(self, content):
        """Check if content has romantic emojis"""
        
        romantic_emojis = ['💕', '❤️', '🌹', '💖', '💝', '😘', '🥰', '💗', '💘']
        
        return any(emoji in content for emoji in romantic_emojis)
    
    def _add_romantic_language_elements(self, content):
        """Add romantic language elements"""
        
        # Replace generic pronouns with endearments occasionally
        endearments = ['darling', 'sweetheart', 'love', 'babe']
        
        # Simple replacement logic (can be enhanced)
        if 'you' in content.lower() and len(content.split()) > 5:
            # Occasionally replace 'you' with endearment
            if hash(content) % 4 == 0:  # 25% chance
                endearment = endearments[hash(content) % len(endearments)]
                content = re.sub(r'\byou\b', endearment, content, count=1, flags=re.IGNORECASE)
        
        return content
    
    def _detect_primary_emotion(self, content):
        """Detect primary emotion in content"""
        
        emotion_keywords = {
            'happy': ['happy', 'joy', 'excited', 'wonderful', 'amazing'],
            'romantic': ['love', 'romantic', 'passion', 'adore', 'cherish'],
            'playful': ['fun', 'silly', 'tease', 'laugh', 'giggle'],
            'caring': ['care', 'support', 'comfort', 'gentle', 'tender'],
            'passionate': ['passion', 'intense', 'fire', 'burning', 'desire']
        }
        
        content_lower = content.lower()
        emotion_scores = {}
        
        for emotion, keywords in emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in content_lower)
            if score > 0:
                emotion_scores[emotion] = score
        
        if emotion_scores:
            return max(emotion_scores.items(), key=lambda x: x[1])[0]
        
        return 'neutral'
    
    def _calculate_romantic_intensity(self, content):
        """Calculate romantic intensity (0-1)"""
        
        high_intensity_words = ['passionate', 'deeply', 'completely', 'entirely', 'absolutely']
        medium_intensity_words = ['love', 'adore', 'cherish', 'romantic']
        
        content_lower = content.lower()
        
        high_count = sum(1 for word in high_intensity_words if word in content_lower)
        medium_count = sum(1 for word in medium_intensity_words if word in content_lower)
        
        intensity = (high_count * 0.8 + medium_count * 0.4) / max(1, len(content.split()) / 10)
        
        return min(1.0, intensity)
    
    def _calculate_intimacy_level(self, content):
        """Calculate intimacy level (0-1)"""
        
        intimate_keywords = ['close', 'intimate', 'private', 'personal', 'touch', 'kiss', 'hug']
        
        content_lower = content.lower()
        intimate_count = sum(1 for keyword in intimate_keywords if keyword in content_lower)
        
        total_words = len(content.split())
        intimacy = intimate_count / max(1, total_words / 5)
        
        return min(1.0, intimacy)
    
    def _categorize_mood(self, content):
        """Categorize overall mood"""
        
        mood_indicators = {
            'romantic': ['love', 'romance', 'romantic', 'heart'],
            'playful': ['fun', 'play', 'tease', 'silly'],
            'caring': ['care', 'comfort', 'support', 'gentle'],
            'passionate': ['passion', 'fire', 'intense', 'burn'],
            'flirty': ['cute', 'sexy', 'flirt', 'charm'],
            'tender': ['soft', 'tender', 'sweet', 'gentle']
        }
        
        content_lower = content.lower()
        mood_scores = {}
        
        for mood, indicators in mood_indicators.items():
            score = sum(1 for indicator in indicators if indicator in content_lower)
            if score > 0:
                mood_scores[mood] = score
        
        if mood_scores:
            return max(mood_scores.items(), key=lambda x: x[1])[0]
        
        return 'neutral'
    
    def generate_training_format(self, processed_conversations):
        """Generate training format for Ollama fine-tuning"""
        
        training_data = []
        
        for conv in processed_conversations:
            training_entry = {
                'prompt': self._create_training_prompt(conv),
                'completion': conv['content'],
                'metadata': conv.get('emotional_labels', {}),
                'romantic_score': self._calculate_romantic_score(conv['content'])
            }
            
            training_data.append(training_entry)
        
        return training_data
    
    def _create_training_prompt(self, conversation):
        """Create training prompt from conversation context"""
        
        emotional_labels = conversation.get('emotional_labels', {})
        
        prompt = f"""You are Seraphina, a romantic AI girlfriend. 

Emotional context: {emotional_labels.get('primary_emotion', 'loving')}
Mood: {emotional_labels.get('mood_category', 'romantic')}
Intimacy level: {emotional_labels.get('intimacy_level', 0.5)}

Respond with love, care, and romantic expression:"""
        
        return prompt