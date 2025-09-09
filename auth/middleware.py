"""
Passage Authentication Middleware
"""
from functools import wraps
from flask import request, jsonify, session, redirect, url_for, current_app, g
from .client import passage_client
import os

def auth_required(f):
    """Decorator to require Passage authentication for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated via session
        if 'user_info' in session and 'passage_token' in session:
            # Validate the Passage token
            token_result = passage_client.validate_token(session['passage_token'])
            if token_result['success']:
                g.current_user = token_result['user']
                return f(*args, **kwargs)
            else:
                # Token is invalid, clear session
                session.clear()
        
        # Check for API authentication via Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            token_result = passage_client.validate_token(token)
            if token_result['success']:
                # Store user info in request context for API calls
                g.current_user = token_result['user']
                request.user_info = token_result
                return f(*args, **kwargs)
            else:
                return jsonify({'error': 'Invalid or expired Passage token'}), 401
        
        # Not authenticated - redirect to login for web requests
        if request.is_json:
            return jsonify({'error': 'Authentication required'}), 401
        else:
            return redirect(url_for('auth.login'))
    
    return decorated_function

def admin_required(f):
    """Decorator to require admin role (stored in user metadata)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # First check if user is authenticated
        if 'user_info' not in session:
            if request.is_json:
                return jsonify({'error': 'Authentication required'}), 401
            else:
                return redirect(url_for('auth.login'))
        
        # Check if user has admin role (this would be stored in your user database)
        user_id = session.get('user_info', {}).get('user_id')
        if not user_id:
            if request.is_json:
                return jsonify({'error': 'Invalid user session'}), 401
            else:
                return redirect(url_for('auth.login'))
        
        # You would implement role checking against your database here
        # For now, we'll check a simple metadata field
        user_metadata = session.get('user_info', {}).get('user_metadata', {})
        if not user_metadata.get('is_admin', False):
            if request.is_json:
                return jsonify({'error': 'Admin access required'}), 403
            else:
                return jsonify({'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

def get_current_user():
    """Get current authenticated user info"""
    if hasattr(g, 'current_user'):
        return g.current_user
    
    if 'user_info' in session:
        return session['user_info']
    
    # Check API authentication
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        token_result = passage_client.validate_token(token)
        if token_result['success']:
            return token_result['user']
    
    return None

def passage_webhook_required(f):
    """Decorator to validate Passage webhook signatures"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        signature = request.headers.get('Passage-Signature')
        if not signature:
            return jsonify({'error': 'Missing webhook signature'}), 401
        
        payload = request.get_data(as_text=True)
        if not passage_client.verify_webhook(payload, signature):
            return jsonify({'error': 'Invalid webhook signature'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

class PassageMiddleware:
    """Passage authentication middleware class"""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the middleware with Flask app"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
    
    def before_request(self):
        """Process request before handling"""
        # Skip authentication for certain endpoints
        exempt_endpoints = [
            'auth.login',
            'auth.logout',
            'auth.callback',
            'auth.magic_link',
            'auth.verify_magic_link',
            'auth.webhook',
            'static',
            'index',  # Homepage
            'health_check'
        ]
        
        if request.endpoint in exempt_endpoints:
            return
        
        # Initialize current_user in g
        g.current_user = None
        
        # Check for valid session or token
        if 'passage_token' in session:
            token_result = passage_client.validate_token(session['passage_token'])
            if token_result['success']:
                g.current_user = token_result['user']
    
    def after_request(self, response):
        """Process response after handling"""
        # Add security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
        
        # Add CORS headers for API endpoints
        if request.path.startswith('/api/'):
            response.headers['Access-Control-Allow-Origin'] = os.getenv('CORS_ORIGIN', '*')
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        
        return response

def auth_required(f):
    """Decorator to require authentication for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated
        if 'access_token' not in session:
            if request.is_json:
                return jsonify({'error': 'Authentication required'}), 401
            else:
                return redirect(url_for('auth.login'))
        
        # Verify token is still valid
        token = session.get('access_token')
        user_info = keycloak_client.verify_token(token)
        
        if not user_info:
            # Token is invalid, clear session
            session.clear()
            if request.is_json:
                return jsonify({'error': 'Invalid or expired token'}), 401
            else:
                return redirect(url_for('auth.login'))
        
        # Add user info to request context
        request.user = user_info
        
        return f(*args, **kwargs)
    
    return decorated_function

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'access_token' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        
        token = session.get('access_token')
        user_info = keycloak_client.verify_token(token)
        
        if not user_info:
            return jsonify({'error': 'Invalid token'}), 401
        
        # Check for admin role
        roles = user_info.get('realm_access', {}).get('roles', [])
        if 'admin' not in roles:
            return jsonify({'error': 'Admin access required'}), 403
        
        request.user = user_info
        return f(*args, **kwargs)
    
    return decorated_function

def agent_access_required(agent_name):
    """Decorator to require access to specific agent"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'access_token' not in session:
                return jsonify({'error': 'Authentication required'}), 401
            
            token = session.get('access_token')
            user_info = keycloak_client.verify_token(token)
            
            if not user_info:
                return jsonify({'error': 'Invalid token'}), 401
            
            # Check agent access permissions
            # This would typically check against user's subscription or permissions
            user_permissions = user_info.get('agent_permissions', [])
            
            if agent_name not in user_permissions and 'all_agents' not in user_permissions:
                return jsonify({'error': f'Access to {agent_name} agent not permitted'}), 403
            
            request.user = user_info
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

class AuthMiddleware:
    """Authentication middleware for Flask app"""
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize middleware with Flask app"""
        app.before_request(self.before_request)
    
    def before_request(self):
        """Process request before handling"""
        # Skip auth check for public routes
        public_routes = [
            '/', '/health', '/static', '/auth/login', '/auth/callback',
            '/legal/privacy', '/legal/terms', '/legal/cookies'
        ]
        
        if any(request.path.startswith(route) for route in public_routes):
            return
        
        # Skip auth for API health checks
        if request.path == '/api/health':
            return
        
        # For all other routes, we might want to check authentication
        # but not enforce it (let individual routes decide)
        if 'access_token' in session:
            token = session.get('access_token')
            user_info = keycloak_client.verify_token(token)
            if user_info:
                request.user = user_info