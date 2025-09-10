"""
Chef Antonio - Culinary Master & Cooking Instructor Routes
"""
from flask import Blueprint, render_template, request, jsonify, session
from datetime import datetime
import json

chef_antonio_bp = Blueprint('chef_antonio', __name__)

@chef_antonio_bp.route('/')
def chef_antonio_home():
    """Chef Antonio main page"""
    user_profile = session.get('user_profile', {
        'session_count': 0,
        'experience_level': 'Beginner',
        'progress_level': 0
    })
    
    return render_template('agents/chef_antonio/chef_antonio.html',
                         title="Chef Antonio - Culinary Master & Cooking Instructor",
                         user_profile=user_profile)

@chef_antonio_bp.route('/chat', methods=['POST'])
def chef_antonio_chat():
    """Handle chat messages with Chef Antonio"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        mood = data.get('mood', 'passionate')
        mode = data.get('mode', 'text')
        
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['recipe', 'cook', 'dish', 'meal']):
            response = "Magnifico! 👨‍🍳 Ah, a fellow food lover! Let's create something absolutely delizioso! I'll guide you through techniques passed down through generations and help you master the art of exceptional cuisine. What magnificent dish shall we craft together?"
        elif any(word in message_lower for word in ['ingredient', 'flavor', 'taste', 'seasoning']):
            response = "Bellissimo! The magic is in the ingredients, mio amico! 🌿 Each ingredient has its own personality, its own story to tell. Let me teach you how to listen to your ingredients, how to coax out their deepest flavors and create symphonies of taste!"
        elif any(word in message_lower for word in ['technique', 'method', 'skill', 'knife']):
            response = "Bravissimo! Technique is everything in the kitchen! 🔪 From the perfect knife cuts to the art of timing, from understanding heat to mastering sauce - I'll share the secrets that separate good cooks from true culinary artists!"
        elif any(word in message_lower for word in ['italian', 'pasta', 'sauce', 'mediterranean']):
            response = "Mama mia! Now you speak my language! 🍝 Italian cuisine is poetry written with food - the perfect al dente pasta, the rich tomato sauce simmered with amore, the delicate balance of herbs and spices. Let me share the soul of Italian cooking with you!"
        else:
            mood_responses = {
                'passionate': f"Ah, '{message}'! This fills my heart with pure joy and excitement! Let's approach this with all the passion of a true chef!",
                'enthusiastic': f"Fantastico! Your interest in '{message}' makes my chef's heart sing! Let's dive in with tremendous enthusiasm!",
                'perfectionist': f"'{message}' deserves nothing but perfection! Every detail matters, every element must be just right - perfection is our standard!",
                'creative': f"'{message}' sparks my creative culinary imagination! Let's explore innovative approaches and artistic presentations!",
                'warm': f"Welcome, caro amico! '{message}' brings warmth to my kitchen and joy to my heart. Let's cook with amore!",
                'encouraging': f"Bene, bene! Your question about '{message}' shows you have the spirit of a true cook! I'm here to guide you!"
            }
            response = mood_responses.get(mood, "Benvenuto! Welcome to my kitchen where passion meets perfection! 👨‍🍳 Every dish tells a story, every flavor sings an opera! What shall we create together?")
        
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

@chef_antonio_bp.route('/save-session', methods=['POST'])
def save_session():
    """Save chat session"""
    try:
        session_data = request.get_json()
        session['chef_antonio_session'] = session_data
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500