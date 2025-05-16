from flask import Flask, request, render_template, redirect, url_for, flash, session
import sys
import os
from datetime import timedelta
from functools import wraps
from sqlalchemy import and_, or_
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
import openai

# Initialize extensions outside of create_app
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
mail = Mail()

def create_app(config):
    # Create application instance - disable instance folder
    app = Flask(__name__, instance_relative_config=False, instance_path=None)
    app.config.from_object(config)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    mail.init_app(app)
    
    # Configure database options
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,  # Test database connection before executing query
    }
    
    # Configure sessions
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Session duration for remember me function
    
    with app.app_context():
        # Import models
        from .models import User
        
        # Create blueprint instance first
        from .blueprints import main
        
        # Import route modules before registering blueprints
        from . import routes
        from . import route_nav
        from . import route_api
        
        # Finally register the blueprint
        app.register_blueprint(main)
        
        # Print database configuration if not in testing mode
        if not app.config.get('TESTING', False):
            print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
            if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:///'):
                db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
                print(f"Database File Path: {db_path}")
                print(f"Database File Exists: {os.path.exists(db_path)}")
    
    return app