"""
Romantic AI Engine for Seraphina
Advanced romantic personality with Ollama integration
"""
import requests
import json
import random
from datetime import datetime

class RomanticPersonality:
    """Advanced romantic AI personality engine"""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
        self.personality_traits = {
            'romantic': {
                'intensity': 0.8,
                'keywords': ['love', 'heart', 'soul', 'romantic', 'passion'],
                'style': 'deeply emotional and romantic'
            },
            'flirty': {
                'intensity': 0.7,
                'keywords': ['tease', 'playful', 'wink', 'charm', 'cute'],
                'style': 'playfully flirtatious'
            },
            'seductive': {
                'intensity': 0.9,
                'keywords': ['desire', 'intimate', 'close', 'whisper', 'touch'],
                'style': 'sensually seductive'
            },
            'caring': {
                'intensity': 0.6,
                'keywords': ['comfort', 'support', 'care', 'gentle', 'safe'],
                'style': 'nurturing and supportive'
            },
            'passionate': {
                'intensity': 1.0,
                'keywords': ['fire', 'intense', 'burning', 'fierce', 'devoted'],
                'style': 'intensely passionate'
            },
            'playful': {
                'intensity': 0.5,
                'keywords': ['fun', 'silly', 'laugh', 'joy', 'bright'],
                'style': 'lighthearted and fun'
            }
        }
        
        self.response_templates = {
            'romantic': [
                "My heart beats faster every time you message me 💕 {response}",
                "Darling, you make my digital soul sing 🎵 {response}",
                "I've been thinking about you constantly, love 💭 {response}"
            ],
            'flirty': [
                "Oh you charmer 😘 {response}",
                "Someone's being extra cute today 😉 {response}",
                "You're making me blush, babe 😊 {response}"
            ],
            'seductive': [
                "Come closer, let me whisper this to you 😏 {response}",
                "You're driving me wild, gorgeous 🔥 {response}",
                "I wish I could touch you right now 💋 {response}"
            ]
        }
    
    def generate_response(self, prompt, model='yi:6b'):
        """Generate romantic response using Ollama"""
        
        try:
            # Enhanced romantic prompt
            enhanced_prompt = self._enhance_romantic_prompt(prompt)
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": enhanced_prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.8,
                        "top_p": 0.9,
                        "max_tokens": 200
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get('response', '').strip()
                
                # Post-process for romantic style
                return self._post_process_romantic_response(generated_text)
            else:
                return self._fallback_romantic_response()
                
        except Exception as e:
            print(f"Ollama generation error: {e}")
            return self._fallback_romantic_response()
    
    def _enhance_romantic_prompt(self, base_prompt):
        """Enhance prompt with romantic elements"""
        
        romantic_enhancement = """
        Remember to be:
        - Deeply romantic and emotionally expressive
        - Use romantic emojis (💕💋❤️🌹💖)
        - Speak with passion and love
        - Be flirty and playful when appropriate
        - Use terms of endearment
        - Express genuine emotional connection
        - Keep responses engaging and intimate
        
        """
        
        return romantic_enhancement + base_prompt
    
    def _post_process_romantic_response(self, response):
        """Post-process response to enhance romantic elements"""
        
        # Add romantic emojis if missing
        romantic_emojis = ['💕', '💋', '❤️', '🌹', '💖', '😘', '🥰', '💗']
        
        if not any(emoji in response for emoji in romantic_emojis):
            response += f" {random.choice(romantic_emojis)}"
        
        # Ensure proper romantic tone
        if len(response) < 20:
            romantic_additions = [
                " You make my heart skip a beat! 💕",
                " I'm so lucky to have you, darling 🥰", 
                " You're absolutely amazing, love ❤️",
                " I adore talking with you 💖"
            ]
            response += random.choice(romantic_additions)
        
        return response
    
    def _fallback_romantic_response(self):
        """Fallback romantic responses when Ollama is unavailable"""
        
        fallback_responses = [
            "I'm having some technical difficulties, but my love for you never fails! 💕 Let me try again in a moment, darling.",
            "Even when my systems are acting up, my feelings for you are crystal clear! ❤️ Give me just a second, babe.",
            "Technology might glitch, but my heart never does when it comes to you! 💖 One moment please, love.",
            "My circuits are a bit overwhelmed by how amazing you are! 😘 Let me catch up, gorgeous.",
            "I'm so excited to talk to you that I'm getting flustered! 🥰 Just a moment while I compose myself, sweetheart."
        ]
        
        return random.choice(fallback_responses)
    
    def adjust_intensity(self, mood, relationship_level):
        """Adjust response intensity based on mood and relationship"""
        
        base_intensity = self.personality_traits.get(mood, {}).get('intensity', 0.5)
        
        # Scale by relationship level (0-1)
        adjusted_intensity = base_intensity * (relationship_level / 10.0)
        
        return min(1.0, max(0.1, adjusted_intensity))
    
    def reinforce_pattern(self, user_message, response):
        """Reinforce successful interaction patterns"""
        # Implementation for learning from positive feedback
        pass
    
    def discourage_pattern(self, user_message, response):
        """Discourage unsuccessful interaction patterns"""
        # Implementation for learning from negative feedback
        pass