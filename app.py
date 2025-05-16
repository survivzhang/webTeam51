from app import create_app
from config import Config, DevelopmentConfig, TestingConfig
import os

# Use environment variable to determine which config to use
config_name = os.environ.get('FLASK_CONFIG', 'default')

if config_name == 'development':
    app = create_app(DevelopmentConfig)
elif config_name == 'testing':
    app = create_app(TestingConfig)
else:
    app = create_app(Config)

if __name__ == '__main__':
    app.run(debug=True) 