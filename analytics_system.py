"""
Dashboard analytics and metrics system
"""
from flask import Blueprint, render_template, jsonify, request, session
from datetime import datetime, timedelta
import json
import random

analytics_bp = Blueprint('analytics', __name__)

# Mock analytics data (replace with actual database queries)
class AnalyticsManager:
    """Manage analytics and metrics"""
    
    @staticmethod
    def get_user_metrics(user_id, days=30):
        """Get user engagement metrics"""
        # Mock data for demo
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Generate mock daily data
        daily_data = []
        for i in range(days):
            date = start_date + timedelta(days=i)
            daily_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'messages_sent': random.randint(5, 25),
                'agents_used': random.randint(1, 5),
                'session_duration': random.randint(10, 120),  # minutes
                'features_used': random.randint(2, 8)
            })
        
        # Calculate totals
        total_messages = sum(day['messages_sent'] for day in daily_data)
        total_sessions = len([day for day in daily_data if day['messages_sent'] > 0])
        avg_session_duration = sum(day['session_duration'] for day in daily_data) / len(daily_data)
        unique_agents = set()
        for day in daily_data:
            unique_agents.update(range(day['agents_used']))
        
        return {
            'period': f'{days} days',
            'total_messages': total_messages,
            'total_sessions': total_sessions,
            'avg_session_duration': round(avg_session_duration, 1),
            'unique_agents_used': len(unique_agents),
            'daily_data': daily_data,
            'growth_rate': random.uniform(5, 25)  # Mock growth percentage
        }
    
    @staticmethod
    def get_agent_usage_stats(user_id=None, days=30):
        """Get agent usage statistics"""
        agents = [
            'strategist', 'healer', 'scout', 'analyst', 'creator', 'guardian',
            'mentor', 'innovator', 'diplomat', 'explorer', 'sage', 'catalyst', 'architect'
        ]
        
        agent_stats = []
        for agent in agents:
            agent_stats.append({
                'agent_id': agent,
                'agent_name': agent.title(),
                'total_interactions': random.randint(50, 500),
                'avg_response_time': random.uniform(1.2, 3.5),  # seconds
                'satisfaction_score': random.uniform(4.2, 4.9),
                'popular_topics': [
                    f'{agent} topic 1',
                    f'{agent} topic 2',
                    f'{agent} topic 3'
                ],
                'usage_trend': random.choice(['up', 'down', 'stable'])
            })
        
        # Sort by usage
        agent_stats.sort(key=lambda x: x['total_interactions'], reverse=True)
        
        return agent_stats
    
    @staticmethod
    def get_platform_metrics():
        """Get overall platform metrics"""
        return {
            'total_users': random.randint(10000, 50000),
            'active_users_today': random.randint(500, 2000),
            'total_conversations': random.randint(100000, 500000),
            'messages_today': random.randint(5000, 20000),
            'avg_response_time': random.uniform(1.5, 2.5),
            'uptime_percentage': random.uniform(99.5, 99.9),
            'top_features': [
                {'name': 'AI Chat', 'usage': random.randint(80, 95)},
                {'name': 'Strategy Planning', 'usage': random.randint(60, 80)},
                {'name': 'Data Analysis', 'usage': random.randint(50, 70)},
                {'name': 'Wellness Coaching', 'usage': random.randint(40, 60)},
                {'name': 'Research Tools', 'usage': random.randint(30, 50)}
            ]
        }
    
    @staticmethod
    def get_performance_metrics():
        """Get system performance metrics"""
        return {
            'server_response_time': random.uniform(0.1, 0.5),
            'database_query_time': random.uniform(0.05, 0.2),
            'ai_model_response_time': random.uniform(1.0, 3.0),
            'memory_usage': random.uniform(40, 80),
            'cpu_usage': random.uniform(20, 60),
            'active_connections': random.randint(100, 500),
            'queue_size': random.randint(0, 20),
            'error_rate': random.uniform(0.1, 2.0)
        }

@analytics_bp.route('/dashboard/analytics')
def analytics_dashboard():
    """Analytics dashboard page"""
    user_id = session.get('user_id', 'guest')
    
    # Get analytics data
    user_metrics = AnalyticsManager.get_user_metrics(user_id)
    agent_stats = AnalyticsManager.get_agent_usage_stats(user_id)
    platform_metrics = AnalyticsManager.get_platform_metrics()
    performance_metrics = AnalyticsManager.get_performance_metrics()
    
    return render_template('dashboard/analytics.html',
                         user_metrics=user_metrics,
                         agent_stats=agent_stats,
                         platform_metrics=platform_metrics,
                         performance_metrics=performance_metrics)

@analytics_bp.route('/api/analytics/user-metrics')
def api_user_metrics():
    """API endpoint for user metrics"""
    user_id = session.get('user_id', 'guest')
    days = int(request.args.get('days', 30))
    
    metrics = AnalyticsManager.get_user_metrics(user_id, days)
    
    return jsonify({
        'success': True,
        'metrics': metrics
    })

@analytics_bp.route('/api/analytics/agent-usage')
def api_agent_usage():
    """API endpoint for agent usage statistics"""
    user_id = session.get('user_id', 'guest')
    days = int(request.args.get('days', 30))
    
    stats = AnalyticsManager.get_agent_usage_stats(user_id, days)
    
    return jsonify({
        'success': True,
        'agent_stats': stats
    })

@analytics_bp.route('/api/analytics/platform-metrics')
def api_platform_metrics():
    """API endpoint for platform metrics"""
    metrics = AnalyticsManager.get_platform_metrics()
    
    return jsonify({
        'success': True,
        'platform_metrics': metrics
    })

@analytics_bp.route('/api/analytics/performance')
def api_performance_metrics():
    """API endpoint for performance metrics"""
    metrics = AnalyticsManager.get_performance_metrics()
    
    return jsonify({
        'success': True,
        'performance_metrics': metrics
    })

@analytics_bp.route('/api/analytics/export')
def export_analytics():
    """Export analytics data"""
    user_id = session.get('user_id', 'guest')
    format_type = request.args.get('format', 'json')
    days = int(request.args.get('days', 30))
    
    # Gather all analytics data
    data = {
        'user_metrics': AnalyticsManager.get_user_metrics(user_id, days),
        'agent_stats': AnalyticsManager.get_agent_usage_stats(user_id, days),
        'platform_metrics': AnalyticsManager.get_platform_metrics(),
        'performance_metrics': AnalyticsManager.get_performance_metrics(),
        'exported_at': datetime.utcnow().isoformat(),
        'user_id': user_id
    }
    
    if format_type == 'json':
        return jsonify({
            'success': True,
            'data': data,
            'export_format': 'json'
        })
    elif format_type == 'csv':
        # Simple CSV export (in real implementation, use pandas or csv module)
        csv_data = "metric,value,date\n"
        for day in data['user_metrics']['daily_data']:
            csv_data += f"messages_sent,{day['messages_sent']},{day['date']}\n"
            csv_data += f"agents_used,{day['agents_used']},{day['date']}\n"
            csv_data += f"session_duration,{day['session_duration']},{day['date']}\n"
        
        return csv_data, 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': f'attachment; filename=analytics_{user_id}_{days}days.csv'
        }
    
    return jsonify({
        'success': False,
        'message': 'Unsupported export format'
    }), 400

@analytics_bp.route('/api/analytics/insights')
def get_insights():
    """Get AI-generated insights from analytics data"""
    user_id = session.get('user_id', 'guest')
    
    # Mock AI insights (replace with actual AI analysis)
    insights = [
        {
            'type': 'trend',
            'title': 'Increased Agent Usage',
            'description': 'Your usage of AI agents has increased by 23% this week.',
            'recommendation': 'Consider exploring advanced features of your most-used agents.',
            'confidence': 0.85
        },
        {
            'type': 'pattern',
            'title': 'Peak Activity Hours',
            'description': 'You are most active between 9-11 AM and 2-4 PM.',
            'recommendation': 'Schedule complex tasks during these high-productivity hours.',
            'confidence': 0.92
        },
        {
            'type': 'opportunity',
            'title': 'Underutilized Features',
            'description': 'You haven\'t used the Data Analyst agent in the past week.',
            'recommendation': 'Try using the Analyst for your next data-related task.',
            'confidence': 0.78
        },
        {
            'type': 'achievement',
            'title': 'Consistency Streak',
            'description': 'You\'ve maintained daily platform usage for 15 days!',
            'recommendation': 'Keep up the great momentum and explore new agents.',
            'confidence': 1.0
        }
    ]
    
    return jsonify({
        'success': True,
        'insights': insights,
        'generated_at': datetime.utcnow().isoformat()
    })