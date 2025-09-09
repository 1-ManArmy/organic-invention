"""
WebSocket handler for real-time chat features
"""
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms
from flask import session, request
import json
import time
from datetime import datetime

socketio = SocketIO(cors_allowed_origins="*")

# Store active connections
active_connections = {}
agent_rooms = {}

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    client_id = request.sid
    user_id = session.get('user_id', f'guest_{client_id[:8]}')
    
    active_connections[client_id] = {
        'user_id': user_id,
        'connected_at': datetime.utcnow(),
        'current_agent': None
    }
    
    emit('connection_status', {
        'status': 'connected',
        'client_id': client_id,
        'user_id': user_id
    })
    
    print(f"Client {client_id} connected as {user_id}")

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    client_id = request.sid
    
    # Leave any agent rooms
    if client_id in active_connections:
        current_agent = active_connections[client_id].get('current_agent')
        if current_agent:
            leave_room(f'agent_{current_agent}')
        
        del active_connections[client_id]
    
    print(f"Client {client_id} disconnected")

@socketio.on('join_agent_chat')
def handle_join_agent(data):
    """Join an agent's chat room"""
    client_id = request.sid
    agent_id = data.get('agent_id')
    
    if not agent_id:
        emit('error', {'message': 'Agent ID required'})
        return
    
    # Leave previous agent room if any
    if client_id in active_connections:
        prev_agent = active_connections[client_id].get('current_agent')
        if prev_agent:
            leave_room(f'agent_{prev_agent}')
    
    # Join new agent room
    room = f'agent_{agent_id}'
    join_room(room)
    
    # Update connection info
    if client_id in active_connections:
        active_connections[client_id]['current_agent'] = agent_id
    
    # Initialize agent room if not exists
    if room not in agent_rooms:
        agent_rooms[room] = {
            'agent_id': agent_id,
            'active_users': 0,
            'last_activity': datetime.utcnow()
        }
    
    agent_rooms[room]['active_users'] += 1
    agent_rooms[room]['last_activity'] = datetime.utcnow()
    
    emit('joined_agent_chat', {
        'agent_id': agent_id,
        'room': room,
        'active_users': agent_rooms[room]['active_users']
    })
    
    # Notify others in the room
    emit('user_joined', {
        'user_id': active_connections[client_id]['user_id'],
        'agent_id': agent_id
    }, room=room, include_self=False)
    
    print(f"Client {client_id} joined agent {agent_id} chat")

@socketio.on('leave_agent_chat')
def handle_leave_agent(data):
    """Leave an agent's chat room"""
    client_id = request.sid
    agent_id = data.get('agent_id')
    
    if client_id in active_connections:
        current_agent = active_connections[client_id].get('current_agent')
        if current_agent == agent_id:
            room = f'agent_{agent_id}'
            leave_room(room)
            
            active_connections[client_id]['current_agent'] = None
            
            # Update room info
            if room in agent_rooms:
                agent_rooms[room]['active_users'] = max(0, agent_rooms[room]['active_users'] - 1)
            
            emit('left_agent_chat', {'agent_id': agent_id})
            
            # Notify others in the room
            emit('user_left', {
                'user_id': active_connections[client_id]['user_id'],
                'agent_id': agent_id
            }, room=room)
            
            print(f"Client {client_id} left agent {agent_id} chat")

@socketio.on('send_message')
def handle_message(data):
    """Handle chat message"""
    client_id = request.sid
    
    if client_id not in active_connections:
        emit('error', {'message': 'Not connected'})
        return
    
    message = data.get('message', '').strip()
    agent_id = data.get('agent_id')
    
    if not message or not agent_id:
        emit('error', {'message': 'Message and agent ID required'})
        return
    
    user_id = active_connections[client_id]['user_id']
    room = f'agent_{agent_id}'
    
    # Create message object
    message_data = {
        'id': f'msg_{int(time.time() * 1000)}',
        'user_id': user_id,
        'agent_id': agent_id,
        'message': message,
        'timestamp': datetime.utcnow().isoformat(),
        'type': 'user'
    }
    
    # Broadcast message to room
    emit('new_message', message_data, room=room)
    
    # Simulate agent typing
    emit('agent_typing', {
        'agent_id': agent_id,
        'typing': True
    }, room=room)
    
    # Simulate agent response after delay
    def send_agent_response():
        time.sleep(1 + (len(message) / 50))  # Simulate thinking time
        
        # Mock agent response (replace with actual AI integration)
        agent_responses = {
            'strategist': f"Based on your message '{message}', I suggest we analyze the strategic implications and develop a tactical approach.",
            'healer': f"I understand your concern about '{message}'. Let me help you find balance and wellness in this situation.",
            'scout': f"Regarding '{message}', I'll gather more information and provide you with comprehensive insights.",
            'analyst': f"Let me analyze the data patterns in '{message}' and provide you with detailed metrics and trends."
        }
        
        default_response = f"Thank you for sharing '{message}'. Let me process this and provide you with the best assistance."
        agent_response = agent_responses.get(agent_id, default_response)
        
        response_data = {
            'id': f'msg_{int(time.time() * 1000)}',
            'user_id': f'agent_{agent_id}',
            'agent_id': agent_id,
            'message': agent_response,
            'timestamp': datetime.utcnow().isoformat(),
            'type': 'agent'
        }
        
        # Stop typing indicator
        socketio.emit('agent_typing', {
            'agent_id': agent_id,
            'typing': False
        }, room=room)
        
        # Send agent response
        socketio.emit('new_message', response_data, room=room)
    
    # Start response in background
    socketio.start_background_task(send_agent_response)
    
    print(f"Message from {user_id} to agent {agent_id}: {message}")

@socketio.on('typing')
def handle_typing(data):
    """Handle typing indicator"""
    client_id = request.sid
    
    if client_id not in active_connections:
        return
    
    agent_id = data.get('agent_id')
    is_typing = data.get('typing', False)
    
    if agent_id:
        user_id = active_connections[client_id]['user_id']
        room = f'agent_{agent_id}'
        
        emit('user_typing', {
            'user_id': user_id,
            'agent_id': agent_id,
            'typing': is_typing
        }, room=room, include_self=False)

@socketio.on('get_room_info')
def handle_room_info(data):
    """Get information about an agent room"""
    agent_id = data.get('agent_id')
    
    if not agent_id:
        emit('error', {'message': 'Agent ID required'})
        return
    
    room = f'agent_{agent_id}'
    room_info = agent_rooms.get(room, {
        'agent_id': agent_id,
        'active_users': 0,
        'last_activity': None
    })
    
    emit('room_info', room_info)

def get_connection_stats():
    """Get connection statistics"""
    return {
        'total_connections': len(active_connections),
        'active_rooms': len(agent_rooms),
        'rooms_detail': {room: info for room, info in agent_rooms.items()}
    }

# Initialize socketio with app (called from app.py)
def init_socketio(app):
    """Initialize SocketIO with Flask app"""
    socketio.init_app(app, 
                     cors_allowed_origins="*",
                     logger=True,
                     engineio_logger=True)
    return socketio