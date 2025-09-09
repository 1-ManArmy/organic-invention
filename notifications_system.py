"""
Real-time notifications system
"""
from flask import Blueprint, render_template, jsonify, request, session
from datetime import datetime, timedelta
import json

notifications_bp = Blueprint('notifications', __name__)

# In-memory storage for demo (replace with database)
notifications_store = {}
user_preferences = {}

class NotificationManager:
    """Manage user notifications"""
    
    @staticmethod
    def create_notification(user_id, title, message, type='info', agent_id=None):
        """Create a new notification"""
        if user_id not in notifications_store:
            notifications_store[user_id] = []
        
        notification = {
            'id': f'notif_{int(datetime.utcnow().timestamp() * 1000)}',
            'title': title,
            'message': message,
            'type': type,  # info, success, warning, error
            'agent_id': agent_id,
            'created_at': datetime.utcnow().isoformat(),
            'read': False,
            'expires_at': (datetime.utcnow() + timedelta(days=7)).isoformat()
        }
        
        notifications_store[user_id].append(notification)
        
        # Keep only last 50 notifications per user
        if len(notifications_store[user_id]) > 50:
            notifications_store[user_id] = notifications_store[user_id][-50:]
        
        return notification
    
    @staticmethod
    def get_notifications(user_id, unread_only=False, limit=20):
        """Get user notifications"""
        user_notifications = notifications_store.get(user_id, [])
        
        if unread_only:
            user_notifications = [n for n in user_notifications if not n['read']]
        
        # Sort by created_at desc
        user_notifications.sort(key=lambda x: x['created_at'], reverse=True)
        
        return user_notifications[:limit]
    
    @staticmethod
    def mark_read(user_id, notification_id):
        """Mark notification as read"""
        user_notifications = notifications_store.get(user_id, [])
        
        for notification in user_notifications:
            if notification['id'] == notification_id:
                notification['read'] = True
                return True
        
        return False
    
    @staticmethod
    def mark_all_read(user_id):
        """Mark all notifications as read"""
        user_notifications = notifications_store.get(user_id, [])
        
        for notification in user_notifications:
            notification['read'] = True
        
        return len(user_notifications)
    
    @staticmethod
    def delete_notification(user_id, notification_id):
        """Delete a notification"""
        user_notifications = notifications_store.get(user_id, [])
        
        for i, notification in enumerate(user_notifications):
            if notification['id'] == notification_id:
                del user_notifications[i]
                return True
        
        return False
    
    @staticmethod
    def get_unread_count(user_id):
        """Get count of unread notifications"""
        user_notifications = notifications_store.get(user_id, [])
        return len([n for n in user_notifications if not n['read']])

@notifications_bp.route('/api/notifications')
def get_notifications():
    """Get user notifications"""
    user_id = session.get('user_id', 'guest')
    unread_only = request.args.get('unread_only', 'false').lower() == 'true'
    limit = int(request.args.get('limit', 20))
    
    notifications = NotificationManager.get_notifications(user_id, unread_only, limit)
    unread_count = NotificationManager.get_unread_count(user_id)
    
    return jsonify({
        'success': True,
        'notifications': notifications,
        'unread_count': unread_count,
        'total': len(notifications_store.get(user_id, []))
    })

@notifications_bp.route('/api/notifications/<notification_id>/read', methods=['POST'])
def mark_notification_read(notification_id):
    """Mark notification as read"""
    user_id = session.get('user_id', 'guest')
    
    success = NotificationManager.mark_read(user_id, notification_id)
    
    return jsonify({
        'success': success,
        'message': 'Notification marked as read' if success else 'Notification not found'
    })

@notifications_bp.route('/api/notifications/mark-all-read', methods=['POST'])
def mark_all_read():
    """Mark all notifications as read"""
    user_id = session.get('user_id', 'guest')
    
    count = NotificationManager.mark_all_read(user_id)
    
    return jsonify({
        'success': True,
        'message': f'Marked {count} notifications as read',
        'count': count
    })

@notifications_bp.route('/api/notifications/<notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    """Delete a notification"""
    user_id = session.get('user_id', 'guest')
    
    success = NotificationManager.delete_notification(user_id, notification_id)
    
    return jsonify({
        'success': success,
        'message': 'Notification deleted' if success else 'Notification not found'
    })

@notifications_bp.route('/api/notifications/preferences')
def get_preferences():
    """Get notification preferences"""
    user_id = session.get('user_id', 'guest')
    
    preferences = user_preferences.get(user_id, {
        'email_notifications': True,
        'push_notifications': True,
        'agent_responses': True,
        'system_updates': True,
        'marketing': False,
        'quiet_hours': {
            'enabled': False,
            'start': '22:00',
            'end': '08:00'
        }
    })
    
    return jsonify({
        'success': True,
        'preferences': preferences
    })

@notifications_bp.route('/api/notifications/preferences', methods=['POST'])
def update_preferences():
    """Update notification preferences"""
    user_id = session.get('user_id', 'guest')
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'message': 'No data provided'
        }), 400
    
    user_preferences[user_id] = data
    
    return jsonify({
        'success': True,
        'message': 'Preferences updated successfully',
        'preferences': data
    })

# Notification templates for different events
def notify_agent_response(user_id, agent_name, message_preview):
    """Notify user of agent response"""
    NotificationManager.create_notification(
        user_id=user_id,
        title=f"New message from {agent_name}",
        message=message_preview[:100] + "..." if len(message_preview) > 100 else message_preview,
        type='info',
        agent_id=agent_name.lower()
    )

def notify_system_update(user_id, update_title, update_message):
    """Notify user of system update"""
    NotificationManager.create_notification(
        user_id=user_id,
        title=update_title,
        message=update_message,
        type='success'
    )

def notify_error(user_id, error_title, error_message):
    """Notify user of error"""
    NotificationManager.create_notification(
        user_id=user_id,
        title=error_title,
        message=error_message,
        type='error'
    )

def notify_payment_success(user_id, amount, service):
    """Notify user of successful payment"""
    NotificationManager.create_notification(
        user_id=user_id,
        title="Payment Successful",
        message=f"Your payment of ${amount} for {service} was processed successfully.",
        type='success'
    )

def notify_subscription_expiry(user_id, days_remaining):
    """Notify user of subscription expiry"""
    NotificationManager.create_notification(
        user_id=user_id,
        title="Subscription Expiring Soon",
        message=f"Your subscription expires in {days_remaining} days. Renew now to continue using all features.",
        type='warning'
    )

# Auto-create some demo notifications
def create_demo_notifications():
    """Create demo notifications for testing"""
    demo_user = 'guest'
    
    notifications = [
        {
            'title': 'Welcome to AI Agents Platform!',
            'message': 'Explore our 13 unique AI agents and start your journey.',
            'type': 'success'
        },
        {
            'title': 'New Feature: Real-time Chat',
            'message': 'Experience instant responses with our enhanced chat system.',
            'type': 'info'
        },
        {
            'title': 'Strategist Agent Response',
            'message': 'Your strategic analysis is ready for review.',
            'type': 'info',
            'agent_id': 'strategist'
        },
        {
            'title': 'System Maintenance',
            'message': 'Scheduled maintenance tonight from 2-4 AM EST.',
            'type': 'warning'
        }
    ]
    
    for notif in notifications:
        NotificationManager.create_notification(
            user_id=demo_user,
            title=notif['title'],
            message=notif['message'],
            type=notif['type'],
            agent_id=notif.get('agent_id')
        )

# Initialize demo notifications on import
create_demo_notifications()