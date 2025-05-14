import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mail Settings - Mailjet
    MAIL_SERVER = 'in-v3.mailjet.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    # For Mailjet: Username is API Key, Password is Secret Key
    MAIL_USERNAME = 'ea7165101f76cfbd95ab95a5a8e7f890'  
    MAIL_PASSWORD = '376e381e29315c47ca56f5202d076511'  
    MAIL_DEFAULT_SENDER = ('CalTrack', 'caltrack1@outlook.com')  
    MAIL_DEBUG = True  # Enable mail debugging
    MAIL_MAX_EMAILS = 5  # Limit emails per connection

    # OpenAI API Settings 
    OPENAI_API_KEY = 'Please add your own OpenAI API key'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'dev.db')
    # Add any other development-specific configurations here

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory database for testing
    WTF_CSRF_ENABLED = False  # Disable CSRF protection in tests