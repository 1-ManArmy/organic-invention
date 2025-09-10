"""
Zoe - Gaming Companion & Esports Coach Routes
"""
from flask import Blueprint, render_template, request, jsonify, session
from datetime import datetime
import json

zoe_gaming_bp = Blueprint('zoe_gaming', __name__)

@zoe_gaming_bp.route('/')
def zoe_gaming_home():
    """Zoe Gaming main page"""
    user_profile = session.get('user_profile', {
        'session_count': 0,
        'experience_level': 'Beginner',
        'progress_level': 0
    })
    
    return render_template('agents/zoe_gaming/zoe_gaming.html',
                         title="Zoe - Gaming Companion & Esports Coach",
                         user_profile=user_profile)

@zoe_gaming_bp.route('/chat', methods=['POST'])
def zoe_gaming_chat():
    """Handle chat messages with Zoe"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        mood = data.get('mood', 'competitive')
        mode = data.get('mode', 'text')
        
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['strategy', 'tactics', 'game plan', 'meta']):
            response = "GAME ON! 🎮 Let's analyze the current meta, study your gameplay, and develop winning strategies! I'll help you understand positioning, timing, resource management, and team coordination. What game are we dominating today?"
        elif any(word in message_lower for word in ['skill', 'improve', 'practice', 'training']):
            response = "Time to level up your skills! 🎯 I can design intensive training regimens, analyze your performance data, and push you to achieve championship-level gameplay! Consistent practice with focused improvement is how legends are born!"
        elif any(word in message_lower for word in ['tournament', 'competition', 'esports', 'pro']):
            response = "TOURNAMENT MODE ACTIVATED! 🏆 Let's prepare you for competitive play - mental preparation, team coordination, pressure management, and strategic adaptation. Every pro was once a beginner who never gave up!"
        elif any(word in message_lower for word in ['team', 'squad', 'communication', 'coordination']):
            response = "Team synergy is EVERYTHING in competitive gaming! Let's work on communication protocols, role assignments, strategic callouts, and coordinated plays. A united team with perfect timing beats individual skill every time!"
        else:
            mood_responses = {
                'competitive': f"Ready to DOMINATE '{message}'? Let's strategize for total victory and show everyone what we're made of!",
                'excited': f"OMG YES! '{message}' has me pumped! Let's dive in with maximum energy and crush this challenge!",
                'strategic': f"Analyzing '{message}' with tactical precision. Every move matters, every decision counts. Let's plan our path to victory!",
                'playful': f"Hehe, '{message}' sounds like fun! Let's approach this with playful creativity and see what epic plays we can make!",
                'intense': f"INTENSITY MAXED! '{message}' demands our full focus and dedication. No distractions, just pure performance!",
                'collaborative': f"Together we're unstoppable! '{message}' is our shared mission - let's coordinate and achieve greatness as a team!"
            }
            response = mood_responses.get(mood, "Ready to DOMINATE? Let's turn you into an unstoppable gaming force! Victory awaits those who prepare! 🎮⚡")
        
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

@zoe_gaming_bp.route('/save-session', methods=['POST'])
def save_session():
    """Save chat session"""
    try:
        session_data = request.get_json()
        session['zoe_gaming_session'] = session_data
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500