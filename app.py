from app import create_app, db
from config import Config, DevelopmentConfig, TestingConfig
import os
import sys

# Check command line arguments
init_db = '--init-db' in sys.argv

# Use environment variable to determine which config to use
config_name = os.environ.get('FLASK_CONFIG', 'default')

if config_name == 'development':
    app = create_app(DevelopmentConfig)
elif config_name == 'testing':
    app = create_app(TestingConfig)
else:
    app = create_app(Config)

# Check if database file exists and create if needed
with app.app_context():
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:///'):
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if not os.path.exists(db_path):
            print(f"Database file does not exist. Creating database at: {db_path}")
            db.create_all()
            print("All tables created successfully!")
        else:
            print(f"Database file exists at: {db_path}")
    
    # If database initialization flag is set, run init_database function
    if init_db:
        try:
            from init_db import init_database
            print("Running database initialization...")
            init_database()
            print("Database initialization completed.")
            
            # If only initializing database without starting the app, exit
            if '--init-db-only' in sys.argv:
                print("Exiting after database initialization.")
                sys.exit(0)
        except Exception as e:
            print(f"Error initializing database: {e}")

if __name__ == '__main__':
    # Print help information
    if '--help' in sys.argv:
        print("\nUsage: python app.py [options]")
        print("\nOptions:")
        print("  --init-db       Initialize database with default data")
        print("  --init-db-only  Initialize database and exit without starting the app")
        print("  --help          Show this help message\n")
        sys.exit(0)
        
    app.run(debug=True)