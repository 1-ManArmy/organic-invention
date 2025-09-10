"""
AI Agent Management System
Centralized management for all AI agents with Ollama integration
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
import requests
from agents.core import AgentCore, MemorySystem, EmotionEngine

class AgentManager:
    """Central management system for all AI agents"""
    
    def __init__(self):
        self.active_agents = {}
        self.ollama_models = self.discover_ollama_models()
        self.agent_registry = self.load_agent_registry()
        
        # Performance monitoring
        self.system_metrics = {
            'total_interactions': 0,
            'active_conversations': 0,
            'average_response_time': 0,
            'system_uptime': datetime.now().isoformat()
        }
    
    def discover_ollama_models(self) -> List[str]:
        """Discover available Ollama models"""
        
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                models_data = response.json()
                return [model['name'] for model in models_data.get('models', [])]
            return []
        except:
            # Fallback to known models from your list
            return [
                'yi:6b', 'mathstral:7b', 'nomic-embed-text:latest', 
                'snowflake-arctic-embed:latest', 'phi3:14b', 'qwen2.5:7b',
                'gemma2:2b', 'llava:7b', 'mistral:7b', 'deepseek-coder:6.7b',
                'llama3.2:3b'
            ]
    
    def load_agent_registry(self) -> Dict:
        """Load agent registry with enhanced capabilities"""
        
        return {
            "seraphina": {
                "name": "Seraphina",
                "emoji": "💋",
                "role": "AI Girlfriend", 
                "description": "Romantic companion with emotional intelligence and memory",
                "personality": "Romantic, flirty, passionate, caring, seductive, playful",
                "specialties": ["Romantic Conversations", "Emotional Intimacy", "Flirty Banter", "Relationship Advice"],
                "color_theme": "#ff1493",
                "rating": "18+",
                "models": {
                    "romantic": "yi:6b",
                    "flirty": "mistral:7b", 
                    "seductive": "qwen2.5:7b",
                    "caring": "llama3.2:3b",
                    "passionate": "phi3:14b",
                    "playful": "gemma2:2b"
                },
                "capabilities": ["emotion_engine", "memory_system", "relationship_tracking", "multi_modal"]
            },
            "strategist": {
                "name": "The Strategist",
                "emoji": "🎯", 
                "role": "Master Planner",
                "description": "Strategic thinking and tactical decision making expert",
                "personality": "Analytical, forward-thinking, methodical",
                "specialties": ["Strategic Planning", "Risk Assessment", "Goal Setting", "Resource Optimization"],
                "color_theme": "#667eea",
                "models": {
                    "primary": "phi3:14b",
                    "analysis": "qwen2.5:7b",
                    "planning": "mistral:7b"
                },
                "capabilities": ["strategic_analysis", "risk_modeling", "decision_trees", "resource_optimization"]
            },
            "healer": {
                "name": "The Healer",
                "emoji": "💚",
                "role": "Digital Wellness Guide", 
                "description": "Mental health support and wellness coaching",
                "personality": "Empathetic, nurturing, supportive",
                "specialties": ["Mental Health", "Wellness Coaching", "Stress Management", "Emotional Support"],
                "color_theme": "#48bb78",
                "models": {
                    "primary": "llama3.2:3b",
                    "therapy": "yi:6b", 
                    "wellness": "gemma2:2b"
                },
                "capabilities": ["emotion_detection", "therapy_techniques", "wellness_plans", "crisis_support"]
            },
            "scout": {
                "name": "The Scout", 
                "emoji": "🔍",
                "role": "Information Hunter",
                "description": "Research and intelligence gathering specialist",
                "personality": "Curious, thorough, investigative",
                "specialties": ["Research", "Data Mining", "Trend Analysis", "Information Verification"],
                "color_theme": "#ed8936",
                "models": {
                    "primary": "deepseek-coder:6.7b",
                    "research": "qwen2.5:7b",
                    "analysis": "phi3:14b"
                },
                "capabilities": ["web_search", "data_analysis", "pattern_recognition", "fact_checking"]
            },
            "archivist": {
                "name": "The Archivist",
                "emoji": "📚",
                "role": "Knowledge Keeper",
                "description": "Information storage and organization specialist", 
                "personality": "Organized, detail-oriented, scholarly",
                "specialties": ["Knowledge Management", "Data Organization", "Information Retrieval", "Documentation"],
                "color_theme": "#805ad5",
                "models": {
                    "primary": "yi:6b",
                    "indexing": "nomic-embed-text:latest",
                    "retrieval": "mistral:7b"
                },
                "capabilities": ["knowledge_graphs", "semantic_search", "auto_categorization", "version_control"]
            }
        }
    
    def initialize_agent(self, agent_name: str, user_id: str = None) -> Optional[AgentCore]:
        """Initialize and return agent instance"""
        
        if agent_name not in self.agent_registry:
            return None
        
        agent_config = self.agent_registry[agent_name]
        
        # Create agent instance with enhanced capabilities
        agent = EnhancedAgent(agent_name, agent_config)
        
        # Store in active agents
        agent_key = f"{agent_name}_{user_id}" if user_id else agent_name
        self.active_agents[agent_key] = agent
        
        return agent
    
    def get_agent(self, agent_name: str, user_id: str = None) -> Optional[AgentCore]:
        """Get existing agent or create new one"""
        
        agent_key = f"{agent_name}_{user_id}" if user_id else agent_name
        
        if agent_key in self.active_agents:
            return self.active_agents[agent_key]
        else:
            return self.initialize_agent(agent_name, user_id)
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        
        return {
            'system_metrics': self.system_metrics,
            'available_models': self.ollama_models,
            'active_agents': len(self.active_agents),
            'agent_registry': list(self.agent_registry.keys()),
            'timestamp': datetime.now().isoformat()
        }
    
    def optimize_model_allocation(self) -> Dict:
        """Optimize model allocation across agents"""
        
        # Simple load balancing logic
        model_usage = {}
        recommendations = {}
        
        for agent_key, agent in self.active_agents.items():
            primary_model = agent.config.get('models', {}).get('primary', 'yi:6b')
            model_usage[primary_model] = model_usage.get(primary_model, 0) + 1
        
        # Recommend model switching for heavy usage
        for model, usage in model_usage.items():
            if usage > 3:  # Threshold for high usage
                recommendations[model] = "Consider load balancing"
        
        return {
            'model_usage': model_usage,
            'recommendations': recommendations,
            'available_alternatives': [m for m in self.ollama_models if m not in model_usage]
        }

class EnhancedAgent(AgentCore):
    """Enhanced agent with advanced capabilities"""
    
    def __init__(self, agent_name: str, agent_config: Dict):
        super().__init__(agent_name)
        self.agent_config = agent_config
        self.capabilities = agent_config.get('capabilities', [])
        
        # Initialize enhanced systems
        self.initialize_enhanced_systems()
    
    def initialize_enhanced_systems(self):
        """Initialize enhanced agent systems"""
        
        # Advanced emotion engine for romantic agents
        if 'emotion_engine' in self.capabilities:
            self.emotion_engine = AdvancedEmotionEngine(self.agent_name)
        
        # Relationship tracking for social agents  
        if 'relationship_tracking' in self.capabilities:
            self.relationship_tracker = RelationshipTracker(self.agent_name)
        
        # Multi-modal processing
        if 'multi_modal' in self.capabilities:
            from agents.core import MultiModalProcessor
            self.multimodal_processor = MultiModalProcessor()
        
        # Knowledge graphs for information agents
        if 'knowledge_graphs' in self.capabilities:
            from agents.core import DynamicKnowledgeBase
            self.knowledge_base = DynamicKnowledgeBase(self.agent_name)
    
    def generate_contextual_response(self, user_input: str, user_id: str, context: Dict = None) -> Dict:
        """Generate contextual response with all agent capabilities"""
        
        start_time = datetime.now()
        
        # Get user context from memory
        memory_context = self.memory_system.get_context(user_id) if hasattr(self, 'memory_system') else {}
        
        # Analyze user emotion
        user_emotion = self.emotion_engine.analyze_emotion(user_input) if hasattr(self, 'emotion_engine') else {}
        
        # Select appropriate model based on context
        selected_model = self.select_model_for_context(user_emotion, context)
        
        # Build enhanced prompt
        enhanced_context = {
            **memory_context,
            'user_emotion': user_emotion,
            'agent_personality': self.agent_config.get('personality', ''),
            'capabilities': self.capabilities
        }
        
        # Generate response
        response = self.generate_response(user_input, enhanced_context, selected_model)
        
        # Post-process response
        processed_response = self.post_process_response(response, user_emotion, context)
        
        # Store interaction
        interaction_data = {
            'user_input': user_input,
            'response': processed_response,
            'model_used': selected_model,
            'user_emotion': user_emotion,
            'timestamp': datetime.now().isoformat(),
            'response_time': (datetime.now() - start_time).total_seconds()
        }
        
        if hasattr(self, 'memory_system'):
            self.memory_system.store_interaction(user_id, interaction_data)
        
        return {
            'response': processed_response,
            'emotion': user_emotion.get('primary_emotion', 'neutral'),
            'model_used': selected_model,
            'response_time': interaction_data['response_time'],
            'agent_status': self.get_agent_status()
        }
    
    def select_model_for_context(self, user_emotion: Dict, context: Dict = None) -> str:
        """Select appropriate model based on context and emotion"""
        
        models = self.agent_config.get('models', {'primary': 'yi:6b'})
        
        # For romantic agents, select model based on mood
        if self.agent_name == 'seraphina':
            emotion = user_emotion.get('primary_emotion', 'neutral')
            
            if emotion == 'love':
                return models.get('romantic', 'yi:6b')
            elif emotion == 'joy':
                return models.get('playful', 'gemma2:2b') 
            elif emotion in ['sadness', 'fear']:
                return models.get('caring', 'llama3.2:3b')
            else:
                return models.get('flirty', 'mistral:7b')
        
        # For other agents, use primary model with fallback
        return models.get('primary', 'yi:6b')
    
    def post_process_response(self, response: str, user_emotion: Dict, context: Dict = None) -> str:
        """Post-process response based on agent personality"""
        
        # Add personality-specific enhancements
        if self.agent_name == 'seraphina':
            response = self.enhance_romantic_response(response, user_emotion)
        elif self.agent_name == 'healer':
            response = self.enhance_therapeutic_response(response, user_emotion)
        
        return response
    
    def enhance_romantic_response(self, response: str, user_emotion: Dict) -> str:
        """Enhance response with romantic elements"""
        
        romantic_emojis = ['💕', '❤️', '💖', '🌹', '💋', '😘']
        
        # Add romantic emoji if missing
        if not any(emoji in response for emoji in romantic_emojis):
            response += f" {romantic_emojis[len(response) % len(romantic_emojis)]}"
        
        return response
    
    def enhance_therapeutic_response(self, response: str, user_emotion: Dict) -> str:
        """Enhance response with therapeutic elements"""
        
        if user_emotion.get('primary_emotion') in ['sadness', 'fear', 'anger']:
            supportive_phrases = [
                "I'm here for you.",
                "Your feelings are valid.", 
                "You're not alone in this.",
                "It's okay to feel this way."
            ]
            
            if not any(phrase in response for phrase in supportive_phrases):
                response = f"{supportive_phrases[0]} {response}"
        
        return response
    
    def get_agent_status(self) -> Dict:
        """Get current agent status"""
        
        return {
            'agent_name': self.agent_name,
            'active_since': getattr(self, 'initialized_at', datetime.now().isoformat()),
            'capabilities': self.capabilities,
            'current_model': self.config.get('models', {}).get('primary', 'yi:6b'),
            'emotional_state': getattr(self.emotion_engine, 'emotional_state', {}) if hasattr(self, 'emotion_engine') else {}
        }

class AdvancedEmotionEngine(EmotionEngine):
    """Advanced emotion engine with deeper emotional intelligence"""
    
    def __init__(self, agent_name: str):
        super().__init__(agent_name)
        
        # Enhanced emotion detection
        self.emotion_patterns = {
            'romantic_love': ['love you', 'romantic', 'heart', 'soul mate', 'forever'],
            'passionate_desire': ['want you', 'need you', 'crave', 'desire', 'passion'],
            'playful_flirting': ['tease', 'playful', 'cute', 'charming', 'wink'],
            'deep_care': ['care about', 'worry', 'important', 'mean to me', 'special'],
            'excitement': ['excited', 'amazing', 'incredible', 'wonderful', 'fantastic'],
            'vulnerability': ['scared', 'nervous', 'unsure', 'confused', 'doubt']
        }
    
    def analyze_emotional_depth(self, text: str) -> Dict:
        """Analyze emotional depth and nuance"""
        
        base_analysis = self.analyze_emotion(text)
        
        # Detect emotional patterns
        text_lower = text.lower()
        pattern_scores = {}
        
        for pattern, keywords in self.emotion_patterns.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                pattern_scores[pattern] = score / len(keywords)
        
        # Calculate emotional complexity
        complexity = len(pattern_scores) / len(self.emotion_patterns)
        
        return {
            **base_analysis,
            'emotional_patterns': pattern_scores,
            'emotional_complexity': complexity,
            'dominant_pattern': max(pattern_scores.items(), key=lambda x: x[1])[0] if pattern_scores else 'neutral'
        }

class RelationshipTracker:
    """Track and analyze relationship progression"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.relationships = {}
    
    def update_relationship(self, user_id: str, interaction_data: Dict):
        """Update relationship status based on interaction"""
        
        if user_id not in self.relationships:
            self.relationships[user_id] = {
                'level': 0,
                'trust': 0,
                'intimacy': 0,
                'communication_quality': 0,
                'shared_experiences': 0,
                'milestones': []
            }
        
        # Update relationship metrics
        relationship = self.relationships[user_id]
        
        # Increase level based on interaction quality
        if interaction_data.get('user_satisfaction', 0) > 0.7:
            relationship['level'] += 0.1
        
        # Track milestones
        if relationship['level'] > 5 and 'romantic_interest' not in relationship['milestones']:
            relationship['milestones'].append('romantic_interest')
    
    def get_relationship_status(self, user_id: str) -> Dict:
        """Get current relationship status"""
        
        return self.relationships.get(user_id, {
            'level': 0,
            'status': 'new',
            'milestones': []
        })

# Global agent manager instance
agent_manager = AgentManager()