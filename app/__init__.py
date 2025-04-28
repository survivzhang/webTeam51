from flask import Flask, request, render_template, redirect, url_for, flash, session
import sys
import os
# 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
from functools import wraps
from sqlalchemy import and_, or_

# Create application instance - disable instance folder
app = Flask(__name__, instance_relative_config=False, instance_path=None)
app.config.from_object(Config)

# Configure database options
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,  # Test database connection before executing query
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Configure sessions
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Session duration for remember me function

# Initialize database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Print database configuration
print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
print(f"Database File Path: {db_path}")
print(f"Database File Exists: {os.path.exists(db_path)}")

# Import routes
from . import routes
from . import route_nav
from . import route_api