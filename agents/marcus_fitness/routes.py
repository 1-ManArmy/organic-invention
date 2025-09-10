"""
Marcus - Fitness Coach & Trainer Routes
"""
from flask import Blueprint, render_template, request, jsonify, session
from datetime import datetime
import json

marcus_fitness_bp = Blueprint('marcus_fitness', __name__)

@marcus_fitness_bp.route('/')
def marcus_fitness_home():
    """Marcus Fitness main page"""
    user_profile = session.get('user_profile', {
        'session_count': 0,
        'experience_level': 'Beginner',
        'progress_level': 0
    })
    
    return render_template('agents/marcus_fitness/marcus_fitness.html',
                         title="Marcus - Fitness Coach & Trainer",
                         user_profile=user_profile)

@marcus_fitness_bp.route('/chat', methods=['POST'])
def marcus_fitness_chat():
    """Handle chat messages with Marcus"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        mood = data.get('mood', 'energetic')
        mode = data.get('mode', 'text')
        
        message_lower = message.lower()
        
        if 'workout' in message_lower or 'exercise' in message_lower:
            response = "LET'S CRUSH THIS WORKOUT! 💪 I'm pumped to help you reach your fitness goals! What's your target today - strength, cardio, or mobility? I'll design the perfect workout to challenge you!"
        elif 'motivation' in message_lower or 'encourage' in message_lower:
            response = "You've GOT THIS! I believe in your potential 100%! Every rep, every step, every healthy choice is building the stronger version of YOU! Your dedication today creates your transformation tomorrow!"
        elif 'nutrition' in message_lower or 'diet' in message_lower:
            response = "Fuel your fire with proper nutrition! 🔥 Let me help you create a meal plan that supports your goals - whether it's muscle gain, fat loss, or peak performance! What are your dietary preferences?"
        elif 'progress' in message_lower or 'results' in message_lower:
            response = "Progress is EARNED, not given! Let's track your journey with precision - measurements, photos, performance metrics. I'll help you celebrate wins and push through plateaus!"
        else:
            mood_responses = {
                'energetic': f"ENERGY LEVELS ARE HIGH! Ready to tackle '{message}' with maximum intensity! Let's make it happen!",
                'motivational': f"You're asking about '{message}' - I LOVE the drive! Let's turn this into ACTION and results!",
                'challenging': f"'{message}' sounds like a challenge - and I LIVE for challenges! Bring on the intensity!",
                'supportive': f"I'm here to support you with '{message}'. We'll work through this together, step by step!",
                'intense': f"Time to get INTENSE about '{message}'! No excuses, just pure determination and results!",
                'encouraging': f"Your question about '{message}' shows you're committed to growth! I'm here to cheer you on!"
            }
            response = mood_responses.get(mood, "ENERGY LEVELS ARE HIGH! Ready to push your limits and achieve greatness? Let's make today AMAZING!")
        
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

@marcus_fitness_bp.route('/save-session', methods=['POST'])
def save_session():
    """Save chat session"""
    try:
        session_data = request.get_json()
        session['marcus_fitness_session'] = session_data
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500