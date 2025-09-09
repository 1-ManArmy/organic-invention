"""
Database Models
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication and profile management"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    passage_id = db.Column(db.String(255), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    
    # Profile information
    profile_picture = db.Column(db.String(255))
    bio = db.Column(db.Text)
    timezone = db.Column(db.String(50), default='UTC')
    language = db.Column(db.String(10), default='en')
    
    # Subscription and usage
    subscription_plan = db.Column(db.String(50), default='free')
    subscription_status = db.Column(db.String(20), default='inactive')
    subscription_expires = db.Column(db.DateTime(timezone=True))
    credits_remaining = db.Column(db.Integer, default=100)
    credits_used_total = db.Column(db.Integer, default=0)
    
    # Preferences
    preferred_agents = db.Column(db.JSON)  # List of favorite agent IDs
    notification_preferences = db.Column(db.JSON)
    theme_preference = db.Column(db.String(20), default='light')
    
    # Timestamps
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime(timezone=True))
    last_active = db.Column(db.DateTime(timezone=True))
    
    # Status flags
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    is_premium = db.Column(db.Boolean, default=False)
    
    # Relationships
    conversations = db.relationship('Conversation', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic')
    agent_logs = db.relationship('AgentLog', backref='user', lazy='dynamic')
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if not self.preferred_agents:
            self.preferred_agents = []
        if not self.notification_preferences:
            self.notification_preferences = {
                'email_notifications': True,
                'push_notifications': True,
                'marketing_emails': False,
                'agent_updates': True
            }
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'subscription_plan': self.subscription_plan,
            'subscription_status': self.subscription_status,
            'credits_remaining': self.credits_remaining,
            'is_premium': self.is_premium,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def update_last_active(self):
        """Update the last active timestamp"""
        self.last_active = datetime.now(timezone.utc)
        db.session.commit()
    
    def add_credits(self, amount):
        """Add credits to user account"""
        self.credits_remaining += amount
        db.session.commit()
    
    def use_credits(self, amount):
        """Use credits from user account"""
        if self.credits_remaining >= amount:
            self.credits_remaining -= amount
            self.credits_used_total += amount
            db.session.commit()
            return True
        return False
    
    def __repr__(self):
        return f'<User {self.username}>'

class Conversation(db.Model):
    """Conversation model for tracking user interactions with agents"""
    __tablename__ = 'conversations'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    agent_id = db.Column(db.String(50), nullable=False, index=True)
    
    # Conversation metadata
    title = db.Column(db.String(200))
    summary = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')  # active, archived, deleted
    
    # Message tracking
    message_count = db.Column(db.Integer, default=0)
    total_tokens = db.Column(db.Integer, default=0)
    credits_used = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    # Relationships
    messages = db.relationship('Message', backref='conversation', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert conversation to dictionary"""
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'title': self.title,
            'summary': self.summary,
            'status': self.status,
            'message_count': self.message_count,
            'credits_used': self.credits_used,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Conversation {self.id} - {self.agent_id}>'

class Message(db.Model):
    """Message model for individual messages within conversations"""
    __tablename__ = 'messages'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = db.Column(db.String(36), db.ForeignKey('conversations.id'), nullable=False, index=True)
    
    # Message content
    role = db.Column(db.String(20), nullable=False)  # user, assistant, system
    content = db.Column(db.Text, nullable=False)
    
    # Metadata
    tokens = db.Column(db.Integer, default=0)
    processing_time = db.Column(db.Float)  # in seconds
    model_used = db.Column(db.String(100))
    
    # Timestamps
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))
    
    def to_dict(self):
        """Convert message to dictionary"""
        return {
            'id': self.id,
            'role': self.role,
            'content': self.content,
            'tokens': self.tokens,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Message {self.id} - {self.role}>'

class Transaction(db.Model):
    """Transaction model for payment and subscription tracking"""
    __tablename__ = 'transactions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Transaction details
    transaction_type = db.Column(db.String(50), nullable=False)  # subscription, credits, one_time
    amount = db.Column(db.Decimal(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='USD')
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed, refunded
    
    # Payment provider information
    provider = db.Column(db.String(50))  # stripe, paypal, lemonsqueezy
    provider_transaction_id = db.Column(db.String(255), index=True)
    provider_customer_id = db.Column(db.String(255))
    
    # Transaction metadata
    description = db.Column(db.String(500))
    credits_granted = db.Column(db.Integer, default=0)
    subscription_months = db.Column(db.Integer, default=0)
    
    # Webhook and processing info
    webhook_received = db.Column(db.Boolean, default=False)
    processed_at = db.Column(db.DateTime(timezone=True))
    
    # Timestamps
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    def to_dict(self):
        """Convert transaction to dictionary"""
        return {
            'id': self.id,
            'transaction_type': self.transaction_type,
            'amount': float(self.amount),
            'currency': self.currency,
            'status': self.status,
            'provider': self.provider,
            'description': self.description,
            'credits_granted': self.credits_granted,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def mark_completed(self):
        """Mark transaction as completed and process benefits"""
        self.status = 'completed'
        self.processed_at = datetime.now(timezone.utc)
        
        # Grant credits to user if applicable
        if self.credits_granted > 0:
            self.user.add_credits(self.credits_granted)
        
        db.session.commit()
    
    def __repr__(self):
        return f'<Transaction {self.id} - {self.amount} {self.currency}>'

class AgentLog(db.Model):
    """Agent interaction logging for analytics and debugging"""
    __tablename__ = 'agent_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    agent_id = db.Column(db.String(50), nullable=False, index=True)
    
    # Interaction details
    action = db.Column(db.String(100), nullable=False)  # chat, initialize, configure, etc.
    session_id = db.Column(db.String(100), index=True)
    
    # Performance metrics
    response_time = db.Column(db.Float)  # in seconds
    tokens_used = db.Column(db.Integer, default=0)
    credits_consumed = db.Column(db.Integer, default=0)
    
    # Request/Response data
    request_data = db.Column(db.JSON)
    response_data = db.Column(db.JSON)
    error_message = db.Column(db.Text)
    
    # Client information
    user_agent = db.Column(db.String(500))
    ip_address = db.Column(db.String(45))  # Supports IPv6
    
    # Timestamps
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))
    
    def to_dict(self):
        """Convert agent log to dictionary"""
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'action': self.action,
            'response_time': self.response_time,
            'tokens_used': self.tokens_used,
            'credits_consumed': self.credits_consumed,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<AgentLog {self.id} - {self.agent_id}:{self.action}>'

class APIKey(db.Model):
    """API Key model for programmatic access"""
    __tablename__ = 'api_keys'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Key details
    name = db.Column(db.String(100), nullable=False)
    key_hash = db.Column(db.String(255), nullable=False, unique=True)
    key_prefix = db.Column(db.String(20), nullable=False)  # First few characters for identification
    
    # Permissions and limits
    scopes = db.Column(db.JSON)  # List of allowed scopes
    rate_limit = db.Column(db.Integer, default=1000)  # Requests per hour
    is_active = db.Column(db.Boolean, default=True)
    
    # Usage tracking
    last_used = db.Column(db.DateTime(timezone=True))
    total_requests = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))
    expires_at = db.Column(db.DateTime(timezone=True))
    
    # Relationship
    user = db.relationship('User', backref='api_keys')
    
    def generate_key(self):
        """Generate a new API key"""
        import secrets
        key = f"sk-{secrets.token_urlsafe(32)}"
        self.key_hash = generate_password_hash(key)
        self.key_prefix = key[:12]
        return key
    
    def verify_key(self, key):
        """Verify an API key"""
        return check_password_hash(self.key_hash, key)
    
    def record_usage(self):
        """Record API key usage"""
        self.last_used = datetime.now(timezone.utc)
        self.total_requests += 1
        db.session.commit()
    
    def __repr__(self):
        return f'<APIKey {self.name} - {self.key_prefix}...>'