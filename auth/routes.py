"""
Passage Authentication Routes
"""
from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template, flash, g
from .client import passage_client
from .middleware import passage_webhook_required
import os
import json

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and magic link handler"""
    if request.method == 'GET':
        return render_template('auth/login.html', title='Login - Passwordless Authentication')
    
    # Handle magic link request
    email = request.form.get('email')
    
    if not email:
        flash('Email address is required', 'error')
        return render_template('auth/login.html', title='Login - Passwordless Authentication')
    
    # Create magic link with Passage
    redirect_url = url_for('auth.callback', _external=True)
    result = passage_client.create_magic_link(email, redirect_url)
    
    if result['success']:
        flash('Magic link sent! Check your email to complete login.', 'success')
        return render_template('auth/login.html', 
                             title='Login - Passwordless Authentication',
                             magic_link_sent=True,
                             email=email)
    else:
        flash(f'Failed to send magic link: {result["error"]}', 'error')
    
    return render_template('auth/login.html', title='Login - Passwordless Authentication')

@auth_bp.route('/logout')
def logout():
    """Logout handler"""
    user_id = session.get('user_info', {}).get('id')
    
    # Revoke user sessions in Passage
    if user_id:
        passage_client.revoke_user_sessions(user_id)
    
    # Clear session
    session.clear()
    
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('index'))

@auth_bp.route('/callback')
def callback():
    """Passage authentication callback handler"""
    # Get the auth token from query parameters
    auth_token = request.args.get('psg_auth_token')
    magic_link_id = request.args.get('psg_magic_link_id')
    
    if not auth_token and magic_link_id:
        # Activate magic link to get auth token
        result = passage_client.activate_magic_link(magic_link_id)
        if result['success']:
            auth_token = result['auth_token']
        else:
            flash('Invalid or expired magic link', 'error') 
            return redirect(url_for('auth.login'))
    
    if not auth_token:
        flash('Authentication failed - no auth token provided', 'error')
        return redirect(url_for('auth.login'))
    
    # Validate the auth token
    token_result = passage_client.validate_token(auth_token)
    
    if token_result['success']:
        user_id = token_result['user_id']
        
        # Get full user information
        user_result = passage_client.get_user(user_id)
        
        if user_result['success']:
            # Store in session
            session['passage_token'] = auth_token
            session['user_info'] = user_result['user']
            
            # Redirect to dashboard or intended page
            next_page = request.args.get('next', url_for('dashboard.home'))
            return redirect(next_page)
        else:
            flash('Failed to get user information', 'error')
    else:
        flash(f'Authentication failed: {token_result["error"]}', 'error')
    
    return redirect(url_for('auth.login'))

@auth_bp.route('/magic-link', methods=['POST'])
def magic_link():
    """API endpoint to create magic link"""
    data = request.get_json()
    
    if not data or 'email' not in data:
        return jsonify({'error': 'Email is required'}), 400
    
    email = data['email']
    redirect_url = data.get('redirect_url', url_for('auth.callback', _external=True))
    
    result = passage_client.create_magic_link(email, redirect_url)
    
    if result['success']:
        return jsonify({
            'success': True,
            'message': 'Magic link sent successfully',
            'magic_link': result.get('magic_link')
        })
    else:
        return jsonify({
            'error': result['error']
        }), 400

@auth_bp.route('/verify-magic-link/<magic_link_id>', methods=['POST'])
def verify_magic_link(magic_link_id):
    """Verify and activate magic link"""
    result = passage_client.activate_magic_link(magic_link_id)
    
    if result['success']:
        return jsonify({
            'success': True,
            'auth_token': result['auth_token'],
            'user': result['user']
        })
    else:
        return jsonify({
            'error': result['error']
        }), 400

@auth_bp.route('/profile', methods=['GET', 'PUT'])
def profile():
    """User profile page and update handler"""
    if 'user_info' not in session:
        return redirect(url_for('auth.login'))
    
    user_info = session['user_info']
    
    if request.method == 'GET':
        return render_template('auth/profile.html', 
                             user=user_info, 
                             title='User Profile')
    
    # Handle profile update
    if request.method == 'PUT':
        data = request.get_json()
        user_id = user_info['id']
        
        # Update user in Passage
        result = passage_client.update_user(user_id, data)
        
        if result['success']:
            # Update session with new user data
            session['user_info'] = result['user']
            return jsonify({
                'success': True,
                'user': result['user']
            })
        else:
            return jsonify({
                'error': result['error']
            }), 400

@auth_bp.route('/webhook', methods=['POST'])
@passage_webhook_required
def webhook():
    """Passage webhook handler"""
    try:
        payload = request.get_json()
        event_type = payload.get('type')
        
        if event_type == 'user.created':
            # Handle new user creation
            user_data = payload.get('user', {})
            # You could create corresponding user record in your database here
            pass
        
        elif event_type == 'user.updated':
            # Handle user updates
            user_data = payload.get('user', {})
            # Update corresponding user record in your database
            pass
        
        elif event_type == 'user.deleted':
            # Handle user deletion
            user_id = payload.get('user_id')
            # Delete corresponding user record from your database
            pass
        
        elif event_type == 'login.succeeded':
            # Handle successful login
            user_data = payload.get('user', {})
            # Log successful login, update last_login timestamp, etc.
            pass
        
        elif event_type == 'login.failed':
            # Handle failed login attempt
            # Log failed attempt for security monitoring
            pass
        
        return jsonify({'received': True}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/status')
def status():
    """Check authentication status"""
    if 'user_info' in session:
        user = session['user_info']
        return jsonify({
            'authenticated': True,
            'user': {
                'id': user.get('id'),
                'email': user.get('email'),
                'phone': user.get('phone'),
                'status': user.get('status'),
                'created_at': user.get('created_at'),
                'last_login_at': user.get('last_login_at')
            }
        })
    else:
        return jsonify({'authenticated': False})

@auth_bp.route('/delete-account', methods=['POST'])
def delete_account():
    """Delete user account"""
    if 'user_info' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    user_id = session['user_info']['id']
    
    # Delete user from Passage
    result = passage_client.delete_user(user_id)
    
    if result['success']:
        # Clear session
        session.clear()
        
        return jsonify({
            'success': True,
            'message': 'Account deleted successfully'
        })
    else:
        return jsonify({
            'error': result['error']
        }), 400

@auth_bp.route('/login')
def login():
    """Initiate login with Keycloak"""
    redirect_uri = url_for('auth.callback', _external=True)
    auth_url = keycloak_client.get_auth_url(redirect_uri)
    return redirect(auth_url)

@auth_bp.route('/callback')
def callback():
    """Handle Keycloak callback"""
    code = request.args.get('code')
    error = request.args.get('error')
    
    if error:
        return jsonify({'error': f'Authentication failed: {error}'}), 400
    
    if not code:
        return jsonify({'error': 'No authorization code received'}), 400
    
    try:
        # Exchange code for tokens
        redirect_uri = url_for('auth.callback', _external=True)
        tokens = keycloak_client.exchange_code_for_token(code, redirect_uri)
        
        # Store tokens in session
        session['access_token'] = tokens['access_token']
        session['refresh_token'] = tokens.get('refresh_token')
        session['id_token'] = tokens.get('id_token')
        
        # Get user info
        user_info = keycloak_client.get_user_info(tokens['access_token'])
        session['user_info'] = user_info
        
        # Redirect to dashboard or originally requested page
        next_page = session.pop('next_page', url_for('dashboard.home'))
        return redirect(next_page)
        
    except Exception as e:
        return jsonify({'error': f'Login failed: {str(e)}'}), 500

@auth_bp.route('/logout')
def logout():
    """Logout user"""
    refresh_token = session.get('refresh_token')
    
    # Logout from Keycloak if refresh token available
    if refresh_token:
        try:
            keycloak_client.logout_user(refresh_token)
        except:
            pass  # Continue with local logout even if Keycloak logout fails
    
    # Clear session
    session.clear()
    
    return redirect(url_for('homepage'))

@auth_bp.route('/profile')
def profile():
    """User profile page"""
    if 'user_info' not in session:
        return redirect(url_for('auth.login'))
    
    user_info = session['user_info']
    return render_template('auth/profile.html', user=user_info)

@auth_bp.route('/api/me')
def api_me():
    """Get current user info via API"""
    if 'user_info' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    return jsonify(session['user_info'])

@auth_bp.route('/api/verify')
def api_verify():
    """Verify token endpoint"""
    access_token = session.get('access_token')
    
    if not access_token:
        return jsonify({'valid': False, 'error': 'No token'}), 401
    
    user_info = keycloak_client.verify_token(access_token)
    
    if user_info:
        return jsonify({'valid': True, 'user': user_info})
    else:
        return jsonify({'valid': False, 'error': 'Invalid token'}), 401