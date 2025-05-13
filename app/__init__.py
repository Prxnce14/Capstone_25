from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_wtf.csrf import CSRFProtect
import os
from flask import send_from_directory

from flask_login import LoginManager
from flask_jwt_extended import JWTManager  # Import JWTManager
import os
import logging
from logging.handlers import RotatingFileHandler


app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)

# Create uploads folder if it doesn't exist
uploads_path = os.path.join(app.static_folder, 'uploads')
os.makedirs(uploads_path, exist_ok=True)
app.logger.info(f"Using upload folder: {uploads_path}")

# Configure CORS - apply to all routes by default
CORS(app, resources={r"/*": {"origins": "*"}})  # For development; restrict origins in production

db = SQLAlchemy(app)
# Instantiate Flask-Migrate library here
migrate = Migrate(app, db)

#Route to serve uploaded images

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# JWTManager initialization
jwt = JWTManager(app)


# Setup security logger
def setup_security_logger(app):
    """Sets up a dedicated security logger for the application."""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # Create a security logger
    security_logger = logging.getLogger('security')
    security_logger.setLevel(logging.INFO)
    
    # Create a file handler for security logs with rotation
    security_handler = RotatingFileHandler(
        'logs/security.log', 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=10
    )
    
    # Create a formatter and set it for the handler
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - [%(ip)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Add null value for ip if not provided
    class ContextFilter(logging.Filter):
        def filter(self, record):
            if not hasattr(record, 'ip'):
                record.ip = 'N/A'
            return True
    
    context_filter = ContextFilter()
    security_logger.addFilter(context_filter)
    
    security_handler.setFormatter(formatter)
    
    # Add the handler to the logger
    security_logger.addHandler(security_handler)
    
    # Also log to console in development environment
    if app.debug:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        security_logger.addHandler(console_handler)
    
    return security_logger

# Initialize security logger
app.security_logger = setup_security_logger(app)


def log_security_event(logger, request, event_type, user_id=None, username=None, message=None, level=logging.INFO):
    """
    Logs a security event with consistent format
    
    Parameters:
    - logger: The security logger to use
    - request: Flask request object to extract IP address
    - event_type: Type of security event (login_success, login_failure, etc.)
    - user_id: ID of the user involved (if applicable)
    - username: Username of the user involved (if applicable) 
    - message: Additional details about the event
    - level: Logging level (default: INFO)
    """
    # Get IP address from request
    ip = request.remote_addr
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    
    # Build the log entry content
    log_content = f"{event_type}"
    
    if username:
        log_content += f": {username}"
    
    if message:
        log_content += f" - {message}"
    
    if user_id:
        log_content += f" (User ID: {user_id})"
    
    # Log the event with the appropriate level
    extra = {'ip': ip}
    
    if level == logging.INFO:
        logger.info(log_content, extra=extra)
    elif level == logging.WARNING:
        logger.warning(log_content, extra=extra)
    elif level == logging.ERROR:
        logger.error(log_content, extra=extra)
    elif level == logging.CRITICAL:
        logger.critical(log_content, extra=extra)


from app import views
from app import models
from app import locations
from app import helpers  
