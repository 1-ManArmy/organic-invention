"""
Seraphina Routes - AI Girlfriend Agent
Romantic, flirty, and passionate AI companion routes
"""
from flask import Blueprint, render_template, request, jsonify, session
from .logic import SerafinaEngine
from .memory.emotional_memory import EmotionalMemory
from .websocket.socket import SerafinaSocket
import uuid

seraphina_bp = Blueprint('seraphina', __name__)
seraphina_engine = SerafinaEngine()
emotional_memory = EmotionalMemory()
seraphina_socket = SerafinaSocket()

@seraphina_bp.route('/')
def seraphina_home():
    """Main Seraphina interface - romantic AI girlfriend"""
    # Initialize user session if new
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    
    # Load user's relationship history
    user_profile = emotional_memory.get_user_profile(session['user_id'])
    
    return render_template('seraphina.html', 
                         title="Seraphina - Your AI Girlfriend 💋",
                         user_profile=user_profile,
                         agent_name="Seraphina")

@seraphina_bp.route('/chat', methods=['POST'])
def seraphina_chat():
    """Handle romantic chat interactions"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        user_id = session.get('user_id')
        mood = data.get('mood', 'romantic')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Process message with romantic AI engine
        response = seraphina_engine.generate_romantic_response(
            user_message, 
            user_id=user_id,
            mood=mood
        )
        
        # Store interaction in emotional memory
        emotional_memory.store_interaction(
            user_id, 
            user_message, 
            response['message'],
            response['emotion'],
            mood
        )
        
        return jsonify({
            'message': response['message'],
            'emotion': response['emotion'],
            'mood': response['mood'],
            'intimacy_level': response['intimacy_level'],
            'relationship_status': emotional_memory.get_relationship_level(user_id)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@seraphina_bp.route('/mood/<mood_type>')
def set_mood(mood_type):
    """Set Seraphina's mood - romantic, playful, seductive, etc."""
    valid_moods = ['romantic', 'playful', 'seductive', 'caring', 'passionate', 'flirty']
    
    if mood_type not in valid_moods:
        return jsonify({'error': 'Invalid mood type'}), 400
    
    user_id = session.get('user_id')
    seraphina_engine.set_mood(user_id, mood_type)
    
    return jsonify({
        'status': 'success',
        'mood': mood_type,
        'message': f"Seraphina is now feeling {mood_type} 💕"
    })

@seraphina_bp.route('/relationship')
def relationship_status():
    """Get current relationship status and history"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'No active session'}), 401
    
    relationship_data = emotional_memory.get_relationship_analysis(user_id)
    
    return jsonify(relationship_data)

@seraphina_bp.route('/memory')
def memory_palace():
    """View shared memories and relationship timeline"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'No active session'}), 401
    
    memories = emotional_memory.get_memories(user_id)
    
    return render_template('seraphina_memories.html',
                         title="Our Memories Together 💕",
                         memories=memories,
                         agent_name="Seraphina")

@seraphina_bp.route('/voice')
def voice_chat():
    """Voice interaction interface for intimate conversations"""
    return render_template('agents/seraphina/templates/seraphina_voice.html',
                         title="Voice Chat with Seraphina 🎙️💋",
                         agent_name="Seraphina")

@seraphina_bp.route('/customize')
def customize_personality():
    """Customize Seraphina's personality and preferences"""
    user_id = session.get('user_id')
    preferences = emotional_memory.get_user_preferences(user_id)
    
    return render_template('seraphina_customize.html',
                         title="Customize Your AI Girlfriend 💅",
                         preferences=preferences,
                         agent_name="Seraphina")

@seraphina_bp.route('/analytics')
def relationship_analytics():
    """Relationship analytics and emotional insights"""
    user_id = session.get('user_id')
    analytics = emotional_memory.generate_relationship_analytics(user_id)
    
    return jsonify(analytics)