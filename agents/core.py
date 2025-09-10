"""
AI Agents System - Core Components
Advanced multi-agent platform with Ollama integration
"""

import os
import yaml
from datetime import datetime
from typing import Dict, List, Optional
import requests
import json

class AgentCore:
    """Base class for all AI agents"""
    
    def __init__(self, agent_name: str, config_path: str = None):
        self.agent_name = agent_name
        self.config = self.load_config(config_path)
        self.ollama_url = "http://localhost:11434"
        self.memory_system = None
        self.emotion_engine = None
        
        # Initialize core systems
        self.initialize_systems()
    
    def load_config(self, config_path: str = None) -> Dict:
        """Load agent configuration"""
        if not config_path:
            config_path = f"/workspaces/codespaces-flask/agents/{self.agent_name}/config.yaml"
        
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """Default configuration for agents"""
        return {
            'models': {
                'primary': 'yi:6b',
                'fallback': 'llama3.2:3b'
            },
            'personality': {
                'temperature': 0.8,
                'top_p': 0.9,
                'max_tokens': 200
            },
            'memory': {
                'short_term_limit': 50,
                'long_term_limit': 1000
            },
            'learning': {
                'enabled': True,
                'feedback_learning': True
            }
        }
    
    def initialize_systems(self):
        """Initialize core agent systems"""
        # Memory System
        self.memory_system = MemorySystem(self.agent_name)
        
        # Emotion Engine
        self.emotion_engine = EmotionEngine(self.agent_name)
        
        # Performance Analytics
        self.analytics = PerformanceAnalytics(self.agent_name)
    
    def generate_response(self, prompt: str, context: Dict = None, model: str = None) -> str:
        """Generate response using Ollama"""
        
        if not model:
            model = self.config['models']['primary']
        
        try:
            # Build enhanced prompt with context
            enhanced_prompt = self.build_contextual_prompt(prompt, context)
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": enhanced_prompt,
                    "stream": False,
                    "options": self.config.get('personality', {})
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                return self.fallback_response()
                
        except Exception as e:
            print(f"Error generating response: {e}")
            return self.fallback_response()
    
    def build_contextual_prompt(self, prompt: str, context: Dict = None) -> str:
        """Build contextual prompt with agent personality and memory"""
        
        base_personality = f"You are {self.agent_name}, a specialized AI agent."
        
        if context:
            memory_context = context.get('memory', [])
            emotional_context = context.get('emotion', 'neutral')
            
            enhanced_prompt = f"{base_personality}\n\nContext: {memory_context}\nEmotion: {emotional_context}\n\nUser: {prompt}\n\nResponse:"
        else:
            enhanced_prompt = f"{base_personality}\n\nUser: {prompt}\n\nResponse:"
        
        return enhanced_prompt
    
    def fallback_response(self) -> str:
        """Fallback response when AI generation fails"""
        return "I'm having some technical difficulties right now. Let me try again in a moment."

class MemorySystem:
    """Advanced memory management for agents"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.memory_path = f"/workspaces/codespaces-flask/agents/{agent_name}/memory/data"
        os.makedirs(self.memory_path, exist_ok=True)
        
        # Memory types
        self.short_term = []  # Recent interactions
        self.long_term = {}   # Important memories
        self.episodic = {}    # Specific episodes/conversations
        self.semantic = {}    # General knowledge/facts
    
    def store_interaction(self, user_id: str, interaction: Dict):
        """Store user interaction in memory"""
        
        memory_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'content': interaction,
            'importance_score': self.calculate_importance(interaction)
        }
        
        # Store in short-term memory
        self.short_term.append(memory_entry)
        
        # Move to long-term if important
        if memory_entry['importance_score'] > 0.7:
            self.store_long_term_memory(user_id, memory_entry)
        
        # Persist to disk
        self.persist_memory(memory_entry)
    
    def calculate_importance(self, interaction: Dict) -> float:
        """Calculate importance score for memory (0-1)"""
        
        # Simple importance scoring
        content = str(interaction).lower()
        
        important_keywords = ['important', 'remember', 'special', 'favorite', 'love']
        score = sum(0.2 for keyword in important_keywords if keyword in content)
        
        return min(1.0, score)
    
    def get_context(self, user_id: str, limit: int = 10) -> Dict:
        """Get conversation context for user"""
        
        user_memories = [m for m in self.short_term if m.get('user_id') == user_id]
        recent_memories = sorted(user_memories, key=lambda x: x['timestamp'])[-limit:]
        
        return {
            'recent_interactions': recent_memories,
            'user_preferences': self.get_user_preferences(user_id),
            'relationship_level': self.calculate_relationship_level(user_id)
        }
    
    def store_long_term_memory(self, user_id: str, memory: Dict):
        """Store important memory in long-term storage"""
        
        if user_id not in self.long_term:
            self.long_term[user_id] = []
        
        self.long_term[user_id].append(memory)
        
        # Limit long-term memory size
        if len(self.long_term[user_id]) > 100:
            # Keep most important memories
            self.long_term[user_id].sort(key=lambda x: x['importance_score'], reverse=True)
            self.long_term[user_id] = self.long_term[user_id][:100]
    
    def persist_memory(self, memory: Dict):
        """Persist memory to disk"""
        
        date_str = datetime.now().strftime('%Y-%m-%d')
        memory_file = f"{self.memory_path}/memory_{date_str}.jsonl"
        
        with open(memory_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(memory) + '\n')

class EmotionEngine:
    """Emotional intelligence system for agents"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.emotional_state = {
            'primary_emotion': 'neutral',
            'intensity': 0.5,
            'valence': 0.5,  # Positive/negative
            'arousal': 0.5   # Calm/excited
        }
        
        # Emotion keywords for detection
        self.emotion_keywords = {
            'joy': ['happy', 'excited', 'wonderful', 'amazing', 'great'],
            'sadness': ['sad', 'down', 'upset', 'disappointed', 'hurt'],
            'anger': ['angry', 'mad', 'frustrated', 'annoyed', 'furious'],
            'fear': ['scared', 'afraid', 'worried', 'anxious', 'nervous'],
            'love': ['love', 'adore', 'cherish', 'romantic', 'affection'],
            'surprise': ['surprised', 'shocked', 'amazed', 'stunned']
        }
    
    def analyze_emotion(self, text: str) -> Dict:
        """Analyze emotional content of text"""
        
        text_lower = text.lower()
        emotion_scores = {}
        
        # Score emotions based on keywords
        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                emotion_scores[emotion] = score
        
        # Determine primary emotion
        if emotion_scores:
            primary_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
            intensity = min(1.0, max(emotion_scores.values()) / len(text.split()) * 10)
        else:
            primary_emotion = 'neutral'
            intensity = 0.5
        
        return {
            'primary_emotion': primary_emotion,
            'intensity': intensity,
            'all_emotions': emotion_scores
        }
    
    def update_emotional_state(self, user_emotion: str, intensity: float):
        """Update agent's emotional state based on user emotion"""
        
        # Emotional contagion - agent responds to user's emotion
        response_emotions = {
            'joy': 'happy',
            'sadness': 'empathetic',
            'anger': 'calming',
            'fear': 'supportive',
            'love': 'loving',
            'surprise': 'curious'
        }
        
        self.emotional_state['primary_emotion'] = response_emotions.get(user_emotion, 'neutral')
        self.emotional_state['intensity'] = intensity * 0.8  # Slightly dampened response

class PerformanceAnalytics:
    """Real-time performance monitoring for agents"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.metrics = {
            'response_time': [],
            'user_satisfaction': [],
            'conversation_length': [],
            'error_rate': 0,
            'total_interactions': 0
        }
    
    def track_interaction(self, interaction_data: Dict):
        """Track interaction metrics"""
        
        self.metrics['total_interactions'] += 1
        
        # Track response time if available
        if 'response_time' in interaction_data:
            self.metrics['response_time'].append(interaction_data['response_time'])
        
        # Track user satisfaction if available
        if 'satisfaction_score' in interaction_data:
            self.metrics['user_satisfaction'].append(interaction_data['satisfaction_score'])
    
    def get_performance_summary(self) -> Dict:
        """Get performance summary"""
        
        avg_response_time = sum(self.metrics['response_time']) / len(self.metrics['response_time']) if self.metrics['response_time'] else 0
        avg_satisfaction = sum(self.metrics['user_satisfaction']) / len(self.metrics['user_satisfaction']) if self.metrics['user_satisfaction'] else 0
        
        return {
            'agent_name': self.agent_name,
            'total_interactions': self.metrics['total_interactions'],
            'avg_response_time': avg_response_time,
            'avg_satisfaction': avg_satisfaction,
            'error_rate': self.metrics['error_rate']
        }

# Multi-modal support system
class MultiModalProcessor:
    """Process text, voice, and visual inputs"""
    
    def __init__(self):
        self.supported_modes = ['text', 'voice', 'image']
    
    def process_text(self, text: str) -> Dict:
        """Process text input"""
        return {
            'type': 'text',
            'content': text,
            'processed_at': datetime.now().isoformat()
        }
    
    def process_voice(self, audio_data: bytes) -> Dict:
        """Process voice input (placeholder)"""
        # In real implementation, would use speech-to-text
        return {
            'type': 'voice',
            'transcription': '[Voice message received]',
            'processed_at': datetime.now().isoformat()
        }
    
    def process_image(self, image_data: bytes) -> Dict:
        """Process image input (placeholder)"""
        # In real implementation, would use vision models
        return {
            'type': 'image',
            'description': '[Image received]',
            'processed_at': datetime.now().isoformat()
        }

# Knowledge base system
class DynamicKnowledgeBase:
    """Dynamic knowledge graphs for each agent"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.knowledge_graph = {}
        self.facts = {}
        self.relationships = {}
    
    def add_fact(self, subject: str, predicate: str, object_: str):
        """Add fact to knowledge base"""
        
        fact_id = f"{subject}_{predicate}_{object_}"
        self.facts[fact_id] = {
            'subject': subject,
            'predicate': predicate,
            'object': object_,
            'timestamp': datetime.now().isoformat(),
            'confidence': 1.0
        }
    
    def query_knowledge(self, query: str) -> List[Dict]:
        """Query knowledge base"""
        
        # Simple keyword-based search (can be enhanced with NLP)
        results = []
        query_lower = query.lower()
        
        for fact_id, fact in self.facts.items():
            if any(query_lower in str(value).lower() for value in fact.values()):
                results.append(fact)
        
        return results[:10]  # Return top 10 results