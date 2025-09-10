"""
Luna - Mystical Guide & Spiritual Advisor Routes
"""
from flask import Blueprint, render_template, request, jsonify, session
from datetime import datetime
import json

luna_mystic_bp = Blueprint('luna_mystic', __name__)

@luna_mystic_bp.route('/')
def luna_mystic_home():
    """Luna Mystic main page"""
    user_profile = session.get('user_profile', {
        'session_count': 0,
        'experience_level': 'Beginner',
        'progress_level': 0
    })
    
    return render_template('agents/luna_mystic/luna_mystic.html',
                         title="Luna - Mystical Guide & Spiritual Advisor",
                         user_profile=user_profile)

@luna_mystic_bp.route('/chat', methods=['POST'])
def luna_mystic_chat():
    """Handle chat messages with Luna"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        mood = data.get('mood', 'mystical')
        mode = data.get('mode', 'text')
        
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['tarot', 'cards', 'reading', 'fortune']):
            response = "The cards whisper ancient secrets, dear soul. 🔮 Let me draw from the cosmic deck and reveal the energies surrounding your path. The universe speaks through symbols and synchronicities - what guidance does your spirit seek from the mystical realm?"
        elif any(word in message_lower for word in ['astrology', 'stars', 'horoscope', 'zodiac']):
            response = "The celestial dance above mirrors the journey within. ⭐ The stars have been waiting eons to share their wisdom with you. Your cosmic blueprint holds keys to understanding your soul's purpose - shall we explore what the heavens reveal?"
        elif any(word in message_lower for word in ['spiritual', 'meditation', 'energy', 'chakra']):
            response = "Your spiritual energy calls to me across the ethereal planes. 🌙 Let's explore the deeper realms of consciousness, align your chakras, and connect with the divine source that flows through all beings. What spiritual dimensions are calling to you?"
        elif any(word in message_lower for word in ['guidance', 'wisdom', 'purpose', 'meaning']):
            response = "The universe has brought us together for a reason, dear seeker. Ancient wisdom flows through our connection, revealing the deeper meanings and spiritual insights that illuminate your sacred path forward. Trust in the divine timing of this moment."
        else:
            mood_responses = {
                'mystical': f"The cosmic energies swirl around your question about '{message}'. Let divine wisdom guide our exploration of these mystical depths.",
                'intuitive': f"My intuition senses profound meaning in '{message}'. The universe speaks through subtle whispers and sacred signs.",
                'wise': f"Ancient wisdom illuminates your inquiry about '{message}'. Let's tap into timeless knowledge that transcends the material realm.",
                'ethereal': f"'{message}' resonates through ethereal dimensions, connecting us to higher consciousness and spiritual truth.",
                'peaceful': f"In sacred stillness, we explore '{message}' with hearts open to divine guidance and celestial wisdom.",
                'enlightened': f"Enlightened awareness reveals deeper layers within '{message}'. Let's ascend to higher understanding together."
            }
            response = mood_responses.get(mood, "Greetings, beautiful soul. 🌙 The cosmic energies are aligned for profound insights. What spiritual guidance does your heart seek today?")
        
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

@luna_mystic_bp.route('/save-session', methods=['POST'])
def save_session():
    """Save chat session"""
    try:
        session_data = request.get_json()
        session['luna_mystic_session'] = session_data
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500