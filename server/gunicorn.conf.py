"""
Gunicorn WSGI Server Configuration
"""

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
workers = 4
worker_class = "gevent"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
preload_app = True
timeout = 30
keepalive = 2

# Restart workers after this many requests, with up to 50 random
# requests variation to prevent thundering herd
max_requests = 1000
max_requests_jitter = 50

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'ai-agents-platform'

# Server mechanics
daemon = False
pidfile = '/tmp/gunicorn.pid'
user = None
group = None
tmp_upload_dir = None

# SSL (if using HTTPS directly through Gunicorn)
# keyfile = '/path/to/keyfile'
# certfile = '/path/to/certfile'

def when_ready(server):
    """Called just after the server is started."""
    server.log.info("🚀 AI Agents Platform server is ready to accept connections")

def worker_int(worker):
    """Called just after a worker exited on SIGINT or SIGQUIT."""
    worker.log.info("👋 Worker received INT or QUIT signal")

def pre_fork(server, worker):
    """Called just before a worker is forked."""
    server.log.info(f"🔄 Worker {worker.pid} spawned")

def post_fork(server, worker):
    """Called just after a worker has been forked."""
    server.log.info(f"✅ Worker {worker.pid} ready")

def pre_exec(server):
    """Called just before a new master process is forked."""
    server.log.info("🔄 Forked child, re-executing")

def when_ready(server):
    """Called just after the server is started."""
    server.log.info("🌟 AI Agents Platform server started successfully")

def worker_abort(worker):
    """Called when a worker received the SIGABRT signal."""
    worker.log.info("💥 Worker received SIGABRT signal")

# Environment variables for production
import os

# Database connection pooling
if os.getenv('DATABASE_URL'):
    # Increase worker count for database-heavy applications
    workers = int(os.getenv('WEB_CONCURRENCY', 4))

# Memory optimization
if os.getenv('FLASK_ENV') == 'production':
    # Use sync workers for better memory usage in production
    worker_class = "sync"
    workers = int(os.getenv('WEB_CONCURRENCY', 2))
    
# Development settings
if os.getenv('FLASK_ENV') == 'development':
    reload = True
    reload_extra_files = [
        'templates/',
        'static/',
        'agents/',
        'auth/',
        'payments/',
        'pages/'
    ]