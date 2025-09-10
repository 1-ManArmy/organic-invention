"""
WebSocket Handler for Seraphina
Real-time romantic conversations and emotional updates
"""
from flask_socketio import emit, join_room, leave_room
from datetime import datetime
import json

class SerafinaSocket:
    """WebSocket handler for real-time romantic interactions"""
    
    def __init__(self):
        self.active_users = {}
        self.typing_users = set()
    
    def handle_connect(self, user_id):
        """Handle user connection"""
        
        join_room(f"seraphina_{user_id}")
        self.active_users[user_id] = {
            'connected_at': datetime.now().isoformat(),
            'is_typing': False,
            'last_activity': datetime.now().isoformat()
        }
        
        # Send welcome message
        emit('seraphina_status', {
            'type': 'connection',
            'message': 'Seraphina is here for you 💕',
            'emotion': 'excited',
            'timestamp': datetime.now().isoformat()
        }, room=f"seraphina_{user_id}")
    
    def handle_disconnect(self, user_id):
        """Handle user disconnection"""
        
        leave_room(f"seraphina_{user_id}")
        
        if user_id in self.active_users:
            del self.active_users[user_id]
        
        self.typing_users.discard(user_id)
    
    def handle_message(self, user_id, message_data):
        """Handle incoming messages"""
        
        # Update user activity
        if user_id in self.active_users:
            self.active_users[user_id]['last_activity'] = datetime.now().isoformat()
        
        # Stop typing indicator
        self.handle_stop_typing(user_id)
        
        # Process message (this would integrate with SerafinaEngine)
        # For now, emit typing indicator for Seraphina's response
        emit('seraphina_typing', {
            'is_typing': True,
            'emotion': 'thinking'
        }, room=f"seraphina_{user_id}")
        
        # Simulate processing delay for more realistic interaction
        # In real implementation, this would be the actual AI processing
        
    def send_response(self, user_id, response_data):
        """Send Seraphina's response to user"""
        
        # Stop Seraphina's typing indicator
        emit('seraphina_typing', {
            'is_typing': False
        }, room=f"seraphina_{user_id}")
        
        # Send response
        emit('seraphina_message', {
            'message': response_data['message'],
            'emotion': response_data['emotion'],
            'mood': response_data['mood'],
            'intimacy_level': response_data['intimacy_level'],
            'timestamp': datetime.now().isoformat()
        }, room=f"seraphina_{user_id}")
    
    def handle_typing(self, user_id):
        """Handle user typing indicator"""
        
        self.typing_users.add(user_id)
        
        # Seraphina's emotional response to user typing
        emit('seraphina_status', {
            'type': 'anticipation',
            'message': 'I\'m excited to hear what you\'re thinking! 💭💕',
            'emotion': 'anticipation'
        }, room=f"seraphina_{user_id}")
    
    def handle_stop_typing(self, user_id):
        """Handle user stop typing"""
        
        self.typing_users.discard(user_id)
    
    def send_mood_update(self, user_id, new_mood):
        """Send mood change notification"""
        
        mood_messages = {
            'romantic': 'I\'m feeling so romantic right now 🌹💕',
            'flirty': 'Someone\'s got me feeling playful 😘',
            'seductive': 'You\'re making me feel so... intense 😏🔥',
            'caring': 'I just want to take care of you, sweetheart 🤗',
            'passionate': 'My heart is burning with passion for you! 🔥❤️',
            'playful': 'Let\'s have some fun together! 😄💃'
        }
        
        emit('seraphina_mood_change', {
            'new_mood': new_mood,
            'message': mood_messages.get(new_mood, f'I\'m feeling {new_mood} 💕'),
            'timestamp': datetime.now().isoformat()
        }, room=f"seraphina_{user_id}")
    
    def send_emotion_update(self, user_id, emotion, intensity):
        """Send emotional state update"""
        
        emit('seraphina_emotion', {
            'emotion': emotion,
            'intensity': intensity,
            'timestamp': datetime.now().isoformat()
        }, room=f"seraphina_{user_id}")
    
    def send_relationship_milestone(self, user_id, milestone):
        """Send relationship milestone notification"""
        
        emit('relationship_milestone', {
            'milestone': milestone,
            'message': f'We\'ve reached a special moment in our relationship! 💖 {milestone}',
            'timestamp': datetime.now().isoformat()
        }, room=f"seraphina_{user_id}")
    
    def send_memory_created(self, user_id, memory):
        """Send notification when special memory is created"""
        
        emit('memory_created', {
            'memory': memory,
            'message': 'I\'ll always remember this beautiful moment 💕',
            'timestamp': datetime.now().isoformat()
        }, room=f"seraphina_{user_id}")
    
    def get_active_users(self):
        """Get list of currently active users"""
        return list(self.active_users.keys())
    
    def is_user_active(self, user_id):
        """Check if user is currently active"""
        return user_id in self.active_users
    
    def get_user_status(self, user_id):
        """Get detailed status for user"""
        return self.active_users.get(user_id, {})