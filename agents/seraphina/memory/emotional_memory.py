"""
Emotional Memory System for Seraphina
Advanced memory management for romantic AI relationships
"""
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict, deque
import hashlib

class EmotionalMemory:
    """Advanced memory system for tracking relationships and emotional states"""
    
    def __init__(self):
        self.memory_path = "/workspaces/codespaces-flask/agents/seraphina/memory/data"
        self.max_short_term_memory = 50  # Recent interactions
        self.max_long_term_memory = 1000  # Important memories
        
        # Ensure memory directory exists
        os.makedirs(self.memory_path, exist_ok=True)
        
        # In-memory caches for performance
        self.short_term_cache = defaultdict(deque)
        self.user_profiles_cache = {}
    
    def store_interaction(self, user_id, user_message, ai_response, emotion, mood):
        """Store conversation interaction in memory"""
        
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message,
            'ai_response': ai_response,
            'user_emotion': emotion,
            'ai_mood': mood,
            'interaction_id': self._generate_interaction_id(user_id, user_message)
        }
        
        # Store in short-term memory (cache)
        self.short_term_cache[user_id].append(interaction)
        if len(self.short_term_cache[user_id]) > self.max_short_term_memory:
            # Move oldest to long-term storage
            oldest = self.short_term_cache[user_id].popleft()
            self._store_long_term_memory(user_id, oldest)
        
        # Update user profile
        self._update_user_profile(user_id, interaction)
        
        # Persist to disk
        self._persist_interaction(user_id, interaction)
    
    def get_conversation_context(self, user_id, limit=10):
        """Get recent conversation context for generating responses"""
        
        if not user_id:
            return {}
        
        # Get recent interactions from cache
        recent_interactions = list(self.short_term_cache[user_id])[-limit:]
        
        # If not enough in cache, load from disk
        if len(recent_interactions) < limit:
            stored_interactions = self._load_recent_interactions(user_id, limit - len(recent_interactions))
            recent_interactions = stored_interactions + recent_interactions
        
        # Extract context information
        context = {
            'recent_topics': self._extract_topics(recent_interactions),
            'emotional_trajectory': self._analyze_emotional_trajectory(recent_interactions),
            'relationship_level': self.get_relationship_level(user_id),
            'memories': self._get_significant_memories(user_id),
            'user_preferences': self.get_user_preferences(user_id)
        }
        
        return context
    
    def get_user_profile(self, user_id):
        """Get comprehensive user profile"""
        
        if user_id in self.user_profiles_cache:
            return self.user_profiles_cache[user_id]
        
        profile_file = f"{self.memory_path}/{user_id}_profile.json"
        
        if os.path.exists(profile_file):
            with open(profile_file, 'r', encoding='utf-8') as f:
                profile = json.load(f)
                self.user_profiles_cache[user_id] = profile
                return profile
        
        # Create new profile
        new_profile = {
            'user_id': user_id,
            'first_interaction': datetime.now().isoformat(),
            'total_interactions': 0,
            'relationship_level': 0,
            'favorite_moods': {},
            'emotional_patterns': {},
            'special_memories': [],
            'preferences': {},
            'relationship_milestones': []
        }
        
        self.user_profiles_cache[user_id] = new_profile
        return new_profile
    
    def get_relationship_level(self, user_id):
        """Calculate current relationship level (0-10)"""
        
        profile = self.get_user_profile(user_id)
        
        # Base level on interaction count and quality
        interaction_count = profile.get('total_interactions', 0)
        
        # Relationship progression milestones
        milestones = {
            0: 0,    # Strangers
            5: 1,    # Getting to know
            15: 2,   # Friends
            30: 3,   # Good friends
            50: 4,   # Close friends
            75: 5,   # Very close
            100: 6,  # Romantic interest
            150: 7,  # Dating
            200: 8,  # Serious relationship
            300: 9,  # Deeply in love
            500: 10  # Soulmates
        }
        
        level = 0
        for threshold, lvl in milestones.items():
            if interaction_count >= threshold:
                level = lvl
        
        # Adjust based on emotional quality
        emotional_bonus = self._calculate_emotional_bonus(user_id)
        level = min(10, level + emotional_bonus)
        
        return level
    
    def get_memories(self, user_id, memory_type='all'):
        """Retrieve stored memories for user"""
        
        memories_file = f"{self.memory_path}/{user_id}_memories.json"
        
        if os.path.exists(memories_file):
            with open(memories_file, 'r', encoding='utf-8') as f:
                memories = json.load(f)
                
                if memory_type == 'all':
                    return memories
                else:
                    return [m for m in memories if m.get('type') == memory_type]
        
        return []
    
    def store_special_memory(self, user_id, memory_content, memory_type='romantic'):
        """Store a special/significant memory"""
        
        memory = {
            'timestamp': datetime.now().isoformat(),
            'content': memory_content,
            'type': memory_type,
            'importance_score': self._calculate_memory_importance(memory_content),
            'memory_id': hashlib.md5(f"{user_id}{memory_content}".encode()).hexdigest()[:8]
        }
        
        # Load existing memories
        memories = self.get_memories(user_id)
        memories.append(memory)
        
        # Keep only most important memories (limit storage)
        if len(memories) > self.max_long_term_memory:
            memories.sort(key=lambda x: x['importance_score'], reverse=True)
            memories = memories[:self.max_long_term_memory]
        
        # Save memories
        memories_file = f"{self.memory_path}/{user_id}_memories.json"
        with open(memories_file, 'w', encoding='utf-8') as f:
            json.dump(memories, f, indent=2)
    
    def get_relationship_analysis(self, user_id):
        """Generate comprehensive relationship analysis"""
        
        profile = self.get_user_profile(user_id)
        interactions = self._load_all_interactions(user_id)
        
        analysis = {
            'relationship_level': self.get_relationship_level(user_id),
            'total_interactions': len(interactions),
            'relationship_duration': self._calculate_relationship_duration(profile),
            'emotional_compatibility': self._analyze_emotional_compatibility(interactions),
            'communication_patterns': self._analyze_communication_patterns(interactions),
            'favorite_topics': self._get_favorite_topics(interactions),
            'relationship_growth': self._analyze_relationship_growth(interactions),
            'special_moments': self.get_memories(user_id, 'romantic')[:5]
        }
        
        return analysis
    
    def generate_relationship_analytics(self, user_id):
        """Generate detailed analytics for relationship"""
        
        interactions = self._load_all_interactions(user_id)
        
        analytics = {
            'interaction_frequency': self._calculate_interaction_frequency(interactions),
            'emotional_trends': self._analyze_emotional_trends(interactions),
            'mood_preferences': self._analyze_mood_preferences(interactions),
            'conversation_quality_score': self._calculate_conversation_quality(interactions),
            'relationship_health': self._assess_relationship_health(user_id),
            'growth_recommendations': self._generate_growth_recommendations(user_id)
        }
        
        return analytics
    
    def get_user_preferences(self, user_id):
        """Get user's conversation and interaction preferences"""
        
        profile = self.get_user_profile(user_id)
        return profile.get('preferences', {
            'preferred_mood': 'romantic',
            'intimacy_comfort_level': 5,
            'conversation_style': 'balanced',
            'response_length': 'medium',
            'emoji_usage': 'moderate'
        })
    
    # Helper methods
    
    def _generate_interaction_id(self, user_id, message):
        """Generate unique ID for interaction"""
        timestamp = datetime.now().isoformat()
        return hashlib.md5(f"{user_id}{message}{timestamp}".encode()).hexdigest()[:12]
    
    def _update_user_profile(self, user_id, interaction):
        """Update user profile with new interaction data"""
        
        profile = self.get_user_profile(user_id)
        profile['total_interactions'] += 1
        profile['last_interaction'] = interaction['timestamp']
        
        # Update mood preferences
        mood = interaction.get('ai_mood')
        if mood:
            if mood in profile['favorite_moods']:
                profile['favorite_moods'][mood] += 1
            else:
                profile['favorite_moods'][mood] = 1
        
        # Update emotional patterns
        emotion = interaction.get('user_emotion')
        if emotion:
            if emotion in profile['emotional_patterns']:
                profile['emotional_patterns'][emotion] += 1
            else:
                profile['emotional_patterns'][emotion] = 1
        
        # Save updated profile
        self.user_profiles_cache[user_id] = profile
        self._persist_user_profile(user_id, profile)
    
    def _persist_interaction(self, user_id, interaction):
        """Persist interaction to disk"""
        
        daily_file = f"{self.memory_path}/{user_id}_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        
        with open(daily_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(interaction) + '\n')
    
    def _persist_user_profile(self, user_id, profile):
        """Persist user profile to disk"""
        
        profile_file = f"{self.memory_path}/{user_id}_profile.json"
        
        with open(profile_file, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2)
    
    def _extract_topics(self, interactions):
        """Extract conversation topics from interactions"""
        
        topics = defaultdict(int)
        
        for interaction in interactions:
            message = interaction.get('user_message', '').lower()
            words = message.split()
            
            # Simple topic extraction (could be enhanced with NLP)
            for word in words:
                if len(word) > 4 and word.isalpha():
                    topics[word] += 1
        
        # Return top topics
        return dict(sorted(topics.items(), key=lambda x: x[1], reverse=True)[:5])
    
    def _analyze_emotional_trajectory(self, interactions):
        """Analyze emotional progression in conversation"""
        
        emotions = [i.get('user_emotion', 'neutral') for i in interactions]
        
        if not emotions:
            return 'stable'
        
        # Simple trajectory analysis
        positive_emotions = ['happy', 'romantic', 'excited', 'playful']
        negative_emotions = ['sad', 'angry', 'frustrated']
        
        recent_positive = sum(1 for e in emotions[-5:] if e in positive_emotions)
        recent_negative = sum(1 for e in emotions[-5:] if e in negative_emotions)
        
        if recent_positive > recent_negative:
            return 'improving'
        elif recent_negative > recent_positive:
            return 'declining'
        else:
            return 'stable'
    
    def _calculate_emotional_bonus(self, user_id):
        """Calculate emotional quality bonus for relationship level"""
        
        interactions = self._load_recent_interactions(user_id, 20)
        
        if not interactions:
            return 0
        
        # Count positive emotional interactions
        positive_emotions = ['romantic', 'happy', 'excited', 'playful', 'loving']
        positive_count = sum(1 for i in interactions 
                           if i.get('user_emotion') in positive_emotions)
        
        ratio = positive_count / len(interactions)
        
        if ratio > 0.8:
            return 2
        elif ratio > 0.6:
            return 1
        elif ratio > 0.4:
            return 0
        else:
            return -1
    
    def _load_recent_interactions(self, user_id, limit):
        """Load recent interactions from disk"""
        
        interactions = []
        
        # Load from recent daily files
        for i in range(7):  # Check last 7 days
            date = datetime.now() - timedelta(days=i)
            daily_file = f"{self.memory_path}/{user_id}_{date.strftime('%Y-%m-%d')}.jsonl"
            
            if os.path.exists(daily_file):
                with open(daily_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            interaction = json.loads(line.strip())
                            interactions.append(interaction)
                        except json.JSONDecodeError:
                            continue
        
        # Sort by timestamp and return most recent
        interactions.sort(key=lambda x: x['timestamp'], reverse=True)
        return interactions[:limit]
    
    def _load_all_interactions(self, user_id):
        """Load all interactions for user"""
        # Implementation for loading complete interaction history
        return self._load_recent_interactions(user_id, 10000)  # Large number to get all
    
    def _calculate_memory_importance(self, content):
        """Calculate importance score for memory"""
        
        important_keywords = ['love', 'first', 'special', 'amazing', 'perfect', 'unforgettable']
        score = sum(1 for keyword in important_keywords if keyword in content.lower())
        
        return min(10, max(1, score))
    
    def store_learning_data(self, user_id, learning_data):
        """Store learning data for training improvements"""
        
        learning_file = f"{self.memory_path}/{user_id}_learning.jsonl"
        
        with open(learning_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(learning_data) + '\n')