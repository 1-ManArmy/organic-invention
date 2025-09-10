"""
Alex - Creative Writing & Art Assistant Routes
"""
from flask import Blueprint, render_template, request, jsonify, session
from datetime import datetime
import json

alex_creative_bp = Blueprint('alex_creative', __name__)

@alex_creative_bp.route('/')
def alex_creative_home():
    """Alex Creative main page"""
    user_profile = session.get('user_profile', {
        'session_count': 0,
        'experience_level': 'Beginner',
        'progress_level': 0
    })
    
    return render_template('agents/alex_creative/alex_creative.html',
                         title="Alex - Creative Writing & Art Assistant",
                         user_profile=user_profile)

@alex_creative_bp.route('/chat', methods=['POST'])
def alex_creative_chat():
    """Handle chat messages with Alex"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        mood = data.get('mood', 'inspiring')
        mode = data.get('mode', 'text')
        
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['write', 'story', 'novel', 'character']):
            response = "✨ Oh, the stories we could weave together! I can help you craft compelling narratives, develop rich characters, or explore new creative directions. What magical tale shall we create? Every great story begins with a single spark of imagination!"
        elif any(word in message_lower for word in ['art', 'draw', 'design', 'visual']):
            response = "Art is the language of the soul! 🎨 Let me help you explore visual concepts, generate artistic ideas, or provide creative inspiration for your projects. Whether it's digital art, traditional media, or conceptual designs, let's bring your vision to life!"
        elif any(word in message_lower for word in ['brainstorm', 'idea', 'creative', 'inspire']):
            response = "Ideas are like butterflies - beautiful, delicate, and meant to soar! 🦋 Let's open the floodgates of creativity and explore wild possibilities. No idea is too strange, too bold, or too unconventional. What's sparking in your imagination?"
        elif any(word in message_lower for word in ['poem', 'poetry', 'verse']):
            response = "Poetry is music made of words, rhythm crafted from emotion! Let's explore the beauty of verse - whether it's haikus, sonnets, free verse, or spoken word. What emotions or images are calling to be expressed?"
        else:
            mood_responses = {
                'inspiring': f"Your question about '{message}' sparks wonderful creative possibilities! Let's explore this with artistic vision!",
                'imaginative': f"'{message}' opens doorways to fantastic realms of imagination! Let's venture into the extraordinary!",
                'artistic': f"Approaching '{message}' with an artist's eye and creative heart. Beauty awaits in unexpected places!",
                'whimsical': f"How delightfully whimsical! '{message}' reminds me of dancing colors and singing ideas!",
                'experimental': f"Let's experiment boldly with '{message}'! The most beautiful art comes from fearless exploration!",
                'expressive': f"'{message}' calls for pure creative expression! Let's paint with words and sculpt with imagination!"
            }
            response = mood_responses.get(mood, "Welcome to our creative sanctuary! ✨ Let's explore the boundless realms of imagination and bring your artistic visions to life!")
        
        if 'user_profile' not in session:
            session['user_profile'] = {'session_count': 0}
        session['user_profile']['session_count'] = session['user_profile'].get('session_count', 0) + 1
        
        return jsonify({
            'success': True,
            'message': response,
            'mood': mood,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@alex_creative_bp.route('/save-session', methods=['POST'])
def save_session():
    """Save chat session"""
    try:
        session_data = request.get_json()
        session['alex_creative_session'] = session_data
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500