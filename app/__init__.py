from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_wtf.csrf import CSRFProtect
import os
from flask import send_from_directory

app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure CORS - apply to all routes by default
CORS(app, resources={r"/*": {"origins": "*"}})  # For development; restrict origins in production

db = SQLAlchemy(app)
# Instantiate Flask-Migrate library here
migrate = Migrate(app, db)

#Route to serve uploaded images

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

from app import views
from app import models  