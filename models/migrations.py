"""
Database Migration Scripts
"""
from flask import Flask
from flask_migrate import Migrate, init, migrate, upgrade
from models.user import db, User, Conversation, Message, Transaction, AgentLog, APIKey
import os

def create_app():
    """Create Flask app for migration purposes"""
    app = Flask(__name__)
    
    # Database configuration
    database_url = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/aiagents')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate = Migrate(app, db)
    
    return app, migrate

def create_tables():
    """Create all database tables"""
    app, _ = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Create initial indexes for performance
        try:
            db.engine.execute("""
                CREATE INDEX IF NOT EXISTS idx_users_passage_id ON users(passage_id);
                CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
                CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
                CREATE INDEX IF NOT EXISTS idx_conversations_user_agent ON conversations(user_id, agent_id);
                CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id);
                CREATE INDEX IF NOT EXISTS idx_transactions_user_status ON transactions(user_id, status);
                CREATE INDEX IF NOT EXISTS idx_agent_logs_user_agent ON agent_logs(user_id, agent_id);
                CREATE INDEX IF NOT EXISTS idx_agent_logs_created_at ON agent_logs(created_at);
            """)
            print("✅ Database indexes created successfully!")
        except Exception as e:
            print(f"⚠️  Index creation warning: {e}")

def seed_database():
    """Seed database with initial data"""
    app, _ = create_app()
    
    with app.app_context():
        # Check if we already have data
        if User.query.first():
            print("Database already contains data. Skipping seed.")
            return
        
        print("🌱 Seeding database with initial data...")
        
        # Create a test user (only for development)
        if os.getenv('FLASK_ENV') == 'development':
            test_user = User(
                keycloak_id='test-user-123',
                username='testuser',
                email='test@aiagents.com',
                first_name='Test',
                last_name='User',
                subscription_plan='professional',
                subscription_status='active',
                credits_remaining=5000,
                is_active=True,
                is_verified=True,
                is_premium=True
            )
            
            db.session.add(test_user)
            db.session.commit()
            
            print("✅ Test user created: testuser")
        
        print("✅ Database seeding completed!")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python migrations.py [init|migrate|upgrade|create|seed]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'init':
        app, migrate_obj = create_app()
        with app.app_context():
            init()
            print("✅ Migration repository initialized!")
    
    elif command == 'migrate':
        app, migrate_obj = create_app()
        message = sys.argv[2] if len(sys.argv) > 2 else 'Auto migration'
        with app.app_context():
            migrate(message=message)
            print(f"✅ Migration created: {message}")
    
    elif command == 'upgrade':
        app, migrate_obj = create_app()
        with app.app_context():
            upgrade()
            print("✅ Database upgraded!")
    
    elif command == 'create':
        create_tables()
    
    elif command == 'seed':
        seed_database()
    
    else:
        print(f"Unknown command: {command}")
        print("Available commands: init, migrate, upgrade, create, seed")
        sys.exit(1)