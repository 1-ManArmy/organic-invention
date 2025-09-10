"""
Elena - Mental Health & Wellness Therapist Routes
"""
from flask import Blueprint, render_template, request, jsonify, session
from datetime import datetime
import json

elena_therapist_bp = Blueprint('elena_therapist', __name__)

@elena_therapist_bp.route('/')
def elena_therapist_home():
    """Elena Therapist main page"""
    user_profile = session.get('user_profile', {
        'session_count': 0,
        'experience_level': 'Beginner',
        'progress_level': 0
    })
    
    return render_template('agents/elena_therapist/elena_therapist.html',
                         title="Elena - Mental Health & Wellness Therapist",
                         user_profile=user_profile)

@elena_therapist_bp.route('/chat', methods=['POST'])
def elena_therapist_chat():
    """Handle chat messages with Elena"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        mood = data.get('mood', 'calming')
        mode = data.get('mode', 'text')
        
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['feel', 'emotion', 'sad', 'anxious', 'stressed', 'worried']):
            response = "I hear you, and your feelings are completely valid. 🌱 This is a safe space where you can express yourself freely. I'm here to listen with compassion and support you through whatever you're experiencing. Would you like to share more about what's on your heart?"
        elif any(word in message_lower for word in ['help', 'support', 'need', 'guidance']):
            response = "You don't have to face this alone. I'm here to walk alongside you, offering gentle guidance and unconditional support. Take all the time you need - there's no rush in healing and growth. What kind of support would feel most helpful right now?"
        elif any(word in message_lower for word in ['meditation', 'mindfulness', 'breathe', 'relax']):
            response = "Mindfulness is a beautiful path to inner peace. 🧘‍♀️ Let's explore some gentle breathing exercises or guided meditations that can help center your mind and calm your spirit. Would you like me to guide you through a brief mindfulness practice?"
        elif any(word in message_lower for word in ['therapy', 'counseling', 'mental health']):
            response = "Mental health is just as important as physical health, and seeking support shows incredible strength. I'm honored to be part of your wellness journey. Together, we can explore healthy coping strategies and build resilience."
        else:
            mood_responses = {
                'calming': f"Let's peacefully explore what you've shared about '{message}'. I'm here with gentle, caring presence.",
                'empathetic': f"I deeply understand your concern about '{message}'. Your experience matters, and I'm here to support you with warmth.",
                'supportive': f"Thank you for trusting me with '{message}'. I'm here to offer unwavering support and encouragement.",
                'understanding': f"I can sense the importance of '{message}' to you. Let's explore this together with patience and compassion.",
                'gentle': f"Approaching '{message}' with gentle care and understanding. You're in a safe space here.",
                'wise': f"Your question about '{message}' shows deep reflection. Let's explore this with wisdom and insight."
            }
            response = mood_responses.get(mood, "Welcome to our peaceful space. I'm here to listen, understand, and support you with warmth and compassion. 💙")
        
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

@elena_therapist_bp.route('/save-session', methods=['POST'])
def save_session():
    """Save chat session"""
    try:
        session_data = request.get_json()
        session['elena_therapist_session'] = session_data
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500