"""
Dashboard Routes
"""
from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
from auth.middleware import auth_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@auth_required
def home():
    """Dashboard home page"""
    user_info = session.get('user_info', {})
    
    # Mock user statistics - in production, this would come from the database
    user_stats = {
        'total_conversations': 156,
        'favorite_agents': ['Strategist', 'Healer', 'Scout'],
        'subscription_plan': 'AI Professional',
        'credits_remaining': 3247,
        'credits_used_this_month': 1753,
        'member_since': '2024-08-15',
        'recent_activity': [
            {'agent': 'Strategist', 'action': 'Strategic planning session', 'timestamp': '2 hours ago'},
            {'agent': 'Healer', 'action': 'Wellness check-in', 'timestamp': '1 day ago'},
            {'agent': 'Scout', 'action': 'Market research', 'timestamp': '2 days ago'},
            {'agent': 'Oracle', 'action': 'Future predictions', 'timestamp': '3 days ago'}
        ]
    }
    
    return render_template('pages/dashboard/dashboard.html', 
                         user=user_info, 
                         stats=user_stats,
                         title='Dashboard')

@dashboard_bp.route('/agents')
@auth_required
def agents():
    """User's agents dashboard"""
    from agents import AGENTS_REGISTRY
    
    user_info = session.get('user_info', {})
    
    # Mock agent usage data
    agent_usage = {
        'strategist': {'conversations': 45, 'last_used': '2 hours ago', 'favorite': True},
        'healer': {'conversations': 32, 'last_used': '1 day ago', 'favorite': True},
        'scout': {'conversations': 28, 'last_used': '2 days ago', 'favorite': True},
        'archivist': {'conversations': 15, 'last_used': '5 days ago', 'favorite': False},
        'diplomat': {'conversations': 12, 'last_used': '1 week ago', 'favorite': False},
        'merchant': {'conversations': 8, 'last_used': '1 week ago', 'favorite': False},
        'guardian': {'conversations': 6, 'last_used': '2 weeks ago', 'favorite': False},
        'oracle': {'conversations': 10, 'last_used': '3 days ago', 'favorite': False},
        'tactician': {'conversations': 7, 'last_used': '1 week ago', 'favorite': False},
        'builder': {'conversations': 9, 'last_used': '4 days ago', 'favorite': False},
        'messenger': {'conversations': 5, 'last_used': '2 weeks ago', 'favorite': False},
        'analyst': {'conversations': 11, 'last_used': '6 days ago', 'favorite': False},
        'navigator': {'conversations': 4, 'last_used': '3 weeks ago', 'favorite': False}
    }
    
    # Combine registry data with usage data
    agents_data = []
    for agent_id, agent_info in AGENTS_REGISTRY.items():
        usage = agent_usage.get(agent_id, {'conversations': 0, 'last_used': 'Never', 'favorite': False})
        agents_data.append({
            **agent_info,
            'id': agent_id,
            **usage
        })
    
    return render_template('pages/dashboard/agents.html', agents=agents_data, title='My AI Agents')

@dashboard_bp.route('/subscription')
@auth_required  
def subscription():
    """User subscription management"""
    user_info = session.get('user_info', {})
    
    # Mock subscription data
    subscription_data = {
        'plan': 'AI Professional',
        'status': 'Active',
        'next_billing': '2025-10-09',
        'price': '$29.99/month',
        'credits_limit': 5000,
        'credits_used': 1753,
        'agents_access': 13,
        'features': [
            'Access to all 13 AI Agents',
            '5,000 monthly conversations', 
            '24/7 premium support',
            'Advanced analytics & insights',
            'Custom agent training',
            'API access',
            'White-label options'
        ],
        'billing_history': [
            {'date': '2025-09-09', 'amount': '$29.99', 'status': 'Paid'},
            {'date': '2025-08-09', 'amount': '$29.99', 'status': 'Paid'},
            {'date': '2025-07-09', 'amount': '$29.99', 'status': 'Paid'}
        ]
    }
    
    return render_template('pages/dashboard/subscription.html', 
                         subscription=subscription_data, 
                         title='Subscription')

@dashboard_bp.route('/analytics')
@auth_required
def analytics():
    """User analytics dashboard"""
    user_info = session.get('user_info', {})
    
    # Mock analytics data
    analytics_data = {
        'conversation_trends': {
            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
            'data': [45, 62, 58, 71, 83, 95, 102, 118, 156]
        },
        'agent_usage': {
            'labels': ['Strategist', 'Healer', 'Scout', 'Oracle', 'Analyst'],
            'data': [45, 32, 28, 10, 11]
        },
        'time_analysis': {
            'peak_hours': '2-4 PM',
            'average_session': '12 minutes',
            'total_time': '42 hours this month'
        },
        'insights': [
            'Your most productive conversations happen on Tuesdays',
            'You prefer strategic and wellness-focused agents',
            'Your engagement has increased 34% this month',
            'You tend to have longer sessions with the Strategist agent'
        ]
    }
    
    return render_template('pages/dashboard/analytics.html', 
                         analytics=analytics_data, 
                         title='Analytics')

@dashboard_bp.route('/settings')
@auth_required
def settings():
    """User settings page"""
    user_info = session.get('user_info', {})
    
    return render_template('pages/dashboard/settings.html', 
                         user=user_info, 
                         title='Settings')

@dashboard_bp.route('/api/stats')
@auth_required
def api_stats():
    """API endpoint for dashboard statistics"""
    # This would typically query your database
    stats = {
        'conversations_today': 12,
        'credits_remaining': 3247,
        'active_agents': 5,
        'subscription_status': 'active'
    }
    
    return jsonify(stats)