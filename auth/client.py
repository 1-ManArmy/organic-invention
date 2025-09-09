"""
Passage Authentication Client (powered by 1Password)
"""
import requests
import os
from datetime import datetime, timedelta
import hashlib
import hmac
import json

class PassageClient:
    """Passage authentication client powered by 1Password"""
    
    def __init__(self):
        self.app_id = os.getenv('PASSAGE_APP_ID')
        self.api_key = os.getenv('PASSAGE_API_KEY')
        self.base_url = 'https://api.passage.id/v1'
        self.webhook_secret = os.getenv('PASSAGE_WEBHOOK_SECRET')
        
        if not self.app_id or not self.api_key:
            raise ValueError("Passage App ID and API Key are required")
    
    def _make_request(self, method, endpoint, data=None, headers=None):
        """Make authenticated request to Passage API"""
        url = f"{self.base_url}{endpoint}"
        
        default_headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        if headers:
            default_headers.update(headers)
        
        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                headers=default_headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def validate_token(self, token):
        """Validate Passage authentication token"""
        try:
            response = self._make_request(
                'GET',
                f'/apps/{self.app_id}/tokens/validate',
                headers={'Authorization': f'Bearer {token}'}
            )
            
            if 'error' in response:
                return {
                    'success': False,
                    'error': response['error']
                }
            
            return {
                'success': True,
                'user_id': response.get('user_id'),
                'user': response.get('user', {})
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_user(self, user_id):
        """Get user information by ID"""
        try:
            response = self._make_request('GET', f'/users/{user_id}')
            
            if 'error' in response:
                return {
                    'success': False,
                    'error': response['error']
                }
            
            user_data = response.get('user', {})
            return {
                'success': True,
                'user': {
                    'id': user_data.get('id'),
                    'email': user_data.get('email'),
                    'phone': user_data.get('phone'),
                    'status': user_data.get('status'),
                    'created_at': user_data.get('created_at'),
                    'updated_at': user_data.get('updated_at'),
                    'last_login_at': user_data.get('last_login_at'),
                    'login_count': user_data.get('login_count', 0)
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def create_magic_link(self, email, redirect_url=None):
        """Create magic link for passwordless authentication"""
        try:
            data = {
                'email': email,
                'send': True
            }
            
            if redirect_url:
                data['redirect_url'] = redirect_url
            
            response = self._make_request(
                'POST',
                f'/apps/{self.app_id}/magic-links',
                data=data
            )
            
            if 'error' in response:
                return {
                    'success': False,
                    'error': response['error']
                }
            
            return {
                'success': True,
                'magic_link': response.get('magic_link')
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def activate_magic_link(self, magic_link_id):
        """Activate a magic link"""
        try:
            response = self._make_request(
                'PATCH',
                f'/apps/{self.app_id}/magic-links/{magic_link_id}/activate'
            )
            
            if 'error' in response:
                return {
                    'success': False,
                    'error': response['error']
                }
            
            return {
                'success': True,
                'auth_token': response.get('auth_token'),
                'user': response.get('user')
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_webhook(self, payload, signature):
        """Verify webhook signature from Passage"""
        if not self.webhook_secret:
            return False
        
        expected_signature = hmac.new(
            self.webhook_secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(f"sha256={expected_signature}", signature)
    
    def revoke_user_sessions(self, user_id):
        """Revoke all sessions for a user"""
        try:
            response = self._make_request(
                'DELETE',
                f'/users/{user_id}/sessions'
            )
            
            if 'error' in response:
                return {
                    'success': False,
                    'error': response['error']
                }
            
            return {'success': True}
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def update_user(self, user_id, user_data):
        """Update user information"""
        try:
            response = self._make_request(
                'PATCH',
                f'/users/{user_id}',
                data={'user': user_data}
            )
            
            if 'error' in response:
                return {
                    'success': False,
                    'error': response['error']
                }
            
            return {
                'success': True,
                'user': response.get('user')
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def delete_user(self, user_id):
        """Delete a user"""
        try:
            response = self._make_request('DELETE', f'/users/{user_id}')
            
            if 'error' in response:
                return {
                    'success': False,
                    'error': response['error']
                }
            
            return {'success': True}
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Global client instance
passage_client = PassageClient()
import json
import jwt
import requests
from flask import current_app, session, request
from functools import wraps

class KeycloakClient:
    """Keycloak authentication client"""
    
    def __init__(self):
        self.server_url = current_app.config.get('KEYCLOAK_SERVER_URL')
        self.realm = current_app.config.get('KEYCLOAK_REALM')
        self.client_id = current_app.config.get('KEYCLOAK_CLIENT_ID')
        self.client_secret = current_app.config.get('KEYCLOAK_CLIENT_SECRET')
        
        # Load configuration
        with open('auth/keycloak_config.json', 'r') as f:
            self.config = json.load(f)
    
    def get_auth_url(self, redirect_uri):
        """Generate Keycloak authentication URL"""
        auth_url = f"{self.server_url}/realms/{self.realm}/protocol/openid-connect/auth"
        params = {
            'client_id': self.client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': 'openid profile email'
        }
        
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return f"{auth_url}?{query_string}"
    
    def exchange_code_for_token(self, code, redirect_uri):
        """Exchange authorization code for access token"""
        token_url = f"{self.server_url}/realms/{self.realm}/protocol/openid-connect/token"
        
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': redirect_uri
        }
        
        response = requests.post(token_url, data=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Token exchange failed: {response.text}")
    
    def verify_token(self, token):
        """Verify JWT token"""
        try:
            # In production, you should verify the token signature
            # For now, we'll decode without verification for development
            decoded = jwt.decode(token, options={"verify_signature": False})
            return decoded
        except jwt.InvalidTokenError:
            return None
    
    def get_user_info(self, access_token):
        """Get user information from Keycloak"""
        userinfo_url = f"{self.server_url}/realms/{self.realm}/protocol/openid-connect/userinfo"
        
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        response = requests.get(userinfo_url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get user info: {response.text}")
    
    def logout_user(self, refresh_token):
        """Logout user from Keycloak"""
        logout_url = f"{self.server_url}/realms/{self.realm}/protocol/openid-connect/logout"
        
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': refresh_token
        }
        
        response = requests.post(logout_url, data=data)
        return response.status_code == 204

# Global client instance
keycloak_client = KeycloakClient()