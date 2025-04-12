from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

# Configure CORS - apply to all routes by default
CORS(app, resources={r"/*": {"origins": "*"}})  # For development; restrict origins in production

from app import views
